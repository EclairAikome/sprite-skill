# sprite-skill

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

## License

MIT -- see `LICENSE`.
