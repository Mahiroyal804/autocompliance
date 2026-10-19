"""Tests for document generation and the PDF writer."""

import os
import tempfile
import unittest

from autocompliance.docs import DOCS, generate_all, list_docs, render_doc
from autocompliance.pdf import markdown_to_pdf


class TestDocs(unittest.TestCase):
    def test_required_docs_exist(self):
        for key in ("privacy_policy", "dpa_template", "ropa", "soc2_checklist", "risk_register"):
            self.assertIn(key, DOCS, f"missing doc: {key}")

    def test_all_docs_have_disclaimer(self):
        for key in DOCS:
            _, content = render_doc(key, "Acme Inc", "privacy@acme.com")
            self.assertIn("not legal advice", content.lower())

    def test_generate_all_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            paths = generate_all("Acme Inc", "privacy@acme.com", d)
            self.assertEqual(len(paths), len(DOCS))
            self.assertTrue(all(os.path.isfile(p) for p in paths))

    def test_generate_all_with_pdf(self):
        with tempfile.TemporaryDirectory() as d:
            paths = generate_all("Acme Inc", "privacy@acme.com", d, pdf=True,
                                 only=["privacy_policy"])
            pdfs = [p for p in paths if p.endswith(".pdf")]
            self.assertEqual(len(pdfs), 1)
            with open(pdfs[0], "rb") as f:
                self.assertEqual(f.read(5), b"%PDF-")


class TestPdf(unittest.TestCase):
    def test_pdf_header(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.pdf")
            markdown_to_pdf("# Hi\n\nBody text.", p, "T")
            with open(p, "rb") as f:
                head = f.read(8)
            self.assertEqual(head, b"%PDF-1.4")


if __name__ == "__main__":
    unittest.main()
