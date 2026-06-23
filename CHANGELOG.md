# Changelog

All notable changes to sprite-skill are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-06-24

### Changed
- **Cover-letter-first is now the enforced default deliverable.** Every job ships a 2-page PDF
  (cover letter on page 1, resume on page 2); `--no-letter` / `--resume-only` is an explicit
  user opt-in, never a default the skill may choose on its own. Hardened in guardrail 9 and the
  SKILL.md workflow after a batch was mistakenly shipped resume-only.

### Added
- Version metadata (`version:` in SKILL.md frontmatter), this changelog, and a Validation section
  in the README documenting the eval benchmark.

## [1.0.0] - 2026-06-22

### Added
- Initial public release: a deterministic one-page resume + cover-letter rendering engine
  (`python-docx` + `PyMuPDF`), candidate-agnostic with a git-ignored `candidate.py` so no personal
  data enters the repo.
- Per-JD work-experience tailoring via a real `BULLET_BANK` per role: re-pick and reframe the 3
  bullets per role for each job, instead of stamping one bullet set across an archetype.
- Hard rules: one page (verified by the real renderer), education above experience, Software as its
  own section, exactly 3 bullets per role, results-first money/time framing, ATS-clean ASCII, and
  no fabrication.
- Eval suite (`evals/evals.json`) and the iteration-1 benchmark: 97% with-skill vs 77% baseline.
