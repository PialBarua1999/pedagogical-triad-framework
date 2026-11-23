import csv
import tempfile
import unittest
from pathlib import Path
from survey_check import audit, REQUIRED

class SurveyCheckTests(unittest.TestCase):
    def write(self, rows):
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / 'input.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=REQUIRED)
            writer.writeheader()
            writer.writerows(rows)
        return tmp, path

    def sample(self):
        row = dict.fromkeys(REQUIRED, '3')
        row.update(response_id='T001', division='Dhaka', setting='urban', school_type='non-government', data_status='synthetic')
        return row

    def test_valid(self):
        t,p=self.write([self.sample()])
        try: self.assertTrue(audit(p)['schema_valid'])
        finally: t.cleanup()

    def test_duplicate(self):
        row=self.sample(); t,p=self.write([row,row])
        try: self.assertFalse(audit(p)['schema_valid'])
        finally: t.cleanup()

    def test_invalid_item(self):
        row=self.sample(); row['ph1']='6'; t,p=self.write([row])
        try: self.assertFalse(audit(p)['schema_valid'])
        finally: t.cleanup()

    def test_blank_template_rejected(self):
        t,p=self.write([])
        try: self.assertFalse(audit(p)['schema_valid'])
        finally: t.cleanup()

if __name__ == '__main__': unittest.main()
