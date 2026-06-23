---
name: sprite-skill
description: >-
  Tailor a one-page, ATS-clean resume to a specific job description and pair it with a humanized,
  company-specific cover letter, exported as a single 2-page PDF (cover letter on page 1, resume on
  page 2, under 2 MB). Use this skill whenever the user wants to tailor / customize / optimize a
  resume or CV to a job posting or JD, build a strict one-page resume, write or tailor a cover
  letter, make a resume ATS-friendly, rewrite resume bullets to be results-oriented with quantified
  money/time impact, or generate job-application materials for a role -- even if they do not say
  "sprite-skill". It enforces the structure rules (education above experience, software as its own
  section, exactly three bullets per role), the one-page hard limit, and final PDF assembly.
---

# sprite-skill

Turn a candidate's true career history into a tailored, one-page, ATS-clean resume for a specific
job, plus a sincere cover letter, assembled into one polished PDF. The skill is a small rendering
engine (deterministic Python) wrapped around a strong methodology (how to select and reword content
per JD without ever fabricating).

**Separation of concerns:** the candidate's real content lives in `candidate.py` (you create it from
`assets/candidate.example.py`; it is git-ignored so personal data never enters the repo). The public
code only contains the engine, the method, and a fictional example.

## Setup (once)

1. Dependencies: `pip install python-docx PyMuPDF` and either **Microsoft Word** (Windows, best
   `.docx` fidelity) or **LibreOffice** (`soffice` on PATH, cross-platform) for PDF export.
2. Copy `assets/candidate.example.py` to the repo root as `candidate.py` and replace every value with
   the candidate's real, verifiable facts. Read the docstring at the top -- it states the schema and
   the bullet rules. Copy `assets/cover_letter_*.example.md` to `cover_letter_*.md` and adapt.

## The workflow

Per job description, follow `references/playbook.md`. The short version:

1. Read the JD; pick the matching variant in `candidate.py` (e.g. `DM`, `PM`) or add one.
2. Extract 15-20 JD keywords; rewrite the variant's `summary` and `competencies` toward them.
3. **Tailor the work experience to THIS JD -- the step that matters most.** For each role, pick the
   **exactly 3** bullets from that role's `BULLET_BANK` that best match what this job asks for, and
   reframe them in the JD's language (true facts only, money/time framed). Lead each role with the
   achievement the JD cares most about. The variant's default `bullets` are only a starting point.
4. Decide soft-skill weighting (people-facing role -> keep Volunteer/Additional; low-touch role ->
   `--drop-soft`).
5. Tailor the cover letter, then **run the `humanizer` skill on it** to strip AI tells. The cover
   letter ships on EVERY job (including big batches) -- do not drop it to save effort; resume-only
   is an explicit user opt-in, never your own default (guardrail 9).
6. Build, verify one page, assemble the 2-page PDF (cover letter p1 + resume p2), compress to <= 2 MB.
7. Look at the result with `preview.py` before declaring done.

> **The cardinal mistake: identical work experience across jobs.** Work experience is the section
> recruiters read most. If you only rewrite the summary and competencies and reuse the same bullets
> everywhere, the resume is not tailored -- it just looks tailored at the top. The `BULLET_BANK`
> exists precisely so the experience section changes per JD. When generating for **many** jobs,
> tailor each one's bullets individually; never let one bullet set get stamped across an archetype.

Always read `references/guardrails.md` before editing content -- the hard rules (never fabricate,
one page, ATS-clean, structure order, 3-bullets-per-role / 2-for-volunteer, results-first,
honest credit) are what make the output trustworthy and effective. `references/action_verbs.md`
is the verb palette for bullet openers.

## Scripts

Run from the repo root. They auto-load `candidate.py` from the root (override with `--candidate`).

```bash
# Final deliverable: cover letter (p1) + tailored resume (p2), verified one page, <= 2 MB
python scripts/assemble.py --variant DM --letter cover_letter_DM.md

# Resume-only PDF (some ATS prefer no cover-letter page)
python scripts/assemble.py --variant PM --no-letter

# Low-touch / non-people-facing role: drop Volunteer + Additional for more experience room
python scripts/assemble.py --variant PM --drop-soft --letter cover_letter_PM.md

# Visual QA -- render each page to PNG and actually look at it
python scripts/preview.py out/Jane_Doe_DM.pdf
```

`assemble.py` prints the page count and final size. **One page is a hard rule** -- if it reports
OVERFLOW, fix content or tune `line_spacing` in `candidate.py` and re-run. The line-spacing ->
page-count relationship is not linear, so adjust in small steps and re-measure (this is why the
script always reports the real page count instead of trusting a word-count estimate).

## What good looks like

```
[ Cover letter -- page 1 ]   sincere, company-specific, humanized, [Company]/[Role] filled in
[ Resume -- page 2 ]
  NAME  ·  phone | email | LinkedIn | GitHub | portfolio
  PROFESSIONAL SUMMARY        3-4 keyword-dense lines
  CORE COMPETENCIES           6-8 hard-skill / domain phrases
  SOFTWARE                    its own section (software is a hard skill)
  EDUCATION                   above experience
  PROFESSIONAL EXPERIENCE     each role: exactly 3 results-first bullets (money/time framed)
  VOLUNTEER & CULTURAL ENGAGEMENT   exactly 2 bullets (unique, trait-revealing)
  ADDITIONAL INFORMATION      brands (optional) | languages | hobbies (me-exclusive, true)
```

## Files

- `scripts/resume_lib.py` -- rendering engine (resume + cover letter) and `candidate.py` loader.
- `scripts/assemble.py` -- build -> export -> verify one page -> merge -> compress.
- `scripts/preview.py` -- render PDF pages to PNG for visual QA.
- `references/playbook.md` -- per-JD tailoring method.
- `references/guardrails.md` -- the hard rules and why they exist.
- `references/action_verbs.md` -- verb palette.
- `assets/candidate.example.py`, `assets/cover_letter_*.example.md` -- fictional templates to copy.
