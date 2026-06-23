# Guardrails

These are the non-negotiables. Each one has a reason; understanding the reason matters more
than memorizing the rule, because real JDs throw edge cases the rules never anticipated.

## 1. Never fabricate
Only reword facts that are true for this candidate. Do not invent skills, employers, titles,
or numbers. If a number is unknown, leave it out -- do not guess a plausible-looking one.
Derived numbers are fine when the math is honest: "~93% less time per item" is a legitimate
restatement of "15x output at the same effort" (1 - 1/15 ≈ 0.93). A made-up "1500%" is not.
*Why:* a resume that cannot survive an interview is worse than a modest true one. Trust is the
whole game.

## 2. One page, hard
The resume body is exactly one page. `assemble.py` reports the page count from the real renderer
(Word, or LibreOffice) -- trust that number, not your eyeballing. If it overflows, fix it by
trimming wordy bullets or adjusting `line_spacing` in `candidate.py`, then re-run.
*Note:* the line-spacing -> page-count relationship is NOT linear. A 0.03 bump can flip a full
page to two. Iterate in small steps and re-measure; do not assume.
*Why:* for early-career and most IC roles, two pages signals an inability to prioritize, and many
recruiters only read page one anyway.

## 3. Fill the page, but never exceed it
Aim for a page that reads full top-to-bottom -- a half-empty page looks thin. Fill with real
content first (a richer bullet, the volunteer section), then with modest `line_spacing`. Do not
pad with fluff or fabricate to fill space. A near-full page with a small bottom margin is fine.

## 4. ATS-clean formatting
Single column. Standard section titles (Professional Summary, Core Competencies, Software,
Education, Professional Experience, ...). ASCII punctuation: use "-", never em/en dashes or curly
quotes. No images, no tables, no multi-column layouts, no text boxes.
*Exception:* diacritics inside real proper nouns (e.g. "Estée Lauder") are correct and stay.
*Why:* applicant tracking systems parse plain linear text; anything fancy gets garbled or dropped.

## 5. Structure order
Summary -> Core Competencies -> Software (its OWN section) -> Education (ABOVE experience) ->
Professional Experience -> Volunteer & Cultural Engagement -> Additional Information.
*Why this order:* competencies + software give a recruiter the hard-skill scan in the first two
seconds; software is hard skill, so it earns its own section rather than hiding in "Additional".
Education above experience suits students/early-career; for senior candidates you may flip it.

## 6. Bullet counts -- and tailor those bullets to EACH JD
Each experience: EXACTLY 3 bullets, one skill per bullet. Volunteer: EXACTLY 2 bullets (a
deliberate exception -- volunteer exists to show traits, not to compete with real work).
*Why three:* it forces ruthless selection of your strongest, most relevant proof per role and keeps
the page scannable.

The harder half of this rule: **those 3 bullets must be re-chosen per JD.** Work experience is the
section a recruiter reads most closely, so keeping a true `BULLET_BANK` per role (more than 3) and
selecting/reframing the 3 that fit each specific job is the core of tailoring -- not an optional
polish. The failure mode to refuse: tailoring only the summary and competencies while the same
experience bullets ride along on every application. At batch scale especially, do the per-job
selection for each job; a stack of resumes with identical experience sections is not tailored work.

## 7. Results-first bullets: Competency + Action = Result, framed in money & time
Lead with a strong action verb (see action_verbs.md), put the quantifiable result in the FIRST
half of the bullet, and frame it in the two things employers care about most: MONEY and TIME
(hours saved, % efficiency, revenue, cost, on-time delivery). Prefer "Cut reporting time ~80%
(10h -> 2h) by automating ..." over "Responsible for reporting automation".
*Why:* readers skim the start of each line; money and time are the universal language of impact.

## 8. Soft-skill weighting depends on the role
The more a role is about people (sales is the archetype: partnerships, account management,
community, customer success), the more soft skills matter -- keep Volunteer + Additional and let
some bullets lead with collaboration, communication, and stakeholder work. The less a role touches
people (e.g. backend engineering, research), the less soft skills matter -- it is fine to drop
Volunteer + Additional (`assemble.py --drop-soft`) and spend that space on deeper technical
experience. Read the JD and decide.

## 9. The deliverable leads with a cover letter (this is the DEFAULT, not an upsell)
Every deliverable PDF is two pages: page 1 a cover letter tailored to the company and role,
page 2 the one-page resume. The letter is sincere, shows concrete fit, and shows real enthusiasm
for THIS company. Draft it, then run it through the `humanizer` skill to strip AI tells (em
dashes, rule-of-three, inflated vocabulary). Keep `[Company]`/`[Role]` placeholders in the
template; fill them per application. Final PDF must be <= 2 MB (`assemble.py` compresses if needed).
*Why:* a generic letter reads as spam; a specific one signals you actually want this job.

**Do not drop the cover letter on your own.** The two-page, cover-letter-first PDF is the
standard deliverable for every job, including large batches. `--no-letter` / `--resume-only`
is an EXCEPTION you take only when the user explicitly asks for a bare resume, or a specific ATS
demands one. "It is a batch of hundreds" and "resume-only is faster / matches what we shipped
before" are NOT reasons to skip it. When tailoring many jobs, generate a per-job letter for each
(the company, the role, and the role's stated focus go in the opening; the body is the real
achievements). If you believe resume-only is warranted, ask the user first rather than deciding
it silently -- shipping a batch without letters when the user expected them is a real failure.

## 10. Honest credit + no confidential detail
If a metric belongs to a team or a campaign, attribute it that way ("Contributed to ...",
"the campaign drew 5M+ views"), never as your sole achievement. Only cite publicly attributable
work; never put NDA'd clients, unreleased products, or internal figures on a public document.

## 11. Header
Name + phone + email + professional links (LinkedIn, GitHub, portfolio). No street address.
Include city only when location is genuinely relevant to the application.
