# -*- coding: utf-8 -*-
"""sprite-skill candidate profile -- EXAMPLE (fictional Jane Doe).

Copy this file to the repo root as `candidate.py` and replace every value with YOUR real,
verifiable content. candidate.py is git-ignored so your personal data never enters the
public repo.

>>> EVERYTHING BELOW IS FICTIONAL. Do NOT copy any number, employer, or specific from this
    example into your real candidate.py. "32% in two quarters", "across 3 user-tested
    iterations", "won two accounts" -- these are invented for Jane Doe. Copying them onto a
    real resume is fabrication, which is the one unforgivable error here (guardrail 1). Reword
    only facts that are true for the real person.

SCHEMA + RULES (see references/guardrails.md for the why):
  IDENTITY     - name, phone, email, links[(label,url)]. No street address / city.
  EDUCATION    - list of (school, degree+GPA, dates, coursework). Renders ABOVE experience.
  EXPERIENCES  - list of (role, org, dates) in recency order.
  BULLET_BANK  - per experience (keyed by index), the FULL set of true achievements you could
                 cite -- more than 3, covering different angles (data, growth, content,
                 stakeholder, delivery). This is the heart of tailoring: per JD you pick the 3
                 that match THAT job and reframe them. One skill per bullet.
  VARIANTS[k]  - per target archetype (e.g. DM = marketing, PM = product). Each has:
                   summary        - 3-4 lines, JD-keyword dense
                   competencies   - 6-8 hard-skill / domain phrases
                   software       - its OWN section; pipe-separated tools
                   brands         - optional endorsement line, or None
                   bullets        - the DEFAULT 3-per-role selection from BULLET_BANK. This is a
                                    STARTING POINT, not a finished resume. ** For each new job you
                                    MUST re-pick and reframe these 3 bullets per role from the bank
                                    to match the specific JD. ** Shipping the same bullets across
                                    different target jobs is the #1 tailoring failure -- work
                                    experience is the section recruiters read most, so it has to
                                    change per job, not just the summary and competencies.
                   line_spacing   - fill the page without overflowing (tune per variant)
  VOLUNTEER    - (role, org, dates, [EXACTLY 2 bullets]). The 2-bullet count is a deliberate
                 exception to the 3-bullet rule (which governs experience only).
  LANGUAGES / HOBBIES - Additional Information. Hobbies are for UNIQUE, "me-exclusive" traits
                 that reveal who you are; keep them true.

Bullet craft: lead with a strong action verb, put the quantifiable result in the FIRST half,
and frame results in the two things employers care about most -- MONEY and TIME (hours saved,
% efficiency, revenue, cost). "Cut reporting time ~80%" beats "improved reporting".
"""

IDENTITY = dict(
    name="JANE DOE",
    phone="+65 0000 0000",
    email="jane.doe@example.com",
    links=[
        ("LinkedIn", "https://www.linkedin.com/in/janedoe-example"),
        ("GitHub", "https://github.com/janedoe-example"),
        ("janedoe.example.com", "https://janedoe.example.com"),
    ],
)

EDUCATION = [
    ("National University of Example", "BBA, Marketing  (GPA 3.8/4.0)", "2020 - 2024",
     "Relevant coursework: Marketing Analytics, Consumer Behavior, Data Visualization"),
]

EXPERIENCES = [
    ("Growth Marketing Associate", "Acme Retail, Singapore", "2024 - Present"),
    ("Marketing Intern", "Globex Media, Remote", "2023 - 2024"),
    ("Brand Assistant", "Initech Agency, Singapore", "2022 - 2023"),
]

# The proof bank: every TRUE achievement per role, more than the 3 you will show. Per JD, pick the
# 3 that hit what THAT job asks for and reframe the wording in the JD's language. Keep one skill per
# bullet, result-first, money/time framed. (All fictional here -- replace with your real wins.)
BULLET_BANK = {
    0: [  # Acme Retail
        "Cut weekly reporting time ~80% (from ~10 hours to ~2) by automating a campaign-performance dashboard across 5 ad channels.",
        "Grew email-driven revenue 32% in two quarters by rebuilding the lifecycle flows around cohort and A/B-test data.",
        "Lifted paid-channel ROAS ~20% by reallocating spend toward the best-performing segments surfaced in the dashboard.",
        "Shipped a 6-person cross-functional launch on schedule by coordinating creative, legal, and ops end to end.",
        "Defined the dashboard's success metrics and a reusable reporting spec the wider team adopted.",
    ],
    1: [  # Globex Media
        "Lifted organic social engagement ~3x (from ~1.5% to ~4.5%) by rebuilding the content calendar around top-performing formats.",
        "Saved the team ~5 hours a week by templating the influencer-outreach workflow in a shared tracker.",
        "Compiled a positioning brief from 20+ competitor campaigns that anchored the Q3 plan.",
        "Grew the newsletter list ~40% by launching a lead-magnet series tied to the top-read blog topics.",
    ],
    2: [  # Initech Agency
        "Delivered 12 client campaigns with 100% on-time delivery by owning the production schedule end to end.",
        "Cut creative revision cycles ~40% by introducing a single-source brief template.",
        "Supported new-business pitches with audience research that helped win two accounts.",
        "Coordinated creative, legal, and vendor partners across overlapping deadlines without slipping a launch.",
    ],
}

LANGUAGES = "English (Native)  |  Mandarin (Professional)  |  Spanish (Conversational)"
HOBBIES = "Trail running (2 marathons)  |  Film photography  |  Competitive bouldering  |  Jazz piano"

VOLUNTEER = (
    "Student Outreach Lead", "University Marketing Club", "2021 - 2023",
    [
        "Built a 150-member community by running monthly events and a weekly newsletter across two academic years.",
        "Mentored 8 juniors into their first internships through a peer-review program.",
    ],
)

VARIANTS = {
    # Digital Marketing archetype. `bullets` = a DEFAULT pick from BULLET_BANK; RE-PICK per JD.
    "DM": dict(
        line_spacing=0.97,
        summary=("Data-driven growth marketer focused on lifecycle, performance analysis, and "
                 "content that compounds. At Acme Retail, automated reporting and rebuilt email "
                 "flows that grew revenue; earlier ran social and competitor research at Globex "
                 "and delivered agency campaigns at Initech. Comfortable turning messy channel "
                 "data into decisions."),
        competencies=["Growth Marketing", "Lifecycle & Email", "Performance Analysis & Reporting",
                      "Campaign Strategy & Execution", "Content Strategy", "A/B Testing & Experimentation",
                      "Marketing Analytics (SQL/Sheets)", "Cross-Functional Collaboration"],
        software="Google Analytics  |  Meta Business Suite  |  HubSpot  |  Looker Studio  |  SQL  |  Python (data analysis)  |  Canva  |  Figma  |  Microsoft Office",
        brands="Northwind  |  Contoso  |  Fabrikam",
        bullets=[
            [BULLET_BANK[0][0], BULLET_BANK[0][1], BULLET_BANK[0][3]],   # Acme: data, lifecycle, launch
            [BULLET_BANK[1][0], BULLET_BANK[1][1], BULLET_BANK[1][2]],   # Globex: social, process, research
            [BULLET_BANK[2][0], BULLET_BANK[2][1], BULLET_BANK[2][2]],   # Initech: delivery, process, pitches
        ],
    ),
    # Product Manager archetype. Same person, product lens; RE-PICK bullets per JD.
    "PM": dict(
        line_spacing=1.02,
        summary=("Product-minded builder who turns recurring pain points into tools the team keeps "
                 "using. At Acme Retail, owned an analytics dashboard from problem to launch and "
                 "defined its success metrics; earlier prototyped workflow automation at Globex and "
                 "ran delivery for an agency at Initech."),
        competencies=["End-to-End Product Ownership", "Problem Definition & Requirements",
                      "Product Metrics & Success Criteria", "Process Automation & Internal Tooling",
                      "Data Analysis (SQL/Python)", "Prototyping & Iteration",
                      "Cross-Functional Coordination", "Documentation & Adoption"],
        software="SQL  |  Python (data analysis)  |  Looker Studio  |  Figma  |  Notion  |  Jira  |  Google Analytics  |  Microsoft Office",
        brands=None,
        bullets=[
            [BULLET_BANK[0][4], BULLET_BANK[0][0], BULLET_BANK[0][3]],   # Acme: metrics/spec, automation, launch
            [BULLET_BANK[1][1], BULLET_BANK[1][2], BULLET_BANK[1][0]],   # Globex: process, research, social
            [BULLET_BANK[2][0], BULLET_BANK[2][1], BULLET_BANK[2][3]],   # Initech: delivery, process, stakeholder
        ],
    ),
}
