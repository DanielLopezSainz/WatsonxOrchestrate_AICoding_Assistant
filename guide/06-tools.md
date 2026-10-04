# Chapter 6. Adding tools

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 5 completed, or its agent and knowledge base imported from the walkthrough folder as that chapter's Overview describes.

## Overview

Suppose that you applied for a building permit three weeks ago. You have a confirmation email with a number on it, PP-2026-0412, and nothing since. You ask CivicPulse: "Where is my permit application PP-2026-0412?" The agent of chapter 5 knows the city's regulations by heart. It can tell you that a decision is given within 30 days, and that is all it can tell you, because it has never seen your application. Your file is in the city's permit system, not in a document.

This is the difference between knowing and looking up. Every answer so far was the same for every resident: the hours of a department, the rule for a shed. The answers in this chapter are different for every resident who asks. Where is my application. Has my pothole report been scheduled. Which day is the grey bin collected on my street. To answer, the agent must fetch one record from one system, at the moment the question is asked.

A tool is how an agent fetches it. In this chapter, Bob writes three tools for the City of Utopia: one that looks up a permit application by its number, one that looks up a problem report by its number, and one that gives the collection days of a street. Utopia has no permit system, so Bob also writes the records that the tools read, a few lines in a file for each. Then Bob connects the tools to the agent, and the agent decides, question by question, when to use one. You watch it decide: for the first time, you read the agent's reasoning, the steps it took between the question and the answer.

The component introduced in this chapter is the tool. Everything else stays as in chapter 5: one agent, its instructions, its knowledge base.

Skip this chapter if you have already given an agent a Python tool with Bob. To continue with chapter 7 without building it, first make sure that the knowledge base of chapter 5 exists on your instance, then send Bob these instructions in Agent mode: `Import the three Python tools in walkthroughs/ch06/tools into my instance, then import walkthroughs/ch06/agents/civic_info_agent.yaml.`

## 6.1 Before you start

- The setup from chapter 2, complete.
- The agent `civic_info_agent` from chapter 5 on your instance, in Draft, with the knowledge base `city_regulations` attached. If you skipped chapter 5, import both as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that both are there: in Ask mode, ask `Which agents and knowledge bases exist on my instance?` and confirm that `civic_info_agent` and `city_regulations` are listed.

## 6.2 What a tool is

Instructions hold what the agent knows. A knowledge base holds what the city has written down. Neither holds the status of your permit application, because that status changed this morning, in a system, and it is yours alone. A tool is a function that the agent can call to fetch information like this, or to act, while it answers.

In watsonx Orchestrate, a tool has three parts, and the agent uses each one in turn.

| Part | What it is | What the agent does with it |
|---|---|---|
| The description | A sentence that says what the tool does and when to use it | Reads it, with the question, to decide whether to call the tool |
| The parameters | The values the tool needs, each with a name and a description, for example a permit number | Finds them in the question, or asks the resident for them |
| The result | What the tool returns, for example the record of one application | Writes the answer from it |

The agent calls a tool the way it searches the knowledge base: nobody tells it to. The model reads the question, the instructions and the descriptions of its tools, and chooses. "Where is my permit application PP-2026-0412?" matches the description of the permit tool and contains a permit number, so the agent calls it with that number. "Where is my permit application?" matches the description but has no number, so the agent asks for it. This is why the description and the parameter names are written with care: they are all the agent has to decide with.

**Kinds of tools**

| Kind | What it is | In this guide |
|---|---|---|
| Python tool | A Python function in a file, uploaded to the instance and run there | This chapter |
| OpenAPI tool | An existing REST API, described by its OpenAPI file; no code to write | The alternative to a Python tool when the API already exists |
| MCP toolkit | A set of tools served by an MCP server, like the one that Bob uses to talk to your instance | Chapter 8 |
| Flow | A sequence of steps with tools and agents in it, which the agent calls as one tool | Chapter 10 |

A Python tool is the simplest kind, and the one that shows best what a tool is: a function, a description, parameters and a result, in one file. Bob writes the file. You read it in 6.7, and it is shorter than you expect.

**The data of this chapter**

In a real city, the permit tool would query the permit system, over its API, with a credential. The City of Utopia has no permit system. In this chapter, each tool reads its records from a small file that Bob writes and uploads together with the tool: ten applications, ten problem reports, the collection days of ten streets. The agent cannot tell the difference, and neither can the resident. Chapter 7 adds a tool that acts instead of reading, by calling a service that needs a key, and shows how the agent uses the key without ever seeing it.

**Reading the agent's reasoning**

An agent with tools makes choices, and watsonx Orchestrate lets you see them. With every answer, the agent can show the steps it took: the tool it called, the values it passed, what the tool returned. In the watsonx Orchestrate chat, the steps are behind a Show Reasoning link next to the answer; through Bob, you ask for them with the words "with reasoning". The agent's definition has a setting for this, `hide_reasoning`, which is `false` for `civic_info_agent`. Reading the steps is how you check that the agent chose the right tool for the right reason. Section 6.8 shows you how.

## 6.3 Ask mode: describe the lookups

Mode: Ask, in a new conversation.

The purpose of this prompt is the same as in chapters 4 and 5: before anything is written, Bob must understand what you want and tell you what it needs to know. This time the request is about things the agent must look up, and Bob needs to know what systems exist. None do, and the prompt says so.

The prompt does not say the word tool. As in chapter 5, it describes what residents ask and where the answer is, and leaves the choice of the component to Bob. You know from 6.2 what the right choice is, so you can check Bob's proposal.

```
I want civic_info_agent to answer questions about one resident's own record,
not only questions about rules and contacts. Residents ask things like "Where
is my permit application PP-2026-0412?", "Has my pothole report RQ-2026-1187
been scheduled?" and "Which day is the grey bin collected on Elm Street?". The
city keeps three kinds of records for this: building permit applications,
problem reports about roads, and the collection calendar by street, each one
found by its number or by the street name. The City of Utopia has no systems
to query: the records are fictional, and you will write them.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Read Bob's answer for four things:

- How Bob would implement it. Under what it understood, Bob proposes record files and Python tools that read them, one per kind of record. Nobody said the word tool; Bob chose it, and 6.2 says why it is the right choice.
- What it found on the instance: the agent, the knowledge base, no tools.
- The line from chapter 4 that says the agent does not look anything up in other systems. Bob may point out that it has to go. It does.
- Its questions: how many records, which status words, which bins, what to say when a number is unknown. They are answered below.

Residents of Utopia are about to get their first personal answers, and the records behind them do not exist yet. The second prompt creates them in words: three applications, three reports, three streets, with numbers and dates that this chapter uses from here to the end, so that your agent and every other reader's agent give the same answers. The rest of the prompt takes the decisions Bob asked about. Nothing is created yet; Ask mode is still the right mode.

```
These are my answers. Three Python tools: get_permit_status, which receives a
permit number and returns the application's address, type of work, status,
submission date and the date by which a decision is due; get_request_status,
which receives a request number and returns the report's street, type of
problem, status and scheduled date when there is one; and get_collection_days,
which receives a street name and returns the collection day of each bin, the
same every week. Each tool reads its records from a CSV file kept with the
tool, so that the file is uploaded with it.

Use these records as they are, and add seven more of your own to each file,
using only the status words that appear in these records. The bins are the four
of the waste sorting rules: grey, green, blue and yellow.

Permit applications. PP-2026-0412, 18 Elm Street, garden shed of 12 square
metres, status Under review, submitted 2026-09-12, decision due 2026-10-12.
PP-2026-0398, 7 Harbour Lane, two-storey extension, status Approved, submitted
2026-08-20, decided 2026-09-30. PP-2026-0433, 42 Mill Road, garage, status
Additional documents requested, submitted 2026-09-25, site plan missing.

Problem reports. RQ-2026-1187, Elm Street, pothole, status Scheduled, repair on
2026-10-09. RQ-2026-1203, Harbour Lane, street light out, status Closed, fixed
on 2026-10-01. RQ-2026-1210, Station Road, damaged sign, status Received.

Collection days. Elm Street: grey bin Monday, green bin Thursday, blue and
yellow bins Wednesday. Harbour Lane: grey Tuesday, green Friday, blue and
yellow Wednesday. Mill Road: grey Monday, green Thursday, blue and yellow
Friday.

The agent uses a tool for any question about one resident's application,
report or street. Any resident who gives a number sees the record; the agent
does not check who is asking. When a question gives no number or street, the
agent asks for it. When a number or street is unknown, the agent says that it has no
record under that number and gives the contact of the department. The agent
keeps its facts and its knowledge base; a question can need both a tool and a
document. The rule from chapter 4 that the agent does not look anything up in
other systems is replaced by these tools. Answers from a tool stay within
three sentences and end with the contact of the department, as before.
```

Bob confirms the answers and, as in chapter 4, goes further. Read its answer for three things:

- The whole implementation is already there: the records in tables, the code of the three tools, the new paragraph of the instructions. Bob may even start as if it were going to write the files, and stop because Ask mode does not allow it.
- The three descriptions, one sentence above each tool. "Look up the status of a building permit application by its permit number" is what the agent will read when it decides.
- The invitation to switch to Agent mode. Do not take it. Nothing has been created, and the next step turns this proposal into a design that you read and approve.

## 6.4 Plan mode: write the design

Mode: Plan, in the same conversation.

Three tools, three record files, a change to the agent and an import for each tool: this is the largest design so far. Have Bob write it down.

```
Write the design for this change into design/city-services-tools-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. Open the file and check that it contains the following:

| Content | What to check |
|---|---|
| The three tools | Name, parameter, result, and the sentence that describes it to the agent. The sentence says what the tool looks up and by what: "by its permit number", not just "a permit" |
| The records | Three CSV files with your records, next to the tool that reads each one |
| The import of each tool | The design says that each tool is uploaded to the instance together with its record file. Without the file, the tool fails on the instance |
| The change to the agent | The three tools attached; the instructions say when to use a tool, ask for a missing number, what to say when a record is unknown; the facts and the knowledge base unchanged |
| The build order | Records and tools first, each tool imported, then the agent |
| The tests | The three questions of the Overview at least, each with its expected record |

## 6.5 Approve the design

Mode: Plan, same conversation.

Read the design once. If something is missing or wrong, ask Bob to change it, as in chapter 4.

Check one point in particular: the design must say that each tool is uploaded together with its record file. If it does not, send:

```
Each tool must be uploaded to the instance together with its record file.
Change the design so that it says how.
```

Bob adds the mechanism to the design and explains it: the import command names the `tools` folder as the package root, and the whole folder goes to the instance with the tool. When the design says what you mean, it is approved.

## 6.6 Agent mode: build and test

Mode: Agent, in a new conversation.

```
The design in @design/city-services-tools-design.md is approved. Build it.
```

The @ mention tells Bob to read the design file. This is the first build with code in it. Bob:

1. **Writes the three record files**, one CSV per kind of record.
2. **Writes the three tools**, one Python file each, in the `tools` folder. Open one while Bob continues.
3. **Imports the tools.** Each one is packaged with its record file and uploaded; the instance checks the code and the description, and Bob corrects a file if the instance refuses it.
4. **Updates the agent**: the three tools are attached, the instructions are extended, and the agent is imported again, replacing the agent in Draft.
5. **Tests** the agent with the questions from the design and reports.

Approve each request as it comes. Bob's report may say that the agent is deployed. It is imported into Draft; deploying in Live is section 6.9.

## 6.7 What Bob built

Open the `tools` folder in the File Explorer. It has six files: three Python files, one per tool, `get_permit_status.py`, `get_request_status.py` and `get_collection_days.py`, and three CSV files with the records, `permits.csv`, `requests.csv` and `collection_calendar.csv`.

Open `get_permit_status.py`. Near the bottom of the file is the function `get_permit_status`. Three things around it are written for the agent:

- The line `@tool` above the function. It tells watsonx Orchestrate that this function is a tool.
- The text between triple quotes just under the function name. This is the description: one sentence on what the tool does, one line on the parameter, one line on the result. These are the words the agent reads when it decides whether to call the tool.
- The parameter `permit_number`. The agent must find a value for it in the resident's question before it can call the tool.

The rest of the file opens `permits.csv`, finds the line with that number, and returns it. If the city connects a real permit system, this is the part that changes; the agent does not.

Open `permits.csv`. One line per application. The second line is PP-2026-0412: 18 Elm Street, garden shed, under review, decision due 2026-10-12. That is the answer the resident of the Overview will get.

Open `agents/civic_info_agent.yaml`. Two things changed. Near the bottom, under `tools`, the three tool names. In the instructions, a new section says when to call each tool, what to ask when the number is missing, and what to say when there is no record. The line from chapter 4 that forbade looking anything up is gone. The facts and the knowledge base are still there.

Bob may have added files of its own, such as a requirements file or a test report. They are not part of the agent on the instance; ignore them unless you are curious.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 6.8 Try it, and read the reasoning

Ask the agent the three questions from the Overview, through Bob or in the preview panel of watsonx Orchestrate. Through Bob, start each message with `Ask civic_info_agent:`.

```
Where is my permit application PP-2026-0412?
```

```
Has my pothole report RQ-2026-1187 been scheduled?
```

```
Which day is the grey bin collected on Elm Street?
```

Under review, decision due 12 October. Repair scheduled for 9 October. Monday. Each answer ends with the department's contact, because the instructions ask for it.

Then ask as residents do:

- Without a number: "Where is my permit application?" The agent asks for it.
- With a number that does not exist: "Where is my permit application PP-2026-9999?" No record under that number, and the contact of Permits and Planning. Nothing is invented.
- With a tool and a document: "My application PP-2026-0412 is for a shed. Can I start building while I wait?" The answer says that work must not start before the decision, from the building permit guide. Keep this question for the next part.
- With a street name but no need for a lookup: "The grey bin on Elm Street was not collected today. Who do I call?" The agent answers with the Waste and Recycling contact and does not call the calendar tool: the question names a street, but nothing in it needs the collection day.

Now read how the agent got there. Ask the first question again through Bob, with two more words:

```
Ask civic_info_agent, with reasoning: "Where is my permit application PP-2026-0412?"
```

Bob now shows the steps along with the answer: the agent called `get_permit_status` with the permit number `PP-2026-0412`, the tool returned the record from `permits.csv`, and the agent wrote the answer from it. In the preview panel of watsonx Orchestrate, every answer has a Show Reasoning link next to it, which opens the same steps: the tool, its input, its output.

Now the shed question, with reasoning. The knowledge base appears in the steps as a tool named `city_regulations`, with the query the agent sent it and the passages it got back. The agent can answer this question by two routes, the record and the guide, and the steps show which it took. On the runs behind this chapter, it took both on one run and the guide alone on another, with a correct answer each time. The steps are the only place where you can see the difference, and that is why you read them.

These steps are what to read whenever an agent with tools answers wrongly. Wrong tool: a tool description is unclear. Right tool, wrong value: a parameter description is unclear. No tool at all: the instructions do not say when to use one. Each is one sentence to Bob, as in 4.9.

## 6.9 Deploy the change in Live

Mode: Agent, same conversation.

The agent that looks up records exists in Draft. The agent deployed in Live still answers that a decision is given within 30 days. Deploy again:

```
Deploy civic_info_agent from draft to live.
```

Bob reports that the agent is deployed. Go to the watsonx Orchestrate chat and ask about PP-2026-0412: the resident of the Overview now gets the status of their application. On the Developer Edition, skip this step.

## 6.10 Summary

The agent now gives answers that are different for every resident: the status of an application, the date of a repair, the collection day of a street. Bob wrote the records, the tools and the change to the agent; you described the lookups, fixed the records, and read the agent's reasoning for the first time.

- A tool is a function that the agent calls while it answers. The agent decides when to call it, from the tool's description and the question.
- The description and the parameter descriptions are written for the agent. The agent decides from them, so they are the first place to look when it decides wrongly.
- One answer can combine the sources: a tool for the resident's record, the knowledge base for the rule, the instructions for the contact.
- The agent's reasoning shows the steps between the question and the answer, every tool call included. Read it to check an answer and to diagnose a wrong one.

The three tools read records; none of them changes anything. The next thing residents ask for is to report a pothole, not to check on one. That takes a tool that creates a record in the city's service desk, a service reached over an API with a key, and that key must never appear in a chat, in git or in a tool's code. In chapter 7, the agent gets a tool that reports an issue, and watsonx Orchestrate keeps the key for it: a connection.
