# Design: City of Utopia — Knowledge Base for Civic Regulations

## Overview

`civic_info_agent` currently answers from ~20 lines of contact facts hardcoded
in its instructions. This change adds a knowledge base named `city_regulations`
containing three plain-text documents written for residents of the City of
Utopia. The agent keeps all existing facts and instructions and gains the
ability to search the knowledge base for any question about a rule, a
procedure, a fee, or a deadline.

**Scope**
- Three new source documents (`.txt`) in `knowledge-bases/`
- One new knowledge base definition (`knowledge-bases/city_regulations.yaml`)
- Updated `agents/civic_info_agent.yaml` — KB attached, instructions extended
- Updated `scripts/import-all.sh` and `scripts/delete-all.sh`

**Out of scope**
- `chat_with_docs` stays disabled
- No new tools, flows, or connections
- No changes to the agent's existing department facts or contact details

---

## Sub-Task 1 — Write the three source documents

**Intent**  
Produce the three plain-text handout files that the knowledge base will index.
Each file must contain every rule supplied by the user, written as a
plain-language resident handout with short labelled sections and no Markdown.

**Expected outcomes**
- `knowledge-bases/building_permit_guide.txt` exists and covers: when a permit
  is required (including the 10 m² / 2.5 m exemption), how to apply (online
  URL, site plan and drawings), fees (120 under 50 m², 300 at 50 m² or above),
  processing time (30 days), and the rule that work must not start before the
  decision.
- `knowledge-bases/waste_sorting_rules.txt` exists and covers: the four bins
  and what goes in each (green food/garden, blue paper/cardboard, yellow
  plastic/metal, grey general), glass bottles and jars to street containers,
  the special rule for broken mirrors/window glass/drinking glasses (grey bin
  wrapped), bulky item collection (online booking, up to 3 items, within 10
  working days, URL), and hazardous waste (paint/batteries/chemicals to 14 Mill
  Road recycling centre, Saturdays 08:00–13:00).
- `knowledge-bases/noise_ordinance.txt` exists and covers: quiet hours
  (22:00–07:00 Sun–Thu, 23:00–08:00 Fri–Sat), the audibility rule during quiet
  hours, construction hours (07:00–19:00 weekdays, 08:00–13:00 Saturdays,
  never Sundays), the one-night event exemption (online request at least 5 days
  in advance, URL), and how to report noise complaints (same URL).

**Todo**
1. Write `knowledge-bases/building_permit_guide.txt`
2. Write `knowledge-bases/waste_sorting_rules.txt`
3. Write `knowledge-bases/noise_ordinance.txt`

**Relevant context**
- All rule content comes from the user's prompt of 2025 (reproduced in full
  in the conversation). Do not invent additional rules.
- Format: plain text, no Markdown, short labelled sections (all-caps headings
  are fine), readable as a standalone printed handout.

**Status** `[x] done`

---

## Sub-Task 2 — Write the knowledge base definition

**Intent**  
Define the `city_regulations` knowledge base as a wxO resource YAML so it can
be imported with `orchestrate knowledge-bases import`.

**Expected outcomes**
- `knowledge-bases/city_regulations.yaml` exists with:
  - `spec_version: v1`
  - `kind: knowledge_base`
  - `name: city_regulations`
  - A description that tells the agent what topics the KB covers, so the agent
    can decide when to search it.
  - `files:` list referencing the three `.txt` documents by relative path.
- The file is valid wxO KB YAML (built-in Milvus, no external provider block
  needed).

**Todo**
1. Write `knowledge-bases/city_regulations.yaml`

**Relevant context**
- Built-in Milvus is the default; no `provider:` block is needed.
- `files:` paths should be relative to the project root or to the YAML file
  itself — use whatever the `orchestrate knowledge-bases import` CLI accepts
  (check `references/connections-models-kb.md §3` if uncertain).

**Status** `[x] done`

---

## Sub-Task 3 — Import the knowledge base and wait for ready

**Intent**  
Import the KB into the active wxO instance and confirm it has finished indexing
before touching the agent. An agent that references a KB that is not yet ready
will fail to search it.

**Expected outcomes**
- `orchestrate knowledge-bases import -f knowledge-bases/city_regulations.yaml`
  completes without error.
- `orchestrate knowledge-bases status -n city_regulations` returns `ready`.

**Todo**
1. Run `orchestrate knowledge-bases import -f knowledge-bases/city_regulations.yaml`
2. Poll `orchestrate knowledge-bases status -n city_regulations` until status
   is `ready` (check every 30 s; give up with an error after 10 minutes).

**Relevant context**
- Indexing three small text files typically takes 1–3 minutes on a SaaS tenant.
- Do not proceed to Sub-Task 4 until status is `ready`.

**Status** `[x] done`

---

## Sub-Task 4 — Update the agent

**Intent**  
Attach the KB to `civic_info_agent` and extend its instructions so it searches
the KB for regulation questions, names the source document in every KB-based
answer, and says it does not have the information when the KB returns nothing
relevant.

**Expected outcomes**
- `agents/civic_info_agent.yaml` has `knowledge_base: [city_regulations]`.
- The instructions retain every existing fact and rule unchanged (department
  contacts, response length for contact-only answers, scope/boundary rules).
- The instructions add a new section that says:
  - For any question about a rule, a procedure, a fee, or a deadline, search
    `city_regulations` first and answer from the document.
  - Every answer taken from a document must name the document (e.g. "According
    to the Building Permit Guide, …").
  - An answer taken from a document may be up to a short paragraph; it still
    ends with the relevant department's contact details when a department is
    involved.
  - When a question is about a rule or procedure that the documents do not
    cover, state clearly that you do not have that information and do not
    speculate.
- `orchestrate agents import -f agents/civic_info_agent.yaml` completes without
  error and the updated agent is visible in draft on the instance.

**Todo**
1. Edit `agents/civic_info_agent.yaml`:
   a. Set `knowledge_base: [city_regulations]`
   b. Add the KB search instructions section described above, after the existing
      Verified Facts block and before the Response Rules block (or at the end of
      the instructions — wherever it reads naturally).
2. Run `orchestrate agents import -f agents/civic_info_agent.yaml`

**Relevant context**
- Existing instructions to keep verbatim: all three department fact blocks,
  the Response Rules (length, tone, contact info, language, scope/boundaries).
- The "exactly two or three sentences" length rule applies to contact-fact
  answers only; KB-sourced answers may be longer (up to a short paragraph).
  Make this distinction explicit in the instructions.

**Status** `[x] done`

---

## Sub-Task 5 — Update scripts and test

**Intent**  
Keep `import-all.sh` and `delete-all.sh` in sync with the new KB resource, and
verify the agent answers the key resident questions correctly.

**Expected outcomes**

`scripts/import-all.sh` runs cleanly end-to-end with this order:
```
orchestrate knowledge-bases import -f knowledge-bases/city_regulations.yaml
# wait for ready
orchestrate agents import -f agents/civic_info_agent.yaml
```

`scripts/delete-all.sh` removes resources in reverse order:
```
orchestrate agents remove -n civic_info_agent --kind native || true
orchestrate knowledge-bases remove -n city_regulations || true
```

The agent passes all five test questions:

| # | Question | Expected answer (key content) | Source document |
|---|---|---|---|
| 1 | "Do I need a permit for a garden shed of 8 square metres?" | No permit needed — under 10 m² and (assumed) under 2.5 m | Building Permit Guide |
| 2 | "Which bin does a broken mirror go in?" | Wrap it and put it in the grey bin — broken mirrors are not accepted as glass | Waste Sorting Rules |
| 3 | "How loud can a party be after 10 pm on a Saturday?" | Must not be audible outside the property after 23:00 on Saturday; a one-night exemption can be requested 5 days in advance at the given URL | Noise Ordinance |
| 4 | "I want to build a 60 square metre extension. What does it cost, and who do I call?" | Fee is 300 (50 m² or above); contact Permits and Planning: 555 0110 / permits@utopia.example | Building Permit Guide |
| 5 | "Can I keep chickens in my garden?" | Agent says it does not have that information (not covered by any document) | — |

**Todo**
1. Update `scripts/import-all.sh` to import the KB before the agent and add a
   status-wait step.
2. Update `scripts/delete-all.sh` to remove the KB after the agent.
3. Run the five test questions via `chat_with_agent` (MCP tool) and record pass
   / fail for each.
4. Write `tests/TEST_REPORT.md` with results.

**Relevant context**
- Use `mcp__watsonx-orchestrate-adk__chat_with_agent` with
  `include_reasoning: true` for the first question; use the returned
  `thread_id` for question 4 to verify multi-turn context.
- Question 5 is the boundary test: the agent must not speculate or invent rules
  about keeping animals.

**Status** `[x] done`
