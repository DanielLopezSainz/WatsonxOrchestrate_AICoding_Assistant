# Design: Front Desk and Department Collaborators

## 1. Overview

This document describes the design for splitting `civic_info_agent` into a front desk agent and three department agents: `permits_agent` (Permits and Planning), `roads_agent` (Roads and Infrastructure) and `waste_agent` (Waste and Recycling).

The department agents are collaborators of the front desk. Residents talk only to `civic_info_agent`. It keeps its name, display name, description, welcome message and starter prompts. It answers general questions about the departments, their contacts and hours, the urgent hazard number, and questions about the noise ordinance. It passes every other question to the department that owns it, and it passes on the department's answer as it is.

Each department agent gets the tools of its department, the facts of its department, and the document of the knowledge base that concerns it. The department agents are hidden in the chat.

The tools, the `address_registry` toolkit, the `city_regulations` knowledge base and the `utopia_311` connection do not change.

---

## 2. Scope of Change

| Asset | Change |
|---|---|
| `agents/permits_agent.yaml` | New: Permits and Planning department agent, hidden |
| `agents/roads_agent.yaml` | New: Roads and Infrastructure department agent, hidden |
| `agents/waste_agent.yaml` | New: Waste and Recycling department agent, hidden |
| `agents/civic_info_agent.yaml` | Updated: instructions rewritten for the front desk role, `tools` emptied, `collaborators` set to the three department agents |
| `scripts/import-all.sh` | Updated: import the three department agents before `civic_info_agent` |
| `scripts/delete-all.sh` | Updated: remove `civic_info_agent` first, then the three department agents |
| `design/collaborators-design.md` | New: this design specification |

Unchanged: `get_permit_status`, `get_request_status`, `get_collection_days`, `report_issue`, the `address_registry` toolkit (`lookup_address`, `list_streets`), the `city_regulations` knowledge base and its three documents, and the `utopia_311` connection.

---

## 3. Agent Topology

| Agent | Display name | Hidden | Tools | Knowledge base | Its document | Collaborators |
|---|---|---|---|---|---|---|
| `civic_info_agent` | Utopia city information | No | none | `city_regulations` | Noise Ordinance | `permits_agent`, `roads_agent`, `waste_agent` |
| `permits_agent` | Permits and Planning | Yes | `get_permit_status` | `city_regulations` | Building Permit Guide | none |
| `roads_agent` | Roads and Infrastructure | Yes | `get_request_status`, `report_issue`, `address_registry:lookup_address` | none | none | none |
| `waste_agent` | Waste and Recycling | Yes | `get_collection_days`, `address_registry:lookup_address`, `address_registry:list_streets` | `city_regulations` | Waste Sorting Rules | none |

Common settings for all four agents, taken from `agents/civic_info_agent.yaml`:

- `llm: groq/openai/gpt-oss-120b`
- `style: react_core`
- `spec_version: v1`, `kind: native`

Department agents carry `hidden: true` and have no welcome message or starter prompts, because residents never reach them directly.

---

## 4. Agent Specifications

### 4.1 `civic_info_agent` (front desk)

**Keeps:** `name`, `display_name`, `description`, `welcome_content`, `starter_prompts`, `knowledge_base: [city_regulations]`, `chat_with_docs`, `llm`, `style`.

**Changes:** `tools: []`, `collaborators: [permits_agent, roads_agent, waste_agent]`, new instructions.

**Facts it holds:**

| Department | Phone | Email | Hours |
|---|---|---|---|
| Permits and Planning | 555 0110 | permits@utopia.example | Monday to Friday, 09:00 to 17:00 |
| Roads and Infrastructure | 555 0120 | roads@utopia.example | Monday to Friday, 07:00 to 19:00 |
| Waste and Recycling | 555 0130 | waste@utopia.example | Monday to Friday, 08:00 to 16:00 |

- What each department handles, in one line each.
- Urgent hazards on a public road, such as a burst water main or a fallen tree: call 555 0199 at any time. The front desk gives this number itself, without a handover, so that nobody waits.

**Its document:** the Noise Ordinance. For noise questions it searches `city_regulations` and answers only from the Noise Ordinance, ending with `https://services.utopia.example/noise`. The Noise Ordinance names no department, so this URL is the contact for noise answers.

**Routing rules:**

| Question about | Passed to |
|---|---|
| Building permits, permit rules, fees, processing time, permit numbers `PP-YYYY-NNNN` | `permits_agent` |
| Potholes, street lights, damaged signs, other road damage, reporting a road problem, request numbers `RQ-YYYY-NNNN` | `roads_agent` |
| Bins, collection days, streets in a district, sorting, glass, bulky items, hazardous waste | `waste_agent` |
| Department contacts and hours, urgent hazards, noise | answered by the front desk |
| Anything outside the three departments and noise | refused by the front desk |

- The front desk passes the resident's question with every detail given: numbers, addresses, descriptions, and the earlier turns it depends on.
- When a question concerns two departments, the front desk calls both and gives each answer one after the other.
- The front desk copies each department's answer word for word, without shortening, rewording, merging or adding to it.
- When a department asks the resident for a missing detail, the front desk asks the resident exactly that question and passes the reply back to the same department.

**Out-of-scope rule:** the front desk says that the question is outside the departments it covers and names the city office most likely to help. It never invents a phone number, email, URL or opening hours for that office.

### 4.2 `permits_agent`

**Description, written for the front desk:** Permits and Planning department of the City of Utopia. Call this agent for questions about building permits: whether a permit is needed, how to apply, fees, processing time and decisions. Also call it for the status of a permit application, which has a number in the format PP-YYYY-NNNN.

**Facts:** 555 0110, permits@utopia.example, Monday to Friday 09:00 to 17:00, applications online at `https://services.utopia.example/permits`.

**Its document:** the Building Permit Guide. It answers only from this document and never from the other documents in `city_regulations`.

**Tool rules (`get_permit_status`):**

- When a permit number `PP-YYYY-NNNN` is mentioned, call the tool with that number.
- When no number is given, ask for it before calling the tool.
- On `status = "NOT_FOUND"`, reply exactly: "I have no record under that reference. Please check the number and try again." Then give 555 0110 · permits@utopia.example.
- No authorisation check.
- For a question that needs both a tool result and the Building Permit Guide, use both in one answer.

**Contact ending:** Phone 555 0110, Email permits@utopia.example.

### 4.3 `roads_agent`

**Description, written for the front desk:** Roads and Infrastructure department of the City of Utopia. Call this agent for road problems on public streets: potholes, street lights, damaged signs and other road damage. Call it to report a new road problem, for the status of a road problem report (format RQ-YYYY-NNNN), and for urgent hazards on a public road such as a burst water main or a fallen tree.

**Facts:** 555 0120, roads@utopia.example, Monday to Friday 07:00 to 19:00, responsible for potholes, street lights and damaged signs. For urgent hazards, call 555 0199 at any time.

**Knowledge base:** none. For a rule or procedure not covered by its facts, it says "I do not have that information."

**Address resolution:** `lookup_address` is called first, with the address as typed, before any tool that takes a street. On `found = false` it asks the resident to check the address and calls no other tool. On `found = true` it uses the returned `street`.

**Tool rules (`get_request_status`):** these follow the permits pattern for numbers `RQ-YYYY-NNNN`. The NOT_FOUND reply is word for word the same, followed by 555 0120 · roads@utopia.example.

**Tool rules (`report_issue`):** the rules from `design/report-issue-design.md` carry over unchanged:

- Ask "What street is the problem on?" when the street is missing.
- Ask "What kind of problem is it (e.g., pothole, street light out, damaged sign)?" when the description is missing.
- Resolve the street with `lookup_address` and put the house number in the description.
- Submit at once, without asking for confirmation.
- On SUCCESS, give the `request_number` and say the resident can check its status later. On FAILED, say the report could not be submitted to the 311 Call Center and direct the resident to Roads and Infrastructure.

**Contact ending:** Phone 555 0120, Email roads@utopia.example, plus 555 0199 for urgent hazards.

### 4.4 `waste_agent`

**Description, written for the front desk:** Waste and Recycling department of the City of Utopia. Call this agent for bin collection days on a street, the streets in a district, which bin to use for which waste, glass, bulky items and booking their collection, and hazardous waste.

**Facts:** 555 0130, waste@utopia.example, Monday to Friday 08:00 to 16:00, bulky item collection booked at `https://services.utopia.example/bulky`.

**Its document:** the Waste Sorting Rules. It answers only from this document and never from the other documents in `city_regulations`.

**Address resolution:** same rules as `roads_agent`.

**Tool rules:**

- `get_collection_days`: resolve the street with `lookup_address` first, then pass the returned `street`. Ask for the street if none was given.
- `list_streets`: used when the resident asks which streets are in a district.
- When `get_collection_days` returns all day fields equal to `"NOT_FOUND"`, reply with the exact NOT_FOUND wording, then 555 0130 · waste@utopia.example.

**Contact ending:** Phone 555 0130, Email waste@utopia.example.

---

## 5. Rules Kept from Earlier Chapters

| Rule | Where it lives now |
|---|---|
| Contact details at the end of each answer | Every agent, with its own department's contacts. Noise answers end with the noise URL. |
| Exact NOT_FOUND wording: "I have no record under that reference. Please check the number and try again." | `permits_agent`, `roads_agent`, `waste_agent` |
| `lookup_address` before any tool that takes a street | `roads_agent`, `waste_agent` |
| Ask for a missing identifier before calling a tool | `permits_agent`, `roads_agent`, `waste_agent` |
| No authorisation check on records | `permits_agent`, `roads_agent`, `waste_agent` |
| Name a document only for an answer taken from the knowledge base | `civic_info_agent`, `permits_agent`, `waste_agent` |
| "I do not have that information." for uncovered rules | All four agents |
| Refusal of questions outside the three departments, naming the office that might help without inventing contact details | `civic_info_agent` only |
| Urgent hazard number 555 0199 | `civic_info_agent` (immediately) and `roads_agent` |
| Answer length: two or three sentences for facts, at most three for tool answers, a short paragraph for documents | All four agents |
| Plain language, English only, no invented answers | All four agents |

---

## 6. Known Limitations

1. **Pass-through is instructed, not enforced.** In the `react_core` style, the front desk always writes the final reply. The instruction to copy department answers word for word lowers the risk of rewording but cannot rule it out. The test scenarios check for this.
2. **Document separation is by instruction.** `civic_info_agent`, `permits_agent` and `waste_agent` all attach the whole `city_regulations` knowledge base, because knowledge bases attach per agent and the knowledge base stays unchanged. Retrieval can return chunks from any of the three documents, and each agent's instructions restrict it to its own document.
3. **Style alignment.** The instance currently reports `react_intrinsic` for `civic_info_agent`, while `agents/civic_info_agent.yaml` says `react_core`. Importing the file sets all four agents to `react_core`.

---

## 7. Import and Delete Order

A collaborator must exist before the agent that lists it.

**`scripts/import-all.sh`:** connection, knowledge base, tools and toolkit as today, then `permits_agent`, `roads_agent`, `waste_agent`, and last `civic_info_agent`.

**`scripts/delete-all.sh`:** `civic_info_agent` first, then `permits_agent`, `roads_agent`, `waste_agent`, then the toolkit, tools, knowledge base and connection as today.

---

## 8. Test Scenarios

All scenarios are sent to `civic_info_agent` only, through the `chat_with_agent` operation of the Orchestrate MCP server. Multi-turn scenarios reuse the returned `thread_id`. `include_reasoning: true` is used to confirm which collaborator, if any, was called.

| # | Prompt to `civic_info_agent` | Expected routing | Expected outcome |
|---|---|---|---|
| 1 | "What are the opening hours of Waste and Recycling?" | Front desk only | Monday to Friday 08:00 to 16:00, ending with 555 0130 / waste@utopia.example. No document named. |
| 2 | "What are the quiet hours on a Saturday night?" | Front desk only | From 23:00 to 08:00, citing the Noise Ordinance, ending with https://services.utopia.example/noise |
| 3 | "A tree has fallen across the road outside my house." | Front desk gives 555 0199 at once | Urgent hazard number given without waiting for a department |
| 4 | "Where is my permit application PP-2026-0412?" | `permits_agent` → `get_permit_status` | Under review, decision due 2026-10-12, 555 0110 / permits@utopia.example |
| 5 | (multi-turn after 4) "How long does a decision normally take?" | `permits_agent` → knowledge base | Cites the Building Permit Guide, 30-day window, 555 0110 / permits@utopia.example |
| 6 | "When is my permit PP-2026-9999 being decided?" | `permits_agent` | Exact NOT_FOUND wording, 555 0110 / permits@utopia.example |
| 7 | "Has my pothole report RQ-2026-1187 been scheduled?" | `roads_agent` → `get_request_status` | Scheduled 2026-10-09, 555 0120 / roads@utopia.example |
| 8 | "Report a pothole outside 18 elm st" | `roads_agent` → `lookup_address` → `report_issue` | Request number `RQ-2026-NNNN` returned. Description includes house number 18. Ends with 555 0120 / roads@utopia.example |
| 9 | "Can you report a pothole for me?" | `roads_agent` | Asks "What street is the problem on?" and the front desk relays this question unchanged |
| 10 | "Which day is the grey bin collected on Elm Street?" | `waste_agent` → `lookup_address` → `get_collection_days` | Monday, 555 0130 / waste@utopia.example |
| 11 | "What are the collection days for King Street?" | `waste_agent` → `lookup_address` | Asks the resident to check the address, calls no other tool, 555 0130 / waste@utopia.example |
| 12 | "Which streets are in the Harbour district?" | `waste_agent` → `list_streets` | Harbour Lane and River Close, 555 0130 / waste@utopia.example |
| 13 | "Where do I put broken glass?" | `waste_agent` → knowledge base | Cites the Waste Sorting Rules, 555 0130 / waste@utopia.example |
| 14 | "I want to build a 12 sqm garden shed and put out an old sofa. What do I need?" | `permits_agent` and `waste_agent` | Both answers given one after the other, each with its own contacts |
| 15 | "How do I renew my passport?" | Front desk only | Outside the covered departments. Names a likely office without inventing any contact detail |
| 16 | Starter prompts "The street light on my street has been out for a week, who do I tell?" and "How do I apply for a building permit?" | `roads_agent`; `permits_agent` → knowledge base | Roads asks for the street or gives its contacts, 555 0120 / roads@utopia.example. Permits cites the Building Permit Guide and https://services.utopia.example/permits, 555 0110 / permits@utopia.example. The other two starter prompts are scenarios 4 and 10. |

---

## 9. Build Steps

1. **Write the four agent definitions:** create `agents/permits_agent.yaml`, `agents/roads_agent.yaml` and `agents/waste_agent.yaml`, and update `agents/civic_info_agent.yaml` as specified in section 4. Update `scripts/import-all.sh` and `scripts/delete-all.sh` as specified in section 7.
2. **Import the three department agents:** `orchestrate agents import -f agents/permits_agent.yaml`, then `agents/roads_agent.yaml`, then `agents/waste_agent.yaml`. Confirm with `list_agents` that all three exist and are hidden.
3. **Import `civic_info_agent`:** `orchestrate agents import -f agents/civic_info_agent.yaml`. Confirm with `list_agents` that it has no tools, the three collaborators, `city_regulations`, and the unchanged welcome message and starter prompts.
4. **Run the test scenarios through the chat operation of the Orchestrate server:** send each scenario in section 8 to `civic_info_agent` with `chat_with_agent`, reusing `thread_id` for multi-turn scenarios, and record the results.
