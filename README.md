# sprite-skill

**Version 1.1.0** &middot; MIT licensed &middot; see [CHANGELOG.md](CHANGELOG.md) for release history.

A Claude skill for tailoring a **one-page, ATS-clean resume** to a specific job description and
pairing it with a **humanized, company-specific cover letter**, exported as a single 2-page PDF
(cover letter on page 1, resume on page 2, under 2 MB).

It is a small, deterministic rendering engine (`python-docx` + `PyMuPDF`) wrapped around an
opinionated methodology: how to select and reword a candidate's *true* history per JD, enforce a
strict one page, and keep everything ATS-parseable. The opinions come from a working
resume-tailoring practice and are documented in `references/`.

## Design

Your real content is **never** in this repo. It lives in a git-ignored `candidate.py` that you
create from `assets/candidate.example.py`. The public code ships only the engine, the method, and a
fictional "Jane Doe" example, so the skill is safe to publish and reuse by anyone.

## What it enforces

- One page, hard (verified by the real renderer, not guessed).
- Structure: Summary -> Core Competencies -> **Software (own section)** -> **Education (above
  experience)** -> Experience -> Volunteer -> Additional.
- Exactly **3 bullets per role** (volunteer is the deliberate 2-bullet exception).
- Results-first bullets framed in **money and time** (hours saved, % efficiency, revenue), led by
  strong action verbs.
- ATS-clean ASCII; no images/tables/columns.
- A cover letter on page 1, de-AI'd via the companion `humanizer` skill.
- Never fabricates -- only rewords true facts (derived numbers must be honest).

## Quick start

```bash
pip install python-docx PyMuPDF          # + Microsoft Word (Windows) or LibreOffice for PDF export
cp assets/candidate.example.py candidate.py        # then edit candidate.py with your real facts
cp assets/cover_letter_DM.example.md cover_letter_DM.md

python scripts/assemble.py --variant DM --letter cover_letter_DM.md
python scripts/preview.py out/*.pdf      # look at it
```

See `SKILL.md` for the full workflow and `references/` for the method and the rules.

## Requirements

- Python 3.9+, `python-docx`, `PyMuPDF`
- A PDF exporter: Microsoft Word (Windows, via `pywin32`) **or** LibreOffice (`soffice` on PATH)
- The `humanizer` skill (companion) for de-AI-ing cover letters

## Validation

The skill ships with an eval suite (`evals/evals.json`) that stress-tests the hard rules on
realistic prompts. It covers three jobs (DM growth, PM internal-tools, and an analyst request that
is deliberately *resume-only* -- which verifies the cover-letter-first default still honors an
explicit opt-out), 10 objective assertions each (30 total): a 2-page cover-letter-first PDF, a
one-page resume, education above experience, Software as its own section, exactly 3 bullets per
role, money/time quantification, ATS-clean ASCII, and no fabricated facts.

Re-run against the current version (**v1.1.0**):

| Configuration | Assertions passed | Pass rate |
|---------------|-------------------|-----------|
| With skill    | 30 / 30           | **100%**  |
| No skill (same prompts) | 22 / 30 | 73%       |

The no-skill baseline reliably misses the structural rules the skill enforces -- education above
experience, a dedicated Software section, and ATS-clean ASCII are the consistent failures. An
earlier run on the initial release (v1.0.0) scored 97% with-skill vs 77% baseline. Two of the ten
assertions (bullet-count, no-fabrication) are graded heuristically; the other eight are exact.
Re-run the suite yourself with the `skill-creator` eval workflow against `evals/evals.json`.

The skill has also been exercised across hundreds of real job descriptions in batch, with every
deliverable programmatically verified for the one-page rule, the 2-page structure, and ATS-clean
ASCII.

## License

MIT -- see `LICENSE`.
