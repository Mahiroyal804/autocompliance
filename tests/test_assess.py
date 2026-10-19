"""Tests for the assessment engine."""

import unittest

from autocompliance.assess import all_questions, load_controls, score_answers


class TestQuestions(unittest.TestCase):
    def test_40_questions(self):
        qs = list(all_questions())
        self.assertEqual(len(qs), 40)

    def test_frameworks_split(self):
        qs = list(all_questions())
        gdpr = [q for q in qs if q[0]["framework"] == "GDPR"]
        soc2 = [q for q in qs if q[0]["framework"] == "SOC 2"]
        self.assertEqual(len(gdpr), 22)
        self.assertEqual(len(soc2), 18)

    def test_load_controls_from_json(self):
        controls = load_controls()
        self.assertEqual(len(controls), 16)
        self.assertTrue(all("questions" in c for c in controls))


class TestScoring(unittest.TestCase):
    def _answers(self, val):
        return {(c["id"], qi): val for c, qi, _ in all_questions()}

    def test_all_yes_is_A(self):
        r = score_answers(self._answers("y"))
        self.assertEqual(r["grade"], "A")
        self.assertEqual(r["overall"], 100)
        self.assertEqual(r["fixes"], [])

    def test_all_no_is_F(self):
        r = score_answers(self._answers("n"))
        self.assertEqual(r["grade"], "F")
        self.assertEqual(r["overall"], 0)
        self.assertTrue(len(r["fixes"]) > 0)

    def test_fixes_sorted_by_priority(self):
        r = score_answers(self._answers("n"))
        prio = {"critical": 0, "high": 1, "medium": 2}
        keys = [prio[f["priority"]] for f in r["fixes"]]
        self.assertEqual(keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
