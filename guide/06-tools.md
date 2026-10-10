# Chapter 6. Adding Orchestrate Tools

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 5 completed, or its Agent and Knowledge Base imported from the walkthrough folder as that chapter's Overview describes.

## Overview

Three weeks ago you applied for a building permit. The confirmation email gives a number, PP-2026-0412, and nothing has arrived since. You ask CivicPulse: "Where is my permit application PP-2026-0412?" The Agent of chapter 5 has the city's regulations in its Knowledge Base. It can tell you that a decision is given within 30 days, and nothing more, because it has never seen your application. Your file is in the city's permit system, not in a document.

Every question that the Agent of chapter 5 could answer had the same answer for every resident: the hours of a department, the rule for a shed. The questions in this chapter need answers that depend on the record asked about: the status of one application, the date of one repair, the collection day of one street. To answer, the Agent looks up that record in the city's system when the question is asked.

An Orchestrate Tool is how an Agent fetches it. In this chapter, Bob writes three Orchestrate Tools for the City of Utopia: one that looks up a permit application by its number, one that looks up a problem report by its number, and one that gives the collection days of a street. Utopia has no permit system, so Bob also writes the records that the Tools read, a few lines in a file for each. Then Bob connects the Tools to the Agent, and the Agent decides, question by question, when to use one.

The Agent and its Knowledge Base stay as in chapter 5; the instructions gain one paragraph.

Skip this chapter if you have already given an Agent a Python Tool with Bob. To continue with chapter 7 without building it, first make sure that the Knowledge Base of chapter 5 exists on your instance, then send Bob these instructions in Agent mode: `Import the three Python tools in walkthroughs/ch06/tools into my instance, each one packaged with its record file, then import walkthroughs/ch06/agents/civic_info_agent.yaml.`

## 6.1 Before you start

- The setup from chapter 2, complete.
- The Agent `civic_info_agent` from chapter 5 on your instance, in Draft, with the Knowledge Base `city_regulations` attached. If you skipped chapter 5, import both as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that both are there: in Ask mode, ask `Which agents and knowledge bases exist on my instance?` and confirm that `civic_info_agent` and `city_regulations` are listed.

## 6.2 What an Orchestrate Tool is

Instructions hold what the Agent knows; the Knowledge Base, what the city has written down. Neither holds the status of a permit application: that information is in the permit system, and it belongs to one resident. An Orchestrate Tool is a function that the Agent calls while it answers, to fetch information or to act.

The Agent uses the following parts of an Orchestrate Tool in turn.

| Part | What it is | What the Agent does with it |
|---|---|---|
| The description | A sentence that says what the Tool does and when to use it | Reads it, with the question, to decide whether to call the Tool |
| The parameters | The values the Tool needs, each with a name and a description, for example a permit number | Finds them in the question, or asks the resident for them |
| The result | What the Tool returns, for example the record of one application | Writes the answer from it |

No prompt tells the Agent to call a Tool for a given question, just as none tells it to search the Knowledge Base: the instructions say when Tools apply, and the model decides each case from the question and the descriptions of its Tools. "Where is my permit application PP-2026-0412?" matches the description of the permit Tool and contains a permit number, so the Agent calls it with that number. "Where is my permit application?" matches the description but has no number, so the Agent asks for it. Besides the instructions, the description and the parameter names are all the Agent has for that decision.

**Kinds of Orchestrate Tools**

| Kind | What it is | In this guide |
|---|---|---|
| Python Tool | A Python function in a file, uploaded to the instance and run there | This chapter |
| OpenAPI Tool | An existing REST API, described by its OpenAPI file; no code to write | The alternative to a Python Tool when the API already exists |
| Orchestrate Toolkit | A set of Tools served by an MCP server, like the one that Bob uses to talk to your instance | Chapter 8 |
| Orchestrate Flow | A sequence of steps with Tools and Agents in it, which the Agent calls as one Tool | Chapter 10 |

A Python Tool consists of a function, a description, parameters and a result, in one file, which section 6.7 describes.

**The data of this chapter**

In a real city, the permit Tool would query the permit system, over its API, with a credential. The City of Utopia has no permit system. In this chapter, each Tool reads its records from a small file that Bob writes and uploads together with the Tool: ten applications, ten problem reports, the collection days of ten streets. The Agent calls each Tool as it would call one connected to a real system.

**Reading the Agent's reasoning**

An Agent with Tools makes choices, and watsonx Orchestrate lets you see them. With every answer, the Agent can show the steps it took: the Tool it called, the values it passed, what the Tool returned. In the watsonx Orchestrate chat, the steps are behind a Show Reasoning link next to the answer; through Bob, you ask for them with the words "with reasoning". The Agent's definition has a setting for this, `hide_reasoning`, which is `false` for `civic_info_agent`; section 6.8 shows how to read the steps.

## 6.3 Ask mode: describe the lookups

Mode: Ask, in a new conversation.

The prompt does not use the word Tool: it describes what residents ask and where the answers are, says that the city has no system to query, and leaves the choice of the component to Bob, which should be a Python Tool, as 6.2 describes.

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

In Bob's answer, look for the following:

- Under what it understood, Bob proposes record files and Python Tools that read them, one per kind of record. Bob chose the word Tool without being told; 6.2 explains why.
- What it found on the instance: the Agent, the Knowledge Base, and no Tools of the project.
- The line from chapter 4 that says the Agent does not look anything up in other systems. Bob may point out that this line has to change; the build in 6.6 changes it.
- Its questions: how many records, which status words, which bins, what to say when a number is unknown. They are answered below.

The second prompt creates the records in words: three applications, three reports and three streets, with fixed numbers and dates, so that your Agent gives the same answers as every other reader's Agent. The rest of the prompt takes the decisions Bob asked about. Nothing is created yet.

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

Check Bob's answer for the following:

- The records in tables, the code of the three Tools, the new paragraph of the instructions. Bob may even start as if it were going to write the files, and stop because Ask mode does not allow it.
- Above each Tool, Bob writes one sentence that describes it. "Look up the status of a building permit application by its permit number" is what the Agent will read when it decides.
- Bob invites you to switch to Agent mode. Do not switch yet; nothing has been created. The design that you read and approve follows in 6.4.

## 6.4 Plan mode: write the design

Mode: Plan, in the same conversation.

The design covers three Tools, three record files, a change to the Agent and an import for each Tool. Have Bob write it down.

```
Write the design for this change into design/city-services-tools-design.md.
```

Bob requests approval, writes the file and summarises it. Check that the file contains the following:

| Content | What to check |
|---|---|
| The three Tools | Name, parameter, result, and the sentence that describes it to the Agent. The sentence says what the Tool looks up and by what: "by its permit number" rather than only "a permit" |
| The records | Three CSV files with your records, next to the Tool that reads each one |
| The import of each Tool | The design says that each Tool is uploaded to the instance together with its record file. Without the file, the Tool fails on the instance |
| The change to the Agent | The three Tools attached; the instructions say when to use a Tool, ask for a missing number, what to say when a record is unknown; the facts and the Knowledge Base unchanged |
| The build order | Records and Tools first, each Tool imported, then the Agent |
| The tests | The three questions of the first prompt in 6.3 at least, each with its expected record |

## 6.5 Approve the design

Mode: Plan, same conversation.

Compare the design with the table in 6.4. If a Tool, a record or a test is missing, ask Bob to change it in the same conversation.

The design must say that each Tool is uploaded together with its record file. If it does not, send:

```
Each tool must be uploaded to the instance together with its record file.
Change the design so that it says how.
```

Bob adds the mechanism to the design and explains it: the import command names the `tools` folder as the package root, and the whole folder goes to the instance with the Tool. When the design says what you mean, go on to 6.6.

## 6.6 Agent mode: build and test

Mode: Agent, in a new conversation.

```
The design in @design/city-services-tools-design.md is approved. Build it.
```

This build includes code. Bob:

1. Writes the three record files, one CSV per kind of record.
2. Writes the three Tools, one Python file each, in the `tools` folder.
3. Imports the Tools. Each one is packaged with its record file and uploaded; the instance checks the code and the description, and Bob corrects a file if the instance refuses it.
4. Updates the Agent: attaches the three Tools, extends the instructions and imports the Agent again, replacing the Agent in Draft.
5. Tests the Agent with the questions from the design and reports.

Approve each request as it comes. Bob's report may say that the Agent is deployed. It is imported into Draft only; section 6.9 deploys it in Live.

## 6.7 What Bob built

Open the `tools` folder in the File Explorer. It has six files: three Python files, one per Tool, `get_permit_status.py`, `get_request_status.py` and `get_collection_days.py`, and three CSV files with the records, `permits.csv`, `requests.csv` and `collection_calendar.csv`.

Open `get_permit_status.py` and find the function `get_permit_status`, in the run near the bottom of the file. Around the function are the following:

- The line `@tool` above the function. It tells watsonx Orchestrate that this function is a Tool.
- Just under the function name, the text between triple quotes. This is the description: one sentence on what the Tool does, one line on the parameter, one line on the result. These are the words the Agent reads when it decides whether to call the Tool.
- `permit_number`, the parameter. The Agent must find a value for it in the resident's question before it can call the Tool.

The rest of the file opens `permits.csv`, finds the line with that number, and returns it.

`permits.csv` has one line per application. Find the line of PP-2026-0412, the application in the Overview: 18 Elm Street, garden shed, under review, decision due 2026-10-12.

Open `agents/civic_info_agent.yaml`. Near the bottom, under `tools`, are the three Tool names. In the instructions, a new section says when to call each Tool, what to ask when the number is missing, and what to say when there is no record. The line from chapter 4 that forbade looking anything up now allows the three Tools. The facts and the Knowledge Base are unchanged. Bob may have added starter prompts for the new questions.

The folder may also contain a requirements file, which names the Python libraries that the Tools need and is uploaded with them, and a test report, which Bob wrote for itself. Neither is part of the Agent.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 6.8 Try it, and read the reasoning

Ask the Agent the three questions of the first prompt in 6.3, through Bob or in the preview panel of watsonx Orchestrate. Through Bob, start each message with `Ask civic_info_agent:`.

```
Where is my permit application PP-2026-0412?
```

```
Has my pothole report RQ-2026-1187 been scheduled?
```

```
Which day is the grey bin collected on Elm Street?
```

The answers are, in order: under review with a decision due 12 October, a repair scheduled for 9 October, and Monday. Each answer ends with the department's contact, because the instructions ask for it.

Then try questions that test the limits of the Tools:

- Leave out the number, in a new conversation so that the Agent does not reuse the one above: "Where is my permit application?" The Agent asks for it.
- Use a number that does not exist: "Where is my permit application PP-2026-9999?" The Agent says that it has no record under that number and gives the contact of Permits and Planning.
- Ask for a Tool and a document: "My application PP-2026-0412 is for a shed. Can I start building while I wait?" The answer says that work must not start before the decision, from the Building Permit Guide. Keep this question for the next part.
- Name a street without needing a lookup: "The grey bin on Elm Street was not collected today. Who do I call?" The Agent answers with the Waste and Recycling contact and does not call the calendar Tool, because the question needs no collection day.

To read how the Agent got there, ask the first question again through Bob, with two more words:

```
Ask civic_info_agent, with reasoning: "Where is my permit application PP-2026-0412?"
```

Bob now shows the steps along with the answer: the Agent called `get_permit_status` with the permit number `PP-2026-0412`, the Tool returned the record from `permits.csv`, and the Agent wrote the answer from it. In the preview panel of watsonx Orchestrate, every answer has a Show Reasoning link next to it, which opens the same steps: the Tool, its input, its output.

Next, ask the shed question with reasoning. The Knowledge Base appears in the steps as a Tool named `city_regulations`, with the query the Agent sent it and the passages it got back. The Agent can answer this question by two routes, the record and the guide, and the steps show which it took: in the test runs, it used both sources on one run and the guide alone on another, and both answers were correct.

When an Agent with Tools answers wrongly, open its reasoning steps. They show which Tool was called and with which values, and that narrows the search: a wrong Tool points at the Tool descriptions, a wrong value at the parameter descriptions, and no call at all at the instructions. Tell Bob what you found, in one sentence, as in 4.9.

## 6.9 Deploy the change in Live

Mode: Agent, same conversation.

On the Developer Edition, skip this section. Until you deploy, the Agent in Live still answers that a decision is given within 30 days, or does not exist if you imported chapter 5 from the walkthrough folder, because only the Agent in Draft has the Tools. Send the deployment instruction again:

```
Deploy civic_info_agent from draft to live.
```

Bob confirms the deployment. Go to the watsonx Orchestrate chat and ask about PP-2026-0412: the resident of the Overview now gets the status of their application.

## 6.10 Summary

The Agent now gives answers that depend on the record asked about: the status of an application, the date of a repair, the collection day of a street. You approved the design and supplied the records; the Tools, the records and the new instructions are files in your project folder, and you have read the Agent's reasoning.

- An Orchestrate Tool is a function that the Agent calls while it answers. The Agent decides when to call it, from the Tool's description and the question.
- The description and the parameter descriptions are written for the Agent. The Agent decides from them, so they are the first place to look when it decides wrongly.
- One answer can combine the sources: a Tool for the resident's record, the Knowledge Base for the rule, the instructions for the contact.
- The Agent's reasoning shows the steps between the question and the answer, every Tool call included. Ask Bob for it with the words "with reasoning", or open Show Reasoning next to an answer in watsonx Orchestrate.

None of the three Tools creates or changes a record. Chapter 7 adds a Tool that creates a problem report through the API of the city's 311 Call Center, and introduces the Orchestrate Connection, the asset where a Tool's credentials are kept so that they never appear in code or in git.
