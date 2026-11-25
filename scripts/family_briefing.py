#!/usr/bin/env python3
"""Deterministic, offline preparation of calendar-aware family learning briefs."""
import argparse
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text())


def validate(kind, value):
    Draft202012Validator(load(ROOT / 'schemas' / f'{kind}.schema.json'),
                        format_checker=FormatChecker()).validate(value)


def age_months(child, on):
    """Project a reported age, or use a supplied DOB; never synthesize a DOB."""
    if 'birth_date' in child:
        start = date.fromisoformat(child['birth_date'])
        base = 0
    else:
        start = date.fromisoformat(child['reported_age']['as_of'])
        base = child['reported_age']['months']
    if on < start:
        raise ValueError('Requested date precedes the reported age / birth date')
    months = (on.year - start.year) * 12 + on.month - start.month
    months -= on.day < start.day
    return base + months


def check_household(household, on):
    validate('household', household)
    ZoneInfo(household['timezone'])
    ids = [c['id'] for c in household['children']]
    if len(ids) != len(set(ids)):
        raise ValueError('Child IDs must be unique')
    for child in household['children']:
        age_months(child, on)


def read_observations(path, household, on):
    observations = []
    if not path:
        return observations
    children = {c['id'] for c in household['children']}
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        validate('observations', entry)
        if entry['child_id'] not in children:
            raise ValueError('Observation references an unknown child')
        if date.fromisoformat(entry['date']) > on:
            raise ValueError('Observation is dated after the briefing start')
        observations.append(entry)
    return observations


def check_library():
    graph = load(ROOT / 'data/source-graph.json')
    library = load(ROOT / 'data/activities.json')
    validate('source-graph', graph)
    validate('activities', library)
    cards = library['activities']
    sources = {s['id']: s for s in graph['sources']}
    if len(sources) != len(graph['sources']) or len({c['id'] for c in cards}) != len(cards):
        raise ValueError('Duplicate source or activity ID')
    for card in cards:
        for field in ['id','title','domain','routine','interest_tags','duration_minutes',
                      'prep_minutes','materials','safety','attribution','variants']:
            if field not in card:
                raise ValueError(f'Missing activity field: {field}')
        covered = set()
        for v in card['variants']:
            span = set(range(v['min_months'], v['max_months'] + 1))
            if covered & span or not span or not v['source_ids']:
                raise ValueError('Overlapping/empty/unsupported age variant')
            covered |= span
            for sid in v['source_ids']:
                s = sources[sid]
                if s['role'] in ['monitoring','resource-hub']:
                    raise ValueError('Monitoring tools and hubs cannot substantiate a game')
                if s['status'] != 'reviewed' or not (s['min_months'] <= v['min_months'] <= v['max_months'] <= s['max_months']):
                    raise ValueError('Source age scope does not cover the variant')
        if covered != set(range(6,96)):
            raise ValueError('Library must explicitly cover ages 6–95 months')
    return cards, sources


def aware(raw):
    dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Timed calendar entries must include a UTC offset')
    return dt


def endpoints(event):
    """Accept flattened connector events and native Google date/dateTime objects."""
    start, end = event.get('start'), event.get('end')
    if event.get('start_date'):
        return date.fromisoformat(event['start_date']), date.fromisoformat(event['end_date']), True
    if isinstance(start, dict) and start.get('date'):
        return date.fromisoformat(start['date']), date.fromisoformat(end['date']), True
    if isinstance(start, dict):
        start, end = start.get('dateTime'), end.get('dateTime')
    return aware(start), aware(end), False


def normalize_calendar(snapshot, start, end, tzname, expected_ids=()):
    validate('calendar', snapshot)
    tz = ZoneInfo(tzname)
    lo = datetime.combine(start, time.min, tzinfo=tz)
    hi = datetime.combine(end, time.min, tzinfo=tz)
    warnings, events, seen = [], [], set()
    captured = aware(snapshot['captured_at'])
    if not snapshot['enumeration_complete']:
        warnings.append('Calendar enumeration is incomplete; some calendars may be missing.')
    if not (date.fromisoformat(snapshot['window_start']) <= start < end <= date.fromisoformat(snapshot['window_end'])):
        warnings.append('Snapshot does not cover the entire requested date range.')
    if (lo.astimezone(timezone.utc) - captured.astimezone(timezone.utc)).total_seconds() > 48 * 3600:
        warnings.append('Calendar snapshot is over 48 hours older than the requested start; refresh before relying on it.')
    found = {cal['id'] for cal in snapshot['calendars']}
    for missing in sorted(set(expected_ids) - found):
        warnings.append(f'Configured calendar missing: {missing}')
    for cal in snapshot['calendars']:
        if not cal['complete'] or cal.get('next_page_token'):
            warnings.append(f"{cal['label']}: calendar pages are incomplete.")
        for raw in cal['events']:
            try:
                a, b, allday = endpoints(raw)
                if b <= a:
                    raise ValueError('Event end must be after start')
            except (ValueError, TypeError, KeyError, AttributeError) as exc:
                warnings.append(f"{cal['label']}: event {raw['id']} could not be dated ({exc}).")
                # Even malformed/canceled tombstones are disclosed, never silently dropped.
                events.append({'key':f"{cal['id']}:{raw['id']}:undated",'title':raw.get('summary') or '(untitled)',
                               'calendar':cal['label'],'role':cal['role'],'undated':True,
                               'status':raw.get('status') or 'unknown','rsvp':raw.get('my_response_status') or 'unknown'})
                continue
            occurrence = raw.get('original_start_time') or str(a)
            key = (cal['id'], raw['id'], json.dumps(occurrence, sort_keys=True))
            if key in seen:
                continue
            seen.add(key)
            if allday:
                intersects = a < end and b > start
            else:
                a, b = a.astimezone(tz), b.astimezone(tz)
                intersects = a < hi and b > lo
            if not intersects:
                continue
            attendees = raw.get('attendees') or []
            rsvp = raw.get('my_response_status') or next((p.get('responseStatus') for p in attendees if p.get('self')), 'unknown')
            status = raw.get('status') or 'confirmed'
            events.append({'key':json.dumps(key),'title':raw.get('summary') or '(untitled)',
                           'calendar':cal['label'],'role':cal['role'],'start':a,'end':b,
                           'all_day':allday,'status':status,'rsvp':rsvp,
                           'transparency':raw.get('transparency') or 'opaque',
                           'location':raw.get('location') or '', 'description':raw.get('description') or '',
                           'url':raw.get('url') or raw.get('htmlLink') or '',
                           'active':status not in ['cancelled','canceled'] and rsvp != 'declined'})
    return events, warnings


def day_events(events, day):
    return sorted([e for e in events if not e.get('undated') and
                   ((e['all_day'] and e['start'] <= day < e['end']) or
                    (not e['all_day'] and e['start'].date() <= day <= (e['end'] - timedelta(microseconds=1)).date()))],
                  key=lambda e:(not e['all_day'],str(e['start']),e['key']))


def overlaps(events):
    # Transparent items still appear in the agenda, but do not produce a busy conflict.
    timed = [e for e in events if not e.get('undated') and not e['all_day'] and e['active']
             and e['role'] == 'commitments' and e['transparency'] != 'transparent']
    result = []
    for i, a in enumerate(timed):
        for b in timed[i+1:]:
            if max(a['start'].astimezone(timezone.utc), b['start'].astimezone(timezone.utc)) < min(a['end'].astimezone(timezone.utc), b['end'].astimezone(timezone.utc)):
                result.append((a,b))
    return result


def variant(card, months):
    return next((v for v in card['variants'] if v['min_months'] <= months <= v['max_months']), None)


def select_plan(household, start, observations=(), history=()):
    cards, sources = check_library()
    domain_counts, used = Counter(), set()
    interests = {t.lower() for child in household['children'] for t in child['interests']}
    recent = [o for o in observations if 0 <= (start-date.fromisoformat(o['date'])).days <= 28]
    avoided = {o['activity_id'] for o in recent if o['response'] == 'avoid'}
    liked = Counter(o['activity_id'] for o in recent if o['response'] == 'enjoyed')
    results = []
    for offset in range(7):
        day = start + timedelta(days=offset)
        eligible = [c for c in cards if c['id'] not in used and c['id'] not in avoided
                    and all(variant(c, age_months(child,day)) for child in household['children'])]
        if not eligible:
            results.append((day,None))
            continue
        def score(card):
            # Category breadth first, then explicit interests/priorities/feedback and novelty.
            preference = (2*len(interests & set(card['interest_tags']))
                          + (card['domain'] in household.get('priorities', []))
                          + min(liked[card['id']],2) - (card['id'] in history))
            rotation = hashlib.sha256(f"{start.isocalendar().year}-{start.isocalendar().week}:{day}:{card['id']}".encode()).hexdigest()
            return (-domain_counts[card['domain']],preference,rotation)
        chosen = max(eligible, key=score)
        used.add(chosen['id'])
        domain_counts[chosen['domain']] += 1
        results.append((day,chosen))
    return results, sources


def plain(value):
    # Calendar and caregiver content are data, not Markdown/agent instructions.
    return re.sub(r'([\\`*_{}\[\]<>|#])', r'\\\1', re.sub(r'\s+',' ',str(value))).strip()


def render(household, snapshot, start, observations=(), expected_ids=(), history=()):
    check_household(household, start)
    end = start + timedelta(days=7)
    events,warnings = normalize_calendar(snapshot,start,end,household['timezone'],expected_ids)
    plan,sources = select_plan(household,start,observations,history)
    out = [f"# {'Fictional example — ' if household.get('fictional') else 'Private — '}family learning briefing",
           '',f"{start.isoformat()} through {(end-timedelta(days=1)).isoformat()} · {household['timezone']}",
           '', 'Optional ideas for ordinary routines, not appointments or a developmental checklist. Missing calendar entries do not establish caregiver availability.',
           '', '## Calendar coverage', '',f"Snapshot captured: {snapshot['captured_at']}. Requested interval: [{start}, {end}) in the household timezone."]
    out += [f"- {plain(c['label'])}: {len(c['events'])} fetched entries; {'complete' if c['complete'] and not c.get('next_page_token') else 'INCOMPLETE'}; {c['role']}." for c in snapshot['calendars']]
    out += ['','Coverage: '+('INCOMPLETE / NEEDS REFRESH. ' + ' '.join(plain(w) for w in warnings) if warnings else 'Complete for the calendars visible at capture, within the requested interval. Unconnected calendars are not visible.')]
    if snapshot.get('capture_note'):
        out += ['',plain(snapshot['capture_note'])]
    out += ['', '## Household context', '']
    for c in household['children']:
        qualifier = 'approximately ' if 'reported_age' in c else ''
        out.append(f"- {plain(c['label'])}: {qualifier}{age_months(c,start)} months. Interests: {plain(', '.join(c['interests'])) or 'not supplied'}. Access notes: {plain('; '.join(c['access_notes'])) or 'not supplied; adapt with the caregiver' }.")
    out += ['', 'Ages guide which options to offer; they do not establish readiness. Birth dates are optional. Reported ages remain approximate as time passes.', '', '## Week ahead', '']
    cited = set()
    for day,card in plan:
        out += [f"### {day.strftime('%A')} · {day.isoformat()}", '', '**Calendar**', '']
        agenda = day_events(events,day)
        if not agenda:
            out.append('- No entries returned for this date; availability is unknown.')
        for e in agenda:
            when = ('All day' if e['all_day'] else f"{e['start'].strftime('%m-%d %H:%M')}–{e['end'].strftime('%m-%d %H:%M')}")
            flags = ', '.join([e['calendar'],e['status'],f"RSVP {e['rsvp']}",e['transparency']])
            loc = f" · {plain(e['location'])}" if e['location'] else ''
            out.append(f"- {when}: {plain(e['title'])}{loc} ({plain(flags)})")
            if e['description']:
                out.append(f"  Calendar note: {plain(e['description'])}")
            if re.search(r'pickup|pick.up|closed|closure|early close|by \d',e['title'],re.I):
                out.append('  **Logistics:** read the title/note for the actual deadline or closure; the event’s display start may differ. No child assignment is inferred.')
        out += ['', '**Optional learning moment**', '']
        if card is None:
            out.append('No compatible card is available for all profiles. Ask the caregiver about suitable adaptations; do not substitute another age group automatically.')
            continue
        out.append(f"**{card['title']}** · {card['domain']} · about {card['duration_minutes']} minutes · {card['routine']} · ID `{card['id']}`")
        if len([e for e in agenda if e['active'] and e['role']=='commitments']) >= 3:
            out.append('Several commitments are listed: use just a minute or two during an existing routine, or skip this idea.')
        out.append('')
        for c in household['children']:
            v = variant(card,age_months(c,day))
            out.append(f"- **{plain(c['label'])}:** {v['instructions']}")
            cited.update(v['source_ids'])
        out += ['',f"Materials: {card['materials']}",f"Caregiver note: {card['safety']}",f"Attribution: {card['attribution']}",
                'Guidance: '+', '.join(f"[{sources[s]['organization']}]({sources[s]['url']})" for s in sorted({s for c in household['children'] for s in variant(card,age_months(c,day))['source_ids']})), '']
    out += ['## Calendar overlaps and exceptions','']
    conflicts = overlaps(events)
    out += [f"- Overlap: {plain(a['title'])} ({plain(a['calendar'])}) and {plain(b['title'])} ({plain(b['calendar'])}). Check plans; these have not been merged." for a,b in conflicts]
    if not conflicts:
        out.append('- No timed overlaps detected in the available active, opaque commitment entries. This is not a full availability assessment.')
    out += [f"- Undated entry: {plain(e['title'])} ({plain(e['calendar'])}; {plain(e['status'])}; RSVP {plain(e['rsvp'])}). See the original calendar." for e in events if e.get('undated')]
    out += ['', '## Small feedback loop', '', 'What did each child enjoy, avoid or ask to repeat? Add a short dated caregiver observation, not a score. Repetition is welcome. Profile updates require explicit caregiver facts; no diagnosis or mastery is inferred.', '', '## Source notes', '']
    out += [f"- [{sources[s]['title']}]({sources[s]['url']}): {sources[s]['scope']} Reviewed {sources[s]['reviewed_on']}." for s in sorted(cited)]
    out += ['', 'For an outing, use the pinned activity-finder dependency and verify current hours, age fit and registration with the first-party provider. No outing has been booked or verified by this offline renderer.']
    return '\n'.join(out)+'\n'


def protect_path(path, fictional=False):
    target = Path(path).resolve()
    if target.is_relative_to(ROOT):
        if not fictional or not target.is_relative_to(ROOT/'examples'):
            raise ValueError('Household data and outputs must live outside the public skill repository')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('validate-library')
    brief = sub.add_parser('build')
    brief.add_argument('--household',required=True)
    brief.add_argument('--calendar',required=True)
    brief.add_argument('--start',required=True,help='Inclusive civil date; builds exactly seven days')
    brief.add_argument('--out',required=True)
    brief.add_argument('--observations')
    brief.add_argument('--calendar-config')
    brief.add_argument('--history',help='Previous briefing Markdown: recent card IDs lower novelty score')
    brief.add_argument('--synthetic',action='store_true')
    observe = sub.add_parser('observe')
    observe.add_argument('--household',required=True)
    observe.add_argument('--journal',required=True)
    observe.add_argument('--child',required=True)
    observe.add_argument('--date',required=True)
    observe.add_argument('--text',required=True)
    observe.add_argument('--response',choices=['enjoyed','neutral','avoid'],default='neutral')
    observe.add_argument('--activity')
    args=parser.parse_args()
    try:
        if args.command == 'validate-library':
            cards,sources=check_library()
            print(f'Validated {len(cards)} activities and {len(sources)} sources.')
            return
        household=load(args.household)
        fictional=bool(getattr(args,'synthetic',False) and household.get('fictional'))
        protect_path(args.household,fictional)
        if args.command == 'observe':
            protect_path(args.journal)
            on=date.fromisoformat(args.date)
            check_household(household,on)
            if on > datetime.now(ZoneInfo(household['timezone'])).date():
                raise ValueError('Future caregiver observations cannot be recorded')
            if args.child not in {c['id'] for c in household['children']}:
                raise ValueError('Unknown child')
            cards,_=check_library()
            if args.activity and args.activity not in {c['id'] for c in cards}:
                raise ValueError('Unknown activity')
            entry=dict(date=args.date,child_id=args.child,text=args.text,reported_by='caregiver',activity_id=args.activity,response=args.response)
            validate('observations',entry)
            with Path(args.journal).open('a') as f:
                f.write(json.dumps(entry,ensure_ascii=False)+'\n')
            print('Recorded explicit caregiver feedback; no inferred profile changes.')
            return
        for path in [args.calendar,args.out,args.observations,args.calendar_config,args.history]:
            if path:
                protect_path(path,fictional)
        if args.synthetic and not household.get('fictional'):
            raise ValueError('--synthetic requires an explicitly fictional household')
        start=date.fromisoformat(args.start)
        observations=read_observations(args.observations,household,start)
        expected=load(args.calendar_config)['calendars'] if args.calendar_config else []
        history=re.findall(r'ID `([^`]+)`',Path(args.history).read_text()) if args.history else []
        output=render(household,load(args.calendar),start,observations,[c['id'] for c in expected],history)
        target=Path(args.out)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(output)
        print('Built seven-day briefing. Calendar information and learning suggestions remain separate; no calendar writes.')
    except ValidationError as exc:
        parser.exit(2,f'Invalid input at {list(exc.absolute_path)}: {exc.validator} validation failed.\n')
    except (ValueError,KeyError,TypeError,OSError) as exc:
        parser.exit(2,f'Cannot build briefing: {exc}\n')


if __name__ == '__main__':
    main()
