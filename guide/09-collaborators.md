# Chapter 9. One Agent per department: Collaborator Agents

Level: intermediate. Time: about 60 minutes. Prerequisites: chapter 8 completed, or its Toolkit and Agent imported from the walkthrough folder as that chapter's Overview describes.

## Overview

Driving home, you hit a pothole on Harbour Lane. That evening you open CivicPulse to report it, and you ask about the bins at the same time: "There is a pothole at 7 harbour ln, and which day is the green bin collected there?" The Agent we have been working on can answer all our questions, because it contains instructions to cover everything: contacts, regulations, four Tools, addresses. That is the problem. Every question goes through a page of rules, and a change for one department can break the answers of the others.

The City of Utopia solved this long ago with its 311 Call Center: residents call one number, and the call centre passes each call to the department that owns it. This chapter does the same. A front desk Agent talks to residents, and one Agent per department sits behind it with its own Tools and documents. The front desk keeps the name `civic_info_agent`, so residents notice nothing.

The Collaborator Agent is the component introduced in this chapter: an Orchestrate Agent that another Agent passes questions to.

Skip this chapter if you have already built an Agent with Collaborator Agents with Bob. To continue with chapter 10 without building it, send Bob these instructions in Agent mode: `Import the four agents in walkthroughs/ch09/agents into my instance, the three department agents first and civic_info_agent last.`

## 9.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 8 on your instance, in Draft, with its four Tools, the two tools of the Toolkit `address_registry`, the Knowledge Base `city_regulations` and the Connection `utopia_311`. If you skipped chapter 8, import them as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that the Agent is there: in Ask mode, ask `Which tools does civic_info_agent have?` and confirm the six names: `get_permit_status`, `get_request_status`, `get_collection_days`, `report_issue`, `address_registry:lookup_address` and `address_registry:list_streets`.

## 9.2 What a Collaborator Agent is

A Collaborator Agent is an ordinary Orchestrate Agent that works for another Agent. The front desk Agent names its Collaborator Agents in its definition file, in a list called `collaborators`. When a question comes in that the front desk does not answer itself, it passes the question to the Collaborator Agent that owns it, waits for the answer, and gives it to the resident. The Collaborator Agent uses its own Tools, documents and instructions. The resident sees one conversation with one Agent.

**How the front desk decides**

No prompt tells the front desk which department to call. It decides from the description of each Collaborator Agent, as it decides from the description of a Tool. The ADK documentation says so in one line: supervisor Agents rely on descriptions to route tasks to the right Collaborator Agent. A department Agent's description is therefore written for the front desk, not for residents: it says what the department answers and when to call it.

**What changes compared with one Agent**

| | One Agent (chapters 4 to 8) | Front desk and departments (this chapter) |
|---|---|---|
| Instructions | Everything about the city in one text | The front desk: welcome, general contacts, routing, refusals. Each department: its own work only |
| Tools | All six on the one Agent | Each Tool on the Agent of its department |
| Knowledge Base | One Agent searches it | Each Agent that needs a document searches it; the instructions say which document is theirs |
| A change to one department | Edits the one Agent that serves all three | Edits one department Agent; the others are untouched |
| Reasoning | The Tool calls | The call to the Collaborator Agent, then its Tool calls inside it |
| Deployment | One Agent | Each Agent is deployed on its own |

Each Agent can use a different model; this guide keeps the default model for all four.

**The team of this chapter**

- `civic_info_agent`, the front desk: no Tools; the Knowledge Base for the Noise Ordinance, which belongs to no department; the welcome message and the starter prompts of chapter 4; the three departments as Collaborator Agents.
- `permits_agent`: `get_permit_status`; the Knowledge Base for the Building Permit Guide; the Permits and Planning facts.
- `roads_agent`: `get_request_status`, `report_issue` and `address_registry:lookup_address`; the Roads and Infrastructure facts, including the number for urgent hazards.
- `waste_agent`: `get_collection_days`, `address_registry:lookup_address` and `address_registry:list_streets`; the Knowledge Base for the Waste Sorting Rules; the Waste and Recycling facts.

Nothing new is written in code. The Tools, the Toolkit, the Knowledge Base and the Connection exist; the chapter changes Agent definitions only.

## 9.3 Ask mode: describe the team

Mode: Ask, in a new conversation.

The prompt names the asset, Collaborator Agents, and says what the front desk keeps and what each department takes, because those are the decisions that Bob would otherwise make for you. It leaves the descriptions and the instructions of the four Agents to Bob.

```
I want to split civic_info_agent into a front desk agent and three department
agents, Permits and Planning, Roads and Infrastructure, and Waste and
Recycling. The department agents are collaborators of the front desk. The front
desk keeps the name civic_info_agent, its welcome message and its starter
prompts; it answers general questions about the departments, their contacts
and hours, and questions about the noise ordinance, and passes every other
question to the department that owns it. Each department agent gets the tools
of its department, the facts of its department, and the documents of the
knowledge base that concern it. Nothing else changes: the tools, the toolkit,
the knowledge base and the connection stay as they are.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Look for these points in Bob's answer:

- What Bob understood: four Agents, the front desk with three Collaborator Agents, the Tools and the documents divided by department, the Knowledge Base shared.
- What exists: the Agent with its six tools, the Knowledge Base, the Toolkit, the Connection, and no other Agent of the project.
- The questions. Expect them about the names of the department Agents, which Tool goes where, what the front desk does with a question that concerns two departments, and whether the departments answer residents directly or only through the front desk. Bob may end by asking you to switch to Agent mode; stay in Ask mode.

Send the prompt below whole, still in Ask mode and in the same conversation; it covers what Bob asked and the points it did not raise. If Bob asked something that it does not cover, add one line with your answer at the end.

```
These are my answers.

1. The department agents are permits_agent, roads_agent and waste_agent.

2. permits_agent gets get_permit_status and the building permit guide.
roads_agent gets get_request_status, report_issue and
address_registry:lookup_address. waste_agent gets get_collection_days,
address_registry:lookup_address, address_registry:list_streets and the waste
sorting rules. civic_info_agent keeps no tool and keeps the noise ordinance.
The knowledge base city_regulations is attached to all four agents; the
instructions of each say which document is theirs.

3. The description of each department agent is written for the front desk: it
says what the department answers and when to call it. The front desk calls one
department for a question about that department, and both departments for a
question that concerns two. Residents talk to the front desk only.

4. Every agent keeps the rules of the earlier chapters: the contact details at
the end of each answer, the exact wording of the not-found replies, the address
lookup before any tool that takes a street, and the refusal of questions
outside the three departments, which stays with the front desk.

5. All four agents use the default model.
```

Bob confirms the answers and lays out the four Agents in the chat: the Tools and the documents of each, the descriptions, the build order. Bob may start as if it were going to write the files, and stop because Ask mode does not allow it. Do not switch to Agent mode: the design is written first, in Plan mode.

## 9.4 Plan mode: write the design

Mode: Plan, in the same conversation.

A design with several Agents has one more thing to get right than the designs of the earlier chapters: the build order. A Collaborator Agent must exist on the instance before the Agent that names it is imported, so the three departments come first and the front desk last. The prompt asks for the build steps in that order.

```
Write the design for this change into design/collaborators-design.md. End it
with the build steps in order: write the four agent definitions, import the
three department agents, import civic_info_agent, run the test scenarios
through the chat operation of the Orchestrate server.
```

Read Bob's answer. Sometimes, in its first lines, Bob says that it cannot write files and asks you to switch to Agent mode. If you get that answer and you have confirmed that you are in Plan mode, send `You are in Plan mode and can write files. Write the design to design/collaborators-design.md.` and approve the write; Bob then writes the file and summarises it.

Open `design/collaborators-design.md` and check it against this table:

| Content | What to check |
|---|---|
| The four Agents | Their names; for each, its Tools, its documents, its facts, in the division of 9.3 |
| The descriptions | One per department Agent, saying what it answers and when the front desk calls it; the front desk's description for residents |
| The front desk | The `collaborators` list with the three names; no Tools; the welcome message and the starter prompts kept |
| The instructions | The front desk: routing, the Noise Ordinance, the refusal; each department: its own work, with the rules of the earlier chapters |
| The build steps | A numbered list at the end: the four definitions, the three departments imported, then the front desk, then the test scenarios |

## 9.5 Approve the design

Mode: Plan, same conversation.

Read Bob's summary and the design file against the table in 9.4. If something is missing or wrong, request the change in the same conversation; Bob revises the file and waits again. When you agree with the design, go to 9.6: its first prompt is the approval.

## 9.6 Agent mode: build and test

Mode: Agent, in a new conversation.

Create a new conversation and switch to Agent mode to run the prompt:

```
The design in @design/collaborators-design.md is approved. Build it.
```

Bob follows the build steps of the design:

1. Writes the four definitions in the `agents` folder: three new files and a new version of `agents/civic_info_agent.yaml`.
2. Imports `permits_agent`, `roads_agent` and `waste_agent`. An Agent that names a Collaborator Agent not yet on the instance is refused at import; the order of the design prevents that.
3. Imports `civic_info_agent`, replacing the Agent in Draft. Its six tools are now on the departments.
4. Sends the test questions of the design to `civic_info_agent` and reports the answers.

Approve each request as it comes. Bob corrects failures of this kind during the build and reports only the results; to see what it corrected, ask in the same conversation: `List every problem you met during the build and how you solved it.`

## 9.7 What Bob built

Open `agents/permits_agent.yaml` in the File Explorer. It is a definition like the one of chapter 4, shorter: its `description` says what the department answers and when to call it; `tools` has one name; `knowledge_base` has `city_regulations`; the instructions hold the Permits and Planning facts, the rule for the Building Permit Guide and the rule for `get_permit_status`, and nothing about roads or waste. `agents/roads_agent.yaml` and `agents/waste_agent.yaml` have the same shape with their own Tools and documents.

Open `agents/civic_info_agent.yaml`. The `tools` list is empty, `collaborators` has the three names, `knowledge_base` keeps `city_regulations`. The instructions are a page shorter than in chapter 8: the welcome, the general contacts and hours, the rule for the Noise Ordinance, the routing rule, and the refusal of questions outside the three departments. The welcome message and the starter prompts are unchanged.

Bob's MCP tab and the project folder have nothing new: a Collaborator Agent is a line in an Agent definition, not a server or a file of its own.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 9.8 Try it

Ask the Agent, through Bob with `Ask civic_info_agent:` in front, or in the preview panel of the Agent in the watsonx Orchestrate builder:

```
There is a pothole at 7 harbour ln, and which day is the green bin collected there?
```

The answer has both parts: a request number for the pothole and the green bin day of Harbour Lane, with the two departments' contacts. Then try these:

- A question for one department: "Where is my permit application PP-2026-0412?" The status, from `permits_agent`.
- A question the front desk answers itself: "What are the quiet hours?" The Noise Ordinance, named in the answer, with no department called.
- A question outside the three departments: "When does the swimming pool open?" A polite refusal, as in chapter 4.
- A question with a wrong address: "Which day is the grey bin collected at 3 Castle Street?" The waste Agent asks you to check the address; the front desk passes that on.

Ask the first question again with reasoning. The steps show the front desk calling `roads_agent` and `waste_agent`, and inside each call the Tool calls of chapter 8: `lookup_address`, then `report_issue` or `get_collection_days`. A Collaborator Agent appears in the reasoning as a step of its own, with its name.

When an answer comes from the wrong department, the cause is a description: the front desk chose from the descriptions of the three. Tell Bob which question went where, in one sentence; Bob changes the description, imports the Agent again and tests.

## 9.9 Deploy the change in Live

Mode: Agent, same conversation.

Four Agents changed or appeared in Draft, and each Agent is deployed on its own. On the Developer Edition, skip this section.

```
Deploy permits_agent, roads_agent, waste_agent and civic_info_agent from draft to live, in that order.
```

When Bob reports the four deployments, go to the watsonx Orchestrate chat and ask the question of the Overview: the resident gets a request number and a collection day from one conversation.

## 9.10 Summary

You have split one Agent into a team: a front desk that residents talk to, and three department Agents that it passes questions to. The answers are the ones of chapter 8; the reasoning shows which department gave each. The same division applies to any Agent whose instructions have grown past one subject: give each subject an Agent, and keep one Agent in front.

- A Collaborator Agent is an Orchestrate Agent named in the `collaborators` list of another Agent. The calling Agent passes the question, the Collaborator Agent answers with its own Tools and documents, and the resident sees one conversation.
- The front desk routes by the descriptions of its Collaborator Agents, so a department Agent's description is written for the front desk: what it answers, and when to call it.
- A Collaborator Agent must be on the instance before the Agent that names it is imported, and each Agent is deployed on its own.
- A change to one department changes one Agent definition.

The team answers questions and takes reports, one exchange at a time. In chapter 10, the permit application itself becomes an Orchestrate Flow: a fixed sequence of steps that an Agent runs the same way for every resident.
