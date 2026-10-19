"""Assessment engine: run questionnaire, score controls, find gaps, prioritize fixes."""

from __future__ import annotations

import json
import os
import time

from .knowledge import CONTROLS

ANSWERS = {"y": 1.0, "n": 0.0, "p": 0.5}  # yes / no / partial


def all_questions(frameworks=("GDPR", "SOC 2")):
    for c in CONTROLS:
        if c["framework"] in frameworks:
            for qi, q in enumerate(c["questions"]):
                yield c, qi, q


def score_answers(answers: dict, frameworks=("GDPR", "SOC 2")) -> dict:
    """answers: {(control_id, q_index): 'y'|'n'|'p'} -> scored result."""
    controls_out = []
    total_w = 0
    earned_w = 0
    fw_scores: dict[str, list] = {}

    for c in CONTROLS:
        if c["framework"] not in frameworks:
            continue
        cw = sum(q["weight"] for q in c["questions"])
        ce = 0.0
        q_out = []
        for qi, q in enumerate(c["questions"]):
            a = answers.get((c["id"], qi), "n")
            val = ANSWERS.get(a, 0.0)
            ce += val * q["weight"]
            q_out.append({"q": q["q"], "answer": a, "fix": q["fix"], "weight": q["weight"]})
        pct = round(100 * ce / cw) if cw else 0
        status = "pass" if pct >= 80 else ("partial" if pct >= 40 else "fail")
        controls_out.append({
            "id": c["id"], "framework": c["framework"], "category": c["category"],
            "title": c["title"], "why": c["why"], "score": pct, "status": status,
            "questions": q_out, "docs": c.get("docs", []),
        })
        total_w += cw
        earned_w += ce
        fw_scores.setdefault(c["framework"], []).append(pct)

    overall = round(100 * earned_w / total_w) if total_w else 0
    fw_overall = {fw: round(sum(v) / len(v)) for fw, v in fw_scores.items()}

    # Priority fixes: failed/partial controls, sorted by total missing weight
    fixes = []
    for c in controls_out:
        if c["status"] == "pass":
            continue
        for q in c["questions"]:
            if q["answer"] != "y":
                fixes.append({
                    "control": c["id"], "category": c["category"], "framework": c["framework"],
                    "fix": q["fix"], "weight": q["weight"],
                    "priority": "critical" if (c["status"] == "fail" and q["weight"] == 3) else ("high" if q["weight"] == 3 else "medium"),
                })
    prio = {"critical": 0, "high": 1, "medium": 2}
    fixes.sort(key=lambda f: (prio[f["priority"]], -f["weight"]))

    return {
        "overall": overall,
        "frameworks": fw_overall,
        "controls": controls_out,
        "fixes": fixes,
        "grade": "A" if overall >= 85 else ("B" if overall >= 70 else ("C" if overall >= 50 else ("D" if overall >= 30 else "F"))),
    }


def save_assessment(company: str, result: dict, path: str | None = None) -> str:
    d = os.path.expanduser("~/.autocompliance")
    os.makedirs(d, exist_ok=True)
    if not path:
        ts = time.strftime("%Y%m%d-%H%M%S")
        safe = "".join(ch if ch.isalnum() else "-" for ch in company.lower())[:30]
        path = os.path.join(d, f"assessment-{safe}-{ts}.json")
    payload = {"company": company, "ts": time.time(), "result": result}
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path


def load_assessment(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
