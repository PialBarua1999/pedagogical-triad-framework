import csv
import tempfile
import unittest
from pathlib import Path
from psychometric_analysis import alpha, corr, eigen_symmetric, read_responses, analyze, ITEMS, ALL


class PsychometricsTests(unittest.TestCase):
    def test_alpha_constant_undefined(self):
        self.assertIsNone(alpha([[3]*20 for _ in range(4)]))

    def test_alpha_perfect_identical_items(self):
        a = [1,2,3,4,5]*5
        self.assertAlmostEqual(alpha([a[:]]*4),1)

    def test_correlation(self):
        self.assertAlmostEqual(corr([1,2,3,4],[4,3,2,1]),-1)

    def test_jacobi(self):
        vals,_=eigen_symmetric([[1,0.5],[0.5,1]])
        self.assertAlmostEqual(vals[0],1.5,6)
        self.assertAlmostEqual(vals[1],0.5,6)

    def test_reject_mixed_status(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'responses.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['response_id','division','setting','school_type','data_status']+ALL)
                w.writeheader()
                for i,s in enumerate(('synthetic','field_verified')):
                    w.writerow({'response_id':str(i),'division':'Dhaka','setting':'urban','school_type':'government','data_status':s,**{x:3 for x in ALL}})
            with self.assertRaisesRegex(ValueError,'Mixed data_status'):
                read_responses(p)

    def test_synthetic_not_validated(self):
        rows=[]
        for i in range(120):
            rows.append({key: 1+((i*7+j*3+(i//9))%5) for j,key in enumerate(ALL)})
        result=analyze(rows,'synthetic')
        self.assertEqual(result['n'],120)
        self.assertIn('NOT VALIDATED',result['validity_decision'])
        self.assertTrue(any('SYNTHETIC' in s for s in result['warnings']))


if __name__=='__main__':
    unittest.main()
