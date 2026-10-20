import unittest
from scripts.chengdu_slides import render


class CompactReferenceTests(unittest.TestCase):
    def test_official_publisher_is_named_once_but_all_unique_links_and_citations_remain(self):
        compact=getattr(render,'_reference_links',None);self.assertTrue(callable(compact))
        rows={str(n):{'id':str(n),'publisher':'Official museum','tier':'official','url':'https://example.com/'+page,'citation_number':n,'title':page} for n,page in [(1,'history'),(2,'visit'),(3,'history')]}
        html=render._reference_links(['1','2','3'],rows,'th')
        self.assertEqual(html.count('Official museum'),1)
        self.assertEqual(html.count('href="https://example.com/history"'),1)
        self.assertEqual(html.count('href="https://example.com/visit"'),1)
        self.assertIn('[1, 3]',html);self.assertIn('[2]',html)

    def test_community_dates_and_index_excerpt_qualifiers_are_not_collapsed(self):
        compact=getattr(render,'_reference_links',None);self.assertTrue(callable(compact))
        rows={str(n):{'id':str(n),'publisher':'Forum','tier':'community','url':'https://example.com/thread','published_at':day,'access_state':'indexed_excerpt','citation_number':n} for n,day in [(1,'2020-01-01'),(2,'2022-02-02')]}
        html=render._reference_links(['1','2'],rows,'th')
        self.assertIn('2020-01-01',html);self.assertIn('2022-02-02',html)
        self.assertEqual(html.count('ข้อความบางส่วน'),2)
