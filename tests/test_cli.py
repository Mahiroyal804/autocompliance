"""Tests for the CLI parser."""

import unittest

from autocompliance.cli import DEFAULT_EMAIL, build_parser


class TestCli(unittest.TestCase):
    def test_default_email(self):
        self.assertEqual(DEFAULT_EMAIL, "mashood0109@gmail.com")

    def test_assess_defaults(self):
        args = build_parser().parse_args(["assess", "--company", "Acme"])
        self.assertEqual(args.email, DEFAULT_EMAIL)
        self.assertEqual(args.output, "./compliance-report")
        self.assertFalse(args.pdf)
        self.assertEqual(args.frameworks, ["GDPR", "SOC 2"])

    def test_pdf_flag(self):
        args = build_parser().parse_args(["assess", "--company", "Acme", "--pdf"])
        self.assertTrue(args.pdf)

    def test_docs_subcommand(self):
        args = build_parser().parse_args(["docs", "--company", "Acme"])
        self.assertEqual(args.cmd, "docs")

    def test_controls_subcommand(self):
        args = build_parser().parse_args(["controls"])
        self.assertEqual(args.cmd, "controls")


if __name__ == "__main__":
    unittest.main()
