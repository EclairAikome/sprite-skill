# -*- coding: utf-8 -*-
"""sprite-skill adversarial verifier: check an assembled deliverable PDF against the hard rules.

Deterministic gate for batch work (see SKILL.md "Large batches"). Given a final 2-page PDF and,
optionally, the candidate module + variant key, it asserts every SKILL.md / guardrails.md hard rule
it can check mechanically and prints PASS or a list of FAILs. Use it on every PDF in a batch before
moving to the next batch.

CLI:
  python scripts/verify.py out/Resume.pdf --variant R1 --candidate candidate.py --company Garena

Importable:
  from verify import check
  errs, warns = check(pdf_path, variant="R1", candidate=mod, company="Garena", expect_letter=True)
"""
import os
import sys
import datetime

ALLOWED_TOOLS = [
    "SQL", "Python", "Git", "GitHub", "Claude Code", "AI agents", "Claude Design",
    "Canva", "Google Analytics", "Meta Business Suite", "Adobe", "Microsoft Office",
    "Excel", "Discord",
]
BAD_CHARS = {
    "—": "em-dash", "–": "en-dash",
    "‘": "curly-quote", "’": "curly-quote",
    "“": "curly-quote", "”": "curly-quote",
}
PLACEHOLDERS = ["[Company]", "[Role]", "[Date]", "[specific", "[One sentence", "Jane Doe", "Acme"]
SECTIONS = [
    "PROFESSIONAL SUMMARY", "CORE COMPETENCIES", "SOFTWARE", "EDUCATION",
    "PROFESSIONAL EXPERIENCE", "VOLUNTEER & CULTURAL ENGAGEMENT", "ADDITIONAL INFORMATION",
]


def load_candidate(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("candidate", os.path.abspath(path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def check(pdf, variant=None, candidate=None, company=None, expect_letter=True):
    import fitz
    errs, warns = [], []
    d = fitz.open(pdf); n = d.page_count
    txt = [p.get_text() for p in d]; d.close()
    full = "\n".join(txt)

    expected_pages = 2 if expect_letter else 1
    if n != expected_pages:
        errs.append("pages=%d (expected %d)" % (n, expected_pages))

    for ch, name in BAD_CHARS.items():
        if ch in full:
            errs.append("non-ASCII %s present (%r)" % (name, ch))
    for ph in PLACEHOLDERS:
        if ph in full:
            errs.append("leftover placeholder/example text: %s" % ph)

    resume_txt = txt[-1] if txt else ""
    if expect_letter:
        p1 = txt[0] if txt else ""
        if "Dear Hiring Manager" not in p1:
            errs.append("letter: missing 'Dear Hiring Manager'")
        if "Sincerely" not in p1:
            errs.append("letter: missing 'Sincerely'")
        if "Ji Li" not in p1:
            errs.append("letter: missing candidate name")
        today = datetime.date.today()
        dstr = "%d %s %d" % (today.day, today.strftime("%B"), today.year)
        if dstr not in p1:
            errs.append("letter: missing/incorrect date (expected '%s')" % dstr)
        if company:
            tok = company.split()[0]
            if tok.lower() not in p1.lower():
                warns.append("letter: company token %r not found in letter" % tok)

    last = -1
    for s in SECTIONS:
        i = resume_txt.find(s)
        if i < 0:
            errs.append("resume: missing section '%s'" % s)
        elif i < last:
            errs.append("resume: section out of order '%s'" % s)
        else:
            last = i

    mb = os.path.getsize(pdf) / (1024 * 1024)
    if mb > 2.0:
        errs.append("size %.2fMB > 2MB" % mb)

    if variant and candidate is not None:
        v = candidate.VARIANTS[variant]
        b = v["bullets"]
        if len(b) != 3:
            errs.append("variant %s: %d experience roles (expected 3)" % (variant, len(b)))
        for i, rb in enumerate(b):
            if len(rb) != 3:
                errs.append("variant %s: role %d has %d bullets (expected 3)" % (variant, i, len(rb)))
        c = v["competencies"]
        if not (6 <= len(c) <= 8):
            errs.append("variant %s: %d competencies (expected 6-8)" % (variant, len(c)))
        for tok in v["software"].split("|"):
            tok = tok.strip()
            if tok and not any(a in tok for a in ALLOWED_TOOLS):
                errs.append("variant %s: software token not in verified set: %r" % (variant, tok))
    return errs, warns


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--variant", default=None)
    ap.add_argument("--candidate", default=None)
    ap.add_argument("--company", default=None)
    ap.add_argument("--no-letter", action="store_true")
    a = ap.parse_args()
    cand = load_candidate(a.candidate) if a.candidate else None
    errs, warns = check(a.pdf, a.variant, cand, a.company, expect_letter=not a.no_letter)
    name = os.path.basename(a.pdf)
    for w in warns:
        print("  warn[%s]: %s" % (name, w))
    if errs:
        print("FAIL %s" % name)
        for e in errs:
            print("   - %s" % e)
        sys.exit(1)
    print("PASS %s" % name)


if __name__ == "__main__":
    main()
