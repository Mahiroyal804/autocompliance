"""AutoCompliance CLI."""

from __future__ import annotations

import argparse
import os
import sys


def _ask(q: str) -> str:
    while True:
        a = input(f"  {q}\n  [y]es / [n]o / [p]artial: ").strip().lower()
        if a in ("y", "yes"): return "y"
        if a in ("n", "no"): return "n"
        if a in ("p", "partial"): return "p"
        print("  Please answer y, n, or p.")


def cmd_assess(args):
    from .assess import all_questions, save_assessment, score_answers
    from .docs import generate_all
    from .report import build_report

    print(f"\n🛡️  AutoCompliance assessment — {args.company}")
    print("Answer honestly: y = yes, n = no, p = partial.\n")

    answers = {}
    current_fw = None
    for c, qi, q in all_questions(frameworks=args.frameworks):
        if c["framework"] != current_fw:
            current_fw = c["framework"]
            print(f"\n━━━ {current_fw} ━━━")
        print(f"\n[{c['id']}] {c['title']}")
        answers[(c["id"], qi)] = _ask(q["q"])

    result = score_answers(answers, frameworks=args.frameworks)
    apath = save_assessment(args.company, result)
    print(f"\n{'='*50}\n  GRADE: {result['grade']}  ({result['overall']}%)")
    for fw, s in result["frameworks"].items():
        print(f"  {fw}: {s}%")
    print(f"{'='*50}")
    print(f"\nTop fixes:")
    for f in result["fixes"][:5]:
        print(f"  [{f['priority'].upper()}] {f['fix'][:90]}")

    outdir = args.out or os.path.join(os.path.expanduser("~/.autocompliance"), "output")
    os.makedirs(outdir, exist_ok=True)
    rpath = build_report(args.company, result, os.path.join(outdir, "compliance-report.html"))
    dpaths = generate_all(args.company, args.email, os.path.join(outdir, "documents"))
    print(f"\n✅ Report: {rpath}")
    print(f"✅ {len(dpaths)} documents: {os.path.join(outdir, 'documents')}")
    print(f"✅ Raw data: {apath}")


def cmd_docs(args):
    from .docs import generate_all, list_docs
    outdir = args.out or os.path.join(os.path.expanduser("~/.autocompliance"), "documents")
    paths = generate_all(args.company, args.email, outdir)
    print(f"✅ {len(paths)} documents written to {outdir}")
    for d in list_docs():
        print(f"   - {d['filename']}")


def cmd_list(args):
    from .knowledge import CONTROLS
    fw = None
    for c in CONTROLS:
        if args.framework and c["framework"] not in args.framework:
            continue
        if c["framework"] != fw:
            fw = c["framework"]
            print(f"\n━━━ {fw} ━━━")
        print(f"  {c['id']}  {c['title']} ({len(c['questions'])} checks)")


def main():
    ap = argparse.ArgumentParser(prog="autocompliance", description="GDPR + SOC 2 compliance autopilot for SMBs.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("assess", help="Interactive compliance assessment")
    pa.add_argument("--company", required=True, help="Company name")
    pa.add_argument("--email", default="privacy@example.com", help="Privacy contact email")
    pa.add_argument("--frameworks", nargs="+", default=["GDPR", "SOC 2"], help="Frameworks to assess")
    pa.add_argument("--out", default=None, help="Output directory")
    pa.set_defaults(func=cmd_assess)

    pd = sub.add_parser("docs", help="Generate compliance document templates")
    pd.add_argument("--company", required=True)
    pd.add_argument("--email", default="privacy@example.com")
    pd.add_argument("--out", default=None)
    pd.set_defaults(func=cmd_docs)

    pl = sub.add_parser("controls", help="List all compliance controls")
    pl.add_argument("--framework", nargs="*", default=None)
    pl.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
