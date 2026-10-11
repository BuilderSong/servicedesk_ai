import tempfile
import unittest
from pathlib import Path
from integrations.summarize_file import summarize

class FileSummary(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'notes.txt'
    def tearDown(self):self.temp.cleanup()
    def test_records_source_and_requires_review(self):
        self.path.write_text('Synthetic facts.',encoding='utf-8')
        calls=[]
        def sender(prompt):
            calls.append(prompt)
            return {'text':'A fake answer.'}
        result=summarize(self.path,sender)
        self.assertEqual(len(result['source_sha256']),64)
        self.assertEqual(result['review_status'],'needs_human_fact_check')
        self.assertIn('Synthetic facts.',calls[0])
    def test_empty_rejected_before_call(self):
        self.path.write_text('  ',encoding='utf-8')
        with self.assertRaises(ValueError):summarize(self.path,lambda p:self.fail('must not call'))
    def test_missing(self):
        with self.assertRaises(FileNotFoundError):summarize(self.path,lambda p:{'text':'x'})
    def test_provider_failure(self):
        self.path.write_text('facts',encoding='utf-8')
        def sender(prompt):raise TimeoutError('simulated')
        with self.assertRaises(TimeoutError):summarize(self.path,sender)
    def test_invalid_output(self):
        self.path.write_text('facts',encoding='utf-8')
        with self.assertRaises(ValueError):summarize(self.path,lambda p:{'text':''})
