# Tailoring playbook

How to turn one job description (JD) into one tailored, one-page resume (+ cover letter) for this
candidate. The candidate's true content lives in `candidate.py`; this file is the method for
selecting and rewording it per JD. Read `guardrails.md` alongside this.

## 0. The loop
1. Read the JD. Decide which archetype/variant fits (e.g. `DM` for marketing, `PM` for product).
   If none fits, add a new variant to `candidate.py` (same schema).
2. Extract 15-20 JD keywords: skills, tools, domain nouns, the verbs they use.
3. Rewrite the variant's `summary` to be keyword-dense and pointed at this JD (3-4 lines).
4. Choose 6-8 `competencies` from the role's pool, tilted toward the JD's language.
5. **Tailor the experience (the step that decides whether the resume is actually tailored).** For
   each role, pick the 3 bullets from its `BULLET_BANK` that best answer this JD and reframe them in
   the JD's vocabulary, leading with the achievement this job values most -- true facts only. The
   variant's default `bullets` are a starting point, not the answer. If two different jobs come out
   with the same experience section, you have not tailored it.
6. Apply money/time framing (guardrail 7) to the headline results.
7. Decide soft-skill weighting (guardrail 8): people-facing role -> keep Volunteer + Additional;
   low-touch role -> `--drop-soft`.
8. Tailor the cover letter to the company/role, then run the `humanizer` skill on it.
9. Build and verify: `python scripts/assemble.py --variant <V> --letter <letter.md>`. Confirm the
   resume is one page and the final PDF <= 2 MB.
10. QA visually: `python scripts/preview.py out/<file>.pdf`. Look at it -- fill, wrapping, header.

## 1. Picking / shaping the archetype
A variant is a lens, not a different person. Same facts, different framing and ordering. Typical
starting variants:
- **DM (Digital Marketing / growth / brand / performance / content):** narrative = data-driven
  marketer; software analytics-first; competencies around campaigns, performance, content, KOL.
- **PM (Product / strategy / internal tooling / AI):** narrative = builder who owns tools end to
  end; software technical-first; competencies around ownership, metrics, requirements, automation.
Other directions (data analyst, ops, partnerships) usually borrow from the nearest variant and
adjust the summary + competencies; keep the guardrails identical.

## 2. Keyword extraction
Pull the literal words the JD repeats and the tools it names. These become: the first 5 words of
the summary, the first bullet of the most relevant role, and the competencies/software lines.
ATS matching is largely literal -- mirror their nouns ("lifecycle marketing" vs your "email flows")
when both are true of you.

## 3. The proof bank (`BULLET_BANK` in candidate.py)
Each role keeps MORE true achievements than the 3 it will show -- that surplus is what makes
per-JD tailoring possible. Think of it as a map of "JD requirement -> true achievement that hits it
-> wording". Per job, pick the 3 per role that match; the rest stay in reserve for other jobs.
- data analysis / metrics -> the reporting-automation work -> "Cut reporting time ~80% ..."
- competitor research -> the competitor-teardown work -> "Compiled a positioning brief from 20+ ..."
- end-to-end ownership -> the internal-tool build -> "Owned ... from problem to launch"
- stakeholder / cross-functional -> launch coordination -> "Coordinated creative, legal, and ops ..."
Never add a row that isn't true.

## 3a. Scaling to many jobs (do not stamp one bullet set across an archetype)
When tailoring for a whole batch of jobs, the tempting shortcut is to tailor only the summary +
competencies and reuse the variant's default bullets for every job in that archetype. Do not. That
produces a stack of resumes whose experience sections are identical -- the opposite of tailored, and
the most visible tell to a recruiter who sees more than one. Tailor each job's 3-per-role selection
from the bank individually. If a batch is large, spend the effort per job (or per tight cluster);
the experience section is not where to cut corners.

## 4. Cover letter
Four short moves: (1) the role + why this company, with a specific hook; (2) your single strongest,
most relevant proof, framed in money/time; (3) one line of breadth + a human note; (4) a brief,
sincere close. Keep `[Company]`/`[Role]`/`[specific reason]` placeholders in the template and fill
them per application. Then run the `humanizer` skill -- cover letters are where AI tells (em dashes,
"exactly the kind of", rule-of-three) are most obvious and most damaging.

## 5. Build + verify (the mechanical part)
```
python scripts/assemble.py --variant DM --letter assets/cover_letter_DM.md
python scripts/assemble.py --variant PM --no-letter            # resume-only PDF
python scripts/assemble.py --variant PM --drop-soft            # low-touch role
python scripts/preview.py out/<name>_DM.pdf                    # eyeball every page
```
`assemble.py` renders the docx, exports via Word (or LibreOffice), checks the resume is one page,
merges letter+resume, and compresses to <= 2 MB. If it reports OVERFLOW, fix content or
`line_spacing` in `candidate.py` and re-run -- do not ship two pages.

## 6. Filling the page
If the page is thin, the best fix is richer real content (a fuller bullet, the volunteer section),
then small `line_spacing` increases. Because the spacing/page relationship is non-linear, change
`line_spacing` in steps of ~0.02 and re-measure. Different variants usually need different values
(a text-heavy variant fills at 0.97; a lighter one may want 1.02+).
