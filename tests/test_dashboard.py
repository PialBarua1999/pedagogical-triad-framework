"""Phase 5 dashboard integration tests; use temporary synthetic fixtures only."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dashboard import build, load_inputs, svg_line


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'data/raw').mkdir(parents=True)
        (self.root/'outputs').mkdir()
        self.records=[]
        self.codes=['SE.SEC.ENRR','SE.SEC.TCHR','SE.SEC.TCHR.FE.ZS','SE.SEC.ENRL']
        for code in self.codes:
            for year, value in [(2020,20),(2022,30)]:
                self.records.append({'indicator_code':code,'indicator':code,'country':'Bangladesh','year':year,'value':value,'source_url':'https://api.worldbank.org','retrieved_utc':'2026-11-23T00:00:00+00:00'})
        with (self.root/'data/raw/worldbank_bgd_secondary.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(self.records[0]));writer.writeheader();writer.writerows(self.records)
        q={'rows':8,'valid_numeric_rows':8,'missing_cell_counts':{},'invalid_rows':[],'duplicate_indicator_country_year':[],
           'indicators':{code:{'records':2,'years_missing_within_range':[2021]} for code in self.codes}}
        t={'country':'Bangladesh','indicator_trends':{code:{'records':2,'first_observation':{'year':2020},'last_observation':{'year':2022}} for code in self.codes},'pupil_teacher_ratio':{'shared_years_count':2}}
        p={'dataset_status':'synthetic','n':120,'validity_decision':'NOT VALIDATED — demonstration only',
           'descriptive_reliability':{code:{'cronbach_alpha':.7,'omega_total_one_factor_approx':.65,'mean_of_person_means':3} for code in ('ph','dl','eq')},
           'exploratory_construct_relationships':{},'exploratory_factor_analysis':{'performed':False},'warnings':['SYNTHETIC ONLY']}
        for filename, obj in [('worldbank_data_quality.json',q),('worldbank_trends.json',t),('psychometric_diagnostics.json',p)]:
            (self.root/'outputs'/filename).write_text(json.dumps(obj),encoding='utf-8')
        (self.root/'outputs/pupil_teacher_ratio.csv').write_text('year,pupils,teachers,pupils_per_teacher\n2020,20,20,1\n',encoding='utf-8')

    def test_build_separates_sources_and_has_exports(self):
        dest,nw,ns,status=build(self.root,self.root/'outputs/dashboard')
        self.assertEqual((nw,ns,status),(8,120,'synthetic'))
        content=dest.read_text(encoding='utf-8')
        self.assertIn('SYNTHETIC DEMONSTRATION',content)
        self.assertIn('NOT VALIDATED',content)
        self.assertIn('WORLD BANK · REAL AGGREGATE',content)
        self.assertNotIn('DEMO-0001',content)
        self.assertTrue((dest.parent/'research_summary.json').exists())
        self.assertTrue((dest.parent/'worldbank_indicator_summary.csv').exists())

    def test_rejects_stale_count(self):
        file=self.root/'outputs/worldbank_data_quality.json'
        obj=json.loads(file.read_text()); obj['rows']=7;file.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError,'record count'):
            load_inputs(self.root/'data/raw/worldbank_bgd_secondary.csv',file,self.root/'outputs/worldbank_trends.json',self.root/'outputs/psychometric_diagnostics.json')

    def test_rejects_unvalidated_missing_flag(self):
        file=self.root/'outputs/psychometric_diagnostics.json'
        obj=json.loads(file.read_text());obj['validity_decision']='validated';file.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError,'NOT VALIDATED'):
            build(self.root,self.root/'outputs/dashboard')

    def test_missing_years_not_connected(self):
        svg=svg_line('SE.SEC.ENRR',{2020:20,2022:30})
        self.assertNotIn('<polyline',svg)
        self.assertEqual(svg.count('<circle'),2)

    def test_field_label_does_not_claim_validity(self):
        file=self.root/'outputs/psychometric_diagnostics.json'
        obj=json.loads(file.read_text());obj['dataset_status']='field';file.write_text(json.dumps(obj))
        path, *_=build(self.root,self.root/'outputs/dashboard')
        self.assertIn('UNVERIFIED PROVENANCE',path.read_text(encoding='utf-8'))


if __name__=='__main__':
    unittest.main()
