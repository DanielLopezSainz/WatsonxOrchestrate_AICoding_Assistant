# Design: City Services Record Lookup Tools

## 1. Overview

This document describes the addition of three Python tools to `civic_info_agent` that allow residents to look up their own city service records. The agent previously answered only questions about rules, procedures, and department contacts. After this change it also retrieves the current status of a resident's building permit application, road problem report, or bin collection schedule.

The City of Utopia has no real backend systems. All records are held in CSV files that are packaged and uploaded with each tool.

---

## 2. Scope of Change

| Asset | Change |
|---|---|
| `tools/get_permit_status.py` | New — Python tool |
| `tools/permits.csv` | New — data file uploaded with the tool |
| `tools/get_request_status.py` | New — Python tool |
| `tools/requests.csv` | New — data file uploaded with the tool |
| `tools/get_collection_days.py` | New — Python tool |
| `tools/collection_calendar.csv` | New — data file uploaded with the tool |
| `agents/civic_info_agent.yaml` | Updated — tools list and instructions |
| `scripts/import-all.sh` | Updated — tool import steps added |
| `scripts/delete-all.sh` | Updated — tool removal steps added |

No other assets change. The `city_regulations` knowledge base and its documents are unchanged.

---

## 3. Record Types

### 3.1 Building Permit Applications

Looked up by permit number in the format `PP-YYYY-NNNN`.

| Field | Description |
|---|---|
| `permit_number` | Primary key, e.g. `PP-2026-0412` |
| `address` | Property address the application relates to |
| `work_type` | Brief description of the proposed work |
| `status` | `Under review` · `Approved` · `Additional documents requested` |
| `submitted` | Date the application was received (YYYY-MM-DD) |
| `decision_date` | Date of decision when `Approved`; due date for decisions not yet made; blank when not applicable |
| `notes` | Any outstanding action required of the applicant, or blank |

**Seed records (as provided):**

| Number | Address | Work type | Status | Submitted | Decision date | Notes |
|---|---|---|---|---|---|---|
| PP-2026-0412 | 18 Elm Street | garden shed 12 sqm | Under review | 2026-09-12 | 2026-10-12 | |
| PP-2026-0398 | 7 Harbour Lane | two-storey extension | Approved | 2026-08-20 | 2026-09-30 | |
| PP-2026-0433 | 42 Mill Road | garage | Additional documents requested | 2026-09-25 | 2026-10-25 | site plan missing |

**Invented records (status words restricted to those above):**

| Number | Address | Work type | Status | Submitted | Decision date | Notes |
|---|---|---|---|---|---|---|
| PP-2026-0445 | 3 Station Road | loft conversion | Under review | 2026-10-01 | 2026-10-31 | |
| PP-2026-0389 | 55 Oak Avenue | single-storey side extension | Approved | 2026-07-14 | 2026-08-13 | |
| PP-2026-0421 | 19 River Close | detached garden studio 18 sqm | Additional documents requested | 2026-09-18 | 2026-10-18 | elevation drawings missing |
| PP-2026-0460 | 8 Maple Drive | rear extension | Under review | 2026-10-07 | 2026-11-06 | |
| PP-2026-0374 | 101 High Street | outbuilding conversion to home office | Approved | 2026-06-30 | 2026-07-30 | |
| PP-2026-0438 | 27 Birch Lane | front porch | Additional documents requested | 2026-09-28 | 2026-10-28 | structural calculations missing |
| PP-2026-0415 | 14 Cedar Way | two-car garage | Approved | 2026-09-10 | 2026-10-10 | |

### 3.2 Road Problem Reports

Looked up by request number in the format `RQ-YYYY-NNNN`.

| Field | Description |
|---|---|
| `request_number` | Primary key, e.g. `RQ-2026-1187` |
| `street` | Street where the problem was reported |
| `problem_type` | `pothole` · `street light out` · `damaged sign` |
| `status` | `Received` · `Scheduled` · `Closed` |
| `scheduled_date` | Repair date when `Scheduled` (YYYY-MM-DD); blank otherwise |

**Seed records (as provided):**

| Number | Street | Problem | Status | Scheduled date |
|---|---|---|---|---|
| RQ-2026-1187 | Elm Street | pothole | Scheduled | 2026-10-09 |
| RQ-2026-1203 | Harbour Lane | street light out | Closed | |
| RQ-2026-1210 | Station Road | damaged sign | Received | |

**Invented records:**

| Number | Street | Problem | Status | Scheduled date |
|---|---|---|---|---|
| RQ-2026-1215 | Oak Avenue | pothole | Received | |
| RQ-2026-1199 | Station Road | street light out | Scheduled | 2026-10-14 |
| RQ-2026-1221 | Cedar Way | damaged sign | Closed | |
| RQ-2026-1228 | Maple Drive | pothole | Scheduled | 2026-10-16 |
| RQ-2026-1195 | High Street | street light out | Closed | |
| RQ-2026-1234 | River Close | pothole | Received | |
| RQ-2026-1241 | Birch Lane | damaged sign | Scheduled | 2026-10-20 |

### 3.3 Bin Collection Calendar

Looked up by street name (case-insensitive exact match).

The four bins are those defined in the Waste Sorting Rules: **grey** (residual), **green** (food and garden), **blue** (paper and cardboard), **yellow** (plastic and metal). Each street has one fixed collection day per bin type, the same every week.

**Seed records (as provided):**

| Street | Grey | Green | Blue | Yellow |
|---|---|---|---|---|
| Elm Street | Monday | Thursday | Wednesday | Wednesday |
| Harbour Lane | Tuesday | Friday | Wednesday | Wednesday |
| Mill Road | Monday | Thursday | Friday | Friday |

**Invented records:**

| Street | Grey | Green | Blue | Yellow |
|---|---|---|---|---|
| Station Road | Wednesday | Friday | Monday | Monday |
| Oak Avenue | Thursday | Tuesday | Friday | Friday |
| Cedar Way | Monday | Thursday | Wednesday | Wednesday |
| Maple Drive | Tuesday | Friday | Thursday | Thursday |
| High Street | Wednesday | Monday | Friday | Friday |
| River Close | Thursday | Tuesday | Monday | Monday |
| Birch Lane | Friday | Wednesday | Tuesday | Tuesday |

---

## 4. Tool Specifications

### 4.1 Packaging — how the CSV travels with the tool

Each tool reads its records from a CSV file kept in the same `tools/` directory as the `.py` file. The tool locates the file at runtime using a path relative to `__file__`, so the path is always correct regardless of where the tool is executed.

When importing a tool that needs supporting files, the ADK CLI `--package-root` flag is used. It causes the entire specified directory to be zipped and uploaded to the platform together with the tool file, so the CSV is available to the tool at the same relative path at runtime.

The import command for each tool therefore takes this form:

```bash
orchestrate tools import -k python \
  --file tools/<tool_file>.py \
  --package-root tools/
```

`--file` names the specific Python file that contains the `@tool` function. `--package-root` names the directory whose contents are packaged and uploaded — in this project, the `tools/` directory, which contains both the `.py` file and its companion CSV.

All three tools use this same command pattern.

### 4.2 `get_permit_status`

| Property | Value |
|---|---|
| File | `tools/get_permit_status.py` |
| Data file | `tools/permits.csv` |
| Permission | `READ_ONLY` |
| Input | `permit_number: str` — the application number, e.g. `PP-2026-0412` |
| Output | `PermitRecord` Pydantic model with all fields listed in §3.1 |
| Not-found signal | Returns a `PermitRecord` with `status = "NOT_FOUND"` and all other fields empty |
| Lookup key | Case-insensitive, trimmed match on `permit_number` |

### 4.3 `get_request_status`

| Property | Value |
|---|---|
| File | `tools/get_request_status.py` |
| Data file | `tools/requests.csv` |
| Permission | `READ_ONLY` |
| Input | `request_number: str` — the request number, e.g. `RQ-2026-1187` |
| Output | `RequestRecord` Pydantic model with all fields listed in §3.2 |
| Not-found signal | Returns a `RequestRecord` with `status = "NOT_FOUND"` and all other fields empty |
| Lookup key | Case-insensitive, trimmed match on `request_number` |

### 4.4 `get_collection_days`

| Property | Value |
|---|---|
| File | `tools/get_collection_days.py` |
| Data file | `tools/collection_calendar.csv` |
| Permission | `READ_ONLY` |
| Input | `street_name: str` — the street name, e.g. `Elm Street` |
| Output | `CollectionDays` Pydantic model with all fields listed in §3.3 |
| Not-found signal | Returns a `CollectionDays` where all day fields equal `"NOT_FOUND"` |
| Lookup key | Case-insensitive, trimmed exact match on street name |

---

## 5. Agent Behaviour Rules

These rules replace the former rule "Do not look anything up in other systems and do not create requests or tickets" (previously §4, Response Rules of `civic-info-design.md`). All other existing rules remain in force.

### 5.1 When to call a tool

| Trigger | Tool to call |
|---|---|
| Resident mentions a permit number (`PP-YYYY-NNNN`) | `get_permit_status` |
| Resident mentions a request number (`RQ-YYYY-NNNN`) | `get_request_status` |
| Resident asks about collection days for a named street | `get_collection_days` |

### 5.2 Missing identifier

If the question clearly requires a tool but the resident has not provided the permit number, request number, or street name, the agent asks for it before calling the tool. The agent does not guess or proceed without the identifier.

### 5.3 Not-found response

When a tool returns `status = "NOT_FOUND"` (permits and reports) or all day fields equal `"NOT_FOUND"` (collection calendar), the agent replies:

> "I have no record under that reference. Please check the number and try again."

The reply ends with the contact details of the relevant department:
- Permit not found → Permits and Planning: 555 0110 · permits@utopia.example
- Report not found → Roads and Infrastructure: 555 0120 · roads@utopia.example
- Street not found → Waste and Recycling: 555 0130 · waste@utopia.example

### 5.4 Authorisation

The agent does not check who is asking. Any resident who provides a valid number or street name receives the record. No authentication is performed.

### 5.5 Combined questions

A question may need both a tool and the knowledge base (for example: "My permit is under review — how long does a decision take?"). The agent uses both sources in the same answer.

### 5.6 Answer length and format for tool-sourced answers

Answers drawn from a tool follow the same rule as answers from the department facts: at most three sentences, ending with the relevant department's contact details.

---

## 6. Agent YAML Changes

### 6.1 `tools` list

```yaml
tools:
  - get_permit_status
  - get_request_status
  - get_collection_days
```

### 6.2 Instructions — new section

A new section titled `### Tools: Record Lookups` is added to the instructions after the `### Knowledge Base: City Regulations` section and before `### Response Rules`. It contains:
- Which tool to call for which kind of question (§5.1)
- The ask-before-calling rule (§5.2)
- The not-found reply pattern with per-department contacts (§5.3)
- The no-authorisation rule (§5.4)
- The combined-question rule (§5.5)
- The answer-length rule for tool answers (§5.6)

### 6.3 Instructions — updated rule

The sentence "Do not look anything up in other systems and do not create requests or tickets" is removed from `### Response Rules` and replaced by: "Do not create requests or tickets and do not access any systems other than the tools provided."

### 6.4 New starter prompts

Two additional starter prompts are added:

```yaml
- id: default2
  title: Check permit application status
  subtitle: ''
  prompt: Where is my permit application PP-2026-0412?
  state: active
- id: default3
  title: Find bin collection days
  subtitle: ''
  prompt: Which day is the grey bin collected on Elm Street?
  state: active
```

---

## 7. Import Order and CLI Commands

Tools must be imported before the agent. There are no dependencies between the three tools themselves.

**Dependency order:**
```
knowledge-bases/city_regulations.yaml  (existing — no change)
tools/get_permit_status.py     + tools/permits.csv
tools/get_request_status.py    + tools/requests.csv
tools/get_collection_days.py   + tools/collection_calendar.csv
agents/civic_info_agent.yaml
```

**CLI commands for the three tool imports** (each packages its CSV via `--package-root`):

```bash
orchestrate tools import -k python \
  --file tools/get_permit_status.py \
  --package-root tools/

orchestrate tools import -k python \
  --file tools/get_request_status.py \
  --package-root tools/

orchestrate tools import -k python \
  --file tools/get_collection_days.py \
  --package-root tools/
```

These commands are added to `scripts/import-all.sh` immediately before the agent import step. The corresponding `orchestrate tools remove` calls are added to `scripts/delete-all.sh` after the agent removal step.

---

## 8. Test Scenarios

| Prompt | Expected tool | Expected outcome |
|---|---|---|
| "Where is my permit application PP-2026-0412?" | `get_permit_status` | Returns 18 Elm Street, garden shed 12 sqm, Under review, submitted 2026-09-12, decision due 2026-10-12. Contact: 555 0110 / permits@utopia.example. |
| "Has my permit PP-2026-0398 been decided?" | `get_permit_status` | Returns 7 Harbour Lane, two-storey extension, Approved, decided 2026-09-30. Contact: 555 0110 / permits@utopia.example. |
| "What does PP-2026-0433 need?" | `get_permit_status` | Returns 42 Mill Road, garage, Additional documents requested, site plan missing. Contact: 555 0110 / permits@utopia.example. |
| "Has my pothole report RQ-2026-1187 been scheduled?" | `get_request_status` | Returns Elm Street, pothole, Scheduled, repair 2026-10-09. Contact: 555 0120 / roads@utopia.example. |
| "What is the status of RQ-2026-1210?" | `get_request_status` | Returns Station Road, damaged sign, Received, no scheduled date yet. Contact: 555 0120 / roads@utopia.example. |
| "Which day is the grey bin collected on Elm Street?" | `get_collection_days` | Returns grey Monday, green Thursday, blue Wednesday, yellow Wednesday. Contact: 555 0130 / waste@utopia.example. |
| "What are the collection days for Harbour Lane?" | `get_collection_days` | Returns grey Tuesday, green Friday, blue Wednesday, yellow Wednesday. Contact: 555 0130 / waste@utopia.example. |
| "When is my permit PP-2026-9999 being decided?" | `get_permit_status` | NOT_FOUND reply. Directs to 555 0110 / permits@utopia.example. |
| "What are the collection days for King Street?" | `get_collection_days` | NOT_FOUND reply. Directs to 555 0130 / waste@utopia.example. |
| "My permit PP-2026-0412 is under review — how long does a decision take?" | `get_permit_status` + `city_regulations` KB | Tool gives application status; KB (Building Permit Guide) states 30-day decision window. Both used in the same answer. Contact: 555 0110 / permits@utopia.example. |
| "My permit application" (no number given) | None yet — ask | Agent asks for the permit number before calling the tool. |
| "What are the bin collection days?" (no street given) | None yet — ask | Agent asks for the street name before calling the tool. |
