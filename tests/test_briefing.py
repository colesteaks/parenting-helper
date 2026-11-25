import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('brief',ROOT/'scripts/family_briefing.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class BriefingTests(unittest.TestCase):
    def setUp(self):
        self.h=b.load(ROOT/'examples/fictional-household.json')
        self.s=b.load(ROOT/'examples/fictional-calendar.json')
        self.start=date(2026,11,23)

    def event(self,id='e',**kwargs):
        return dict(id=id,summary='Same title',start='2026-11-24T09:00:00-06:00',
                    end='2026-11-24T10:00:00-06:00',**kwargs)

    def normalized(self):
        return b.normalize_calendar(self.s,self.start,date(2026,11,30),'America/Chicago')

    def test_reported_age_grows_without_inventing_dob(self):
        child=self.h['children'][0]
        self.assertEqual(b.age_months(child,date(2027,1,1)),56)
        self.assertNotIn('birth_date',child)
        with self.assertRaises(ValueError): b.age_months(child,date(2026,10,1))

    def test_birth_date_leap_and_completed_month(self):
        c={'birth_date':'2024-02-29'}
        self.assertEqual(b.age_months(c,date(2025,2,28)),11)
        self.assertEqual(b.age_months(c,date(2025,3,1)),12)

    def test_duplicate_child_ids_and_ambiguous_age_rejected(self):
        self.h['children'][1]['id']=self.h['children'][0]['id']
        with self.assertRaises(ValueError): b.check_household(self.h,self.start)
        self.h['children'][0]['birth_date']='2022-01-01'
        with self.assertRaises(Exception): b.check_household(self.h,self.start)

    def test_library_has_age_scoped_sources_and_no_monitoring_curriculum(self):
        cards,sources=b.check_library()
        for c in cards:
            for v in c['variants']:
                for sid in v['source_ids']:
                    self.assertNotEqual(sources[sid]['role'],'monitoring')
                    if v['max_months']<36: self.assertNotIn('ies-prek',v['source_ids'])

    def test_mixed_age_variants_differ_and_plan_is_reproducible(self):
        a,_=b.select_plan(self.h,self.start)
        z,_=b.select_plan(self.h,self.start)
        self.assertEqual(a,z)
        self.assertEqual(len({c['domain'] for _,c in a}),7)
        for day,card in a:
            variants=[b.variant(card,b.age_months(c,day))['instructions'] for c in self.h['children']]
            self.assertEqual(len(set(variants)),2)
        future,_=b.select_plan(self.h,date(2026,11,30))
        self.assertNotEqual([c['id'] for _,c in a],[c['id'] for _,c in future])

    def test_unsupported_age_does_not_get_another_age_variant(self):
        self.h['children'][0]['reported_age']['months']=120
        plan,_=b.select_plan(self.h,self.start)
        self.assertTrue(all(c is None for _,c in plan))

    def test_explicit_feedback_changes_preferences_without_changing_profile(self):
        before=copy.deepcopy(self.h)
        obs=[dict(date='2026-11-22',child_id='robin',text='Wanted to stop',reported_by='caregiver',activity_id='book-conversation',response='avoid')]
        plan,_=b.select_plan(self.h,self.start,obs)
        self.assertNotIn('book-conversation',[c['id'] for _,c in plan])
        self.assertEqual(before,self.h)

    def test_all_day_end_is_exclusive_and_stays_civil(self):
        events,warnings=self.normalized()
        self.assertEqual(len(b.day_events(events,date(2026,11,26))),1)
        self.assertEqual(len(b.day_events(events,date(2026,11,27))),0)
        self.assertFalse(warnings)

    def test_native_google_events_normalize(self):
        self.s['calendars'][0]['events']=[dict(id='native',summary='Day',start={'date':'2026-11-25'},end={'date':'2026-11-27'})]
        events,_=self.normalized()
        self.assertEqual(len(b.day_events(events,date(2026,11,26))),1)
        self.assertEqual(len(b.day_events(events,date(2026,11,27))),0)

    def test_overlaps_and_duplicates_not_semantically_merged(self):
        self.s['calendars'][0]['events']=[self.event('e'),self.event('e'),self.event('different')]
        events,_=self.normalized()
        self.assertEqual(len(events),2)
        self.assertEqual(len(b.overlaps(events)),1)
        duplicate_calendar=copy.deepcopy(self.s['calendars'][0])
        duplicate_calendar['id']='another-calendar'
        self.s['calendars'].append(duplicate_calendar)
        events,_=self.normalized()
        self.assertEqual(len(events),4)

    def test_declined_cancelled_transparent_still_appear_but_not_busy(self):
        self.s['calendars'][0]['events']=[self.event('accepted'),self.event('declined',my_response_status='declined'),self.event('cancelled',status='cancelled'),self.event('transparent',transparency='transparent')]
        events,_=self.normalized()
        self.assertEqual(len(events),4)
        self.assertFalse(b.overlaps(events))
        output=b.render(self.h,self.s,self.start)
        for flag in ['declined','cancelled','transparent']: self.assertIn(flag,output)

    def test_partial_calendar_enumeration_pagination_missing_calendar(self):
        self.s['enumeration_complete']=False
        self.s['calendars'][0]['next_page_token']='more'
        events,warnings=b.normalize_calendar(self.s,self.start,date(2026,11,30),'America/Chicago',['not-returned'])
        self.assertEqual(len(warnings),3)
        self.assertIn('INCOMPLETE',b.render(self.h,self.s,self.start))

    def test_window_mismatch_and_stale_snapshot_warn(self):
        self.s['captured_at']='2026-10-01T00:00:00Z'
        self.s['window_end']='2026-11-27'
        _,warnings=self.normalized()
        self.assertEqual(len(warnings),2)

    def test_missing_time_or_naive_time_disclosed_not_dropped(self):
        self.s['calendars'][0]['events']=[{'id':'tombstone','status':'cancelled'},{'id':'naive','start':'2026-11-24T09:00:00','end':'2026-11-24T10:00:00'}]
        events,warnings=self.normalized()
        self.assertEqual(len(events),2)
        self.assertEqual(len(warnings),2)
        output=b.render(self.h,self.s,self.start)
        self.assertIn('Undated entry',output)

    def test_timezone_conversion_and_multiday_midnight_end(self):
        self.s['calendars'][0]['events']=[{'id':'late','start':'2026-11-24T23:30:00-08:00','end':'2026-11-25T22:00:00-08:00'}]
        events,_=self.normalized()
        self.assertFalse(b.day_events(events,date(2026,11,24)))
        self.assertEqual(len(b.day_events(events,date(2026,11,25))),1)
        self.assertFalse(b.day_events(events,date(2026,11,26)))

    def test_dst_fall_back_overlap_uses_real_instant(self):
        snapshot=copy.deepcopy(self.s)
        snapshot.update(window_start='2026-11-01',window_end='2026-11-02',captured_at='2026-10-31T12:00:00Z')
        snapshot['calendars'][0]['events']=[{'id':'before','start':'2026-11-01T01:15:00-05:00','end':'2026-11-01T01:45:00-05:00'},{'id':'after','start':'2026-11-01T01:15:00-06:00','end':'2026-11-01T01:45:00-06:00'}]
        events,_=b.normalize_calendar(snapshot,date(2026,11,1),date(2026,11,2),'America/Chicago')
        self.assertFalse(b.overlaps(events))

    def test_calendar_and_profile_content_not_instructions(self):
        self.s['calendars'][0]['events'][0]['summary']='<script>alert(1)</script> [link](javascript:evil)'
        result=b.render(self.h,self.s,self.start)
        self.assertNotIn('<script>',result)
        self.assertNotIn('[link](javascript:',result)

    def test_no_availability_inference_and_all_entries_included(self):
        result=b.render(self.h,self.s,self.start)
        self.assertIn('availability is unknown',result)
        for e in self.s['calendars'][0]['events']: self.assertIn(e['summary'],result)
        self.assertNotIn('free at',result)

    def test_privacy_guard_resolves_symlinks(self):
        with self.assertRaises(ValueError): b.protect_path(ROOT/'data/private.json')
        with tempfile.TemporaryDirectory() as temp:
            link=Path(temp)/'public-link'
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(ValueError): b.protect_path(link/'private.json')
        b.protect_path(ROOT/'examples/fictional-household.json',True)


if __name__ == '__main__':
    unittest.main()
