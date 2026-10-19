"""AutoCompliance CLI — GDPR + SOC 2 compliance autopilot for small businesses.

Answer 40 yes/no questions, get a compliance grade (A-F), a prioritized
fix list, and a full set of generated documents (markdown + PDF).
"""

from __future__ import annotations

import argparse
import os
import sys

DEFAULT_EMAIL = "mashood0109@gmail.com"
DEFAULT_OUT = "./compliance-report"


def _ask(q: str) -> str:
    while True:
        a = input(f"  {q}\n  [y]es / [n]o / [p]artial: ").strip().lower()
        if a in ("y", "yes"):
            return "y"
        if a in ("n", "no"):
            return "n"
        if a in ("p", "partial"):
            return "p"
        print("  Please answer y, n, or p.")


def cmd_assess(args):
    from .assess import all_questions, save_assessment, score_answers
    from .docs import generate_all
    from .report import build_report

    print(f"\n  AutoCompliance assessment — {args.company}")
    print("  Answer honestly: y = yes, n = no, p = partial.\n")

    answers = {}
    current_fw = None
    for c, qi, q in all_questions(frameworks=args.frameworks):
        if c["framework"] != current_fw:
            current_fw = c["framework"]
            print(f"\n  --- {current_fw} ---")
        print(f"\n  [{c['id']}] {c['title']}")
        answers[(c["id"], qi)] = _ask(q["q"])

    result = score_answers(answers, frameworks=args.frameworks)
    apath = save_assessment(args.company, result)
    print(f"\n  {'=' * 46}\n  GRADE: {result['grade']}  ({result['overall']}%)")
    for fw, s in result["frameworks"].items():
        print(f"  {fw}: {s}%")
    print(f"  {'=' * 46}")
    print("\n  Top fixes:")
    for f in result["fixes"][:5]:
        print(f"  [{f['priority'].upper()}] {f['fix'][:88]}")

    outdir = os.path.abspath(args.output)
    os.makedirs(outdir, exist_ok=True)
    rpath = build_report(args.company, result, os.path.join(outdir, "compliance-report.html"))
    dpaths = generate_all(args.company, args.email, os.path.join(outdir, "documents"),
                          pdf=args.pdf)
    print(f"\n  Report: {rpath}")
    print(f"  {len(dpaths)} documents: {os.path.join(outdir, 'documents')}")
    print(f"  Raw data: {apath}")


def cmd_docs(args):
    from .docs import generate_all, list_docs
    outdir = os.path.abspath(args.output)
    paths = generate_all(args.company, args.email, outdir, pdf=args.pdf)
    print(f"  {len(paths)} files written to {outdir}")
    for d in list_docs():
        print(f"   - {d['filename']}")


def cmd_list(args):
    from .assess import load_controls
    fw = None
    total = 0
    for c in load_controls():
        if args.framework and c["framework"] not in args.framework:
            continue
        if c["framework"] != fw:
            fw = c["framework"]
            print(f"\n  --- {fw} ---")
        n = len(c["questions"])
        total += n
        print(f"  {c['id']}  {c['title']} ({n} checks)")
    print(f"\n  Total: {total} questions")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="autocompliance",
        description=(
            "AutoCompliance — open-source GDPR + SOC 2 compliance autopilot for "
            "small businesses. Answer 40 yes/no questions and get an A-F grade, "
            "a prioritized fix list, and generated compliance documents."
        ),
        epilog=(
            "Examples:\n"
            '  autocompliance assess --company "Acme Inc" --email privacy@acme.com\n'
            '  autocompliance assess --company "Acme Inc" --output ./report --pdf\n'
            '  autocompliance docs --company "Acme Inc"\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True, metavar="command")

    pa = sub.add_parser("assess", help="Run the interactive 40-question assessment")
    pa.add_argument("--company", required=True, help="Company name (used in documents)")
    pa.add_argument("--email", default=DEFAULT_EMAIL,
                    help=f"Privacy contact email (default: {DEFAULT_EMAIL})")
    pa.add_argument("--frameworks", nargs="+", default=["GDPR", "SOC 2"],
                    help="Frameworks to assess (default: GDPR SOC 2)")
    pa.add_argument("--output", default=DEFAULT_OUT,
                    help=f"Output directory (default: {DEFAULT_OUT})")
    pa.add_argument("--pdf", action="store_true",
                    help="Also generate PDF versions of all documents")
    pa.set_defaults(func=cmd_assess)

    pd = sub.add_parser("docs", help="Generate compliance document templates only")
    pd.add_argument("--company", required=True, help="Company name (used in documents)")
    pd.add_argument("--email", default=DEFAULT_EMAIL,
                    help=f"Privacy contact email (default: {DEFAULT_EMAIL})")
    pd.add_argument("--output", default=DEFAULT_OUT,
                    help=f"Output directory (default: {DEFAULT_OUT})")
    pd.add_argument("--pdf", action="store_true",
                    help="Also generate PDF versions of all documents")
    pd.set_defaults(func=cmd_docs)

    pl = sub.add_parser("controls", help="List all compliance controls and question counts")
    pl.add_argument("--framework", nargs="*", default=None, help="Filter by framework")
    pl.set_defaults(func=cmd_list)

    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
