"""Thai-first pagination preserves source text and supports unequal language pages."""
import copy
import re
import unittest
from html.parser import HTMLParser
from fixtures import sample_dataset
from scripts.chengdu_slides import pagination
from scripts.chengdu_slides.render import render_deck


class Sections(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]
    def handle_starttag(self, tag, attrs):
        row=dict(attrs)
        if tag=='section' and 'slide' in (row.get('class') or '').split(): self.rows.append(row)


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.data=sample_dataset()
        self.data['assets']=[{'id':'fixture-image','kind':'diagram','path':'slides/chengdu/images/fixture.svg'}]

    def test_regroup_removes_old_artificial_splits_without_mutating_sources(self):
        item=self.data['attractions'][0]; original=copy.deepcopy(item['units'][0])
        second=copy.deepcopy(original); second['id']=original['id']+'-present-2'
        second['body']={lang:['second '+lang] for lang in ('th','zh-Hans')}
        second['source_ids']=['additional-source']; item['units'].insert(1,second)
        snapshot=copy.deepcopy(self.data); result=pagination.regroup_dataset(self.data)
        self.assertEqual(self.data,snapshot)
        group=result['attractions'][0]['units'][0]
        self.assertEqual(group['body']['th'],original['body']['th']+['second th'])
        self.assertIn('additional-source',group['source_ids'])
        self.assertIn(second['id'],group['legacy_ids'])
        self.assertNotIn('continuation',group)
        self.assertEqual(len(result['attractions'][0]['units']),2)

    def planned(self):
        data=pagination.regroup_dataset(self.data)
        for lang in ('th','zh-Hans'):
            data['attractions'][0]['units'][1]['body'][lang].append('second '+lang)
        for item in data['attractions']:
            for unit in item['units']:
                n=len(unit['body']['th']); unit['pagination']=[{'th':[0,n],'zh-Hans':[[0,n]]}]
        unit=data['attractions'][0]['units'][1]
        unit['pagination']=[{'th':[0,2],'zh-Hans':[[0,1],[1,2]]}]
        data['meta']['pagination_signature']=pagination.layout_signature(data)
        return data

    def test_one_thai_page_can_have_two_chinese_pages_without_losing_text(self):
        data=self.planned(); rendered=render_deck(data); parser=Sections(); parser.feed(rendered)
        th=[r for r in parser.rows if r['data-lang']=='th']; zh=[r for r in parser.rows if r['data-lang']=='zh-Hans']
        self.assertEqual((len(th),len(zh)),(2,3))
        self.assertEqual(zh[-1]['id'],'fixture-details-page-2--zh-Hans')
        self.assertEqual(zh[-1]['data-pair-id'],th[-1]['data-pair-id'])
        self.assertEqual(re.findall(r'class="page-no">(\d+)</span>',rendered),['001','001','002','002','003'])
        for lang in ('th','zh-Hans'):
            for unit in data['attractions'][0]['units']:
                for body in unit['body'][lang]: self.assertIn(body.format_map(data['attractions'][0]['facts']),rendered)

    def test_every_bullet_is_covered_exactly_once_in_each_language(self):
        data=self.planned(); self.assertEqual(pagination.validate_pagination(data),[])
        unit=data['attractions'][0]['units'][1]
        for windows in ([[0,1]],[[0,1],[0,2]],[[1,2]],[[0,3]],[[-1,2]],[[True,2]]):
            with self.subTest(windows=windows):
                unit['pagination'][0]['zh-Hans']=windows
                self.assertTrue(pagination.validate_pagination(data))

    def test_chinese_cannot_merge_across_thai_page_boundaries(self):
        data=self.planned(); unit=data['attractions'][0]['units'][1]
        unit['pagination']=[{'th':[0,1],'zh-Hans':[[0,2]]},{'th':[1,2],'zh-Hans':[[1,2]]}]
        self.assertTrue(pagination.validate_pagination(data))

    def test_stale_measurements_fail_closed_but_draft_status_is_not_layout(self):
        data=self.planned(); data['meta']['status']='research_incomplete'
        self.assertEqual(pagination.validate_pagination(data),[])
        data['attractions'][0]['units'][0]['body']['th'][0]+=' changed'
        self.assertTrue(pagination.validate_pagination(data))
        with self.assertRaises(ValueError): render_deck(data)

    def test_missing_or_malformed_page_plans_are_not_silently_ignored(self):
        for plan in (None,[],{},[{'th':[0,2]}]):
            data=self.planned(); data['attractions'][0]['units'][1]['pagination']=plan
            self.assertTrue(pagination.validate_pagination(data))

    def test_removing_policy_flag_does_not_bypass_plan_validation(self):
        data=self.planned(); data['meta'].pop('pagination_policy')
        self.assertTrue(pagination.validate_pagination(data))
        with self.assertRaises(ValueError): render_deck(data)


if __name__=='__main__': unittest.main()
