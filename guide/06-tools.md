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

An agent with tools has choices to make, and watsonx Orchestrate lets you see them. The agent's definition has a setting, `hide_reasoning`, which is `false` for `civic_info_agent`: with every answer, the chat can show the steps that the agent took, including the tool it called and the values it passed. Reading those steps is how you check that the agent chose the right tool for the right reason, and it is where a wrong answer is diagnosed. Section 6.8 shows you how.

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

Bob queries the instance and answers with the three parts you know. Under what it understood, it says how it would implement the change: fictional record files, Python tools that read them, one per kind of record, and an addition to the agent's instructions. That is the right choice. If Bob proposes to put the records into the knowledge base instead, tell it that the records change and that a resident wants one exact record, not the closest passage; the answer below names the tools in any case.

On the instance, Bob finds the agent and the knowledge base, no tools, and an empty `tools` folder, created by the extension in chapter 2. It may also notice a line in the agent's instructions from chapter 4, "do not look anything up in other systems", and say that it must change. It must. Its questions vary from one run to another: one tool or three, how many records to write, which status words and bin colours to use, whether collection days are the same every week, what to say when a number is unknown, and whether any resident may see any record. The answer below settles all of them.

Bob may again end with suggested answers to click. Do not click any of them; type the answer below.

The second prompt is your answer. Its purpose is to fix the records that the chapter relies on, so that the questions in 6.8 have known answers on your instance as on anyone else's, and to take the decisions that Bob asked about. Nothing is created: Ask mode is still the right mode.

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

Bob confirms the answers. It might sketch the tools in the chat; the design is written in the next step.

## 6.4 Plan mode: write the design

Mode: Plan, in the same conversation.

This design has a new kind of content: code. For each tool, the design says what the function receives and returns and how it is described to the agent, before Bob writes a line of it.

```
Write the design for this change into design/city-services-tools-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. Open the file and check that it contains the following:

| Content | What to check |
|---|---|
| The three tools | For each: its name, the sentence that describes it to the agent, its parameter with a description, and what it returns, in the `tools` folder |
| The records | The three CSV files, each with your records and the columns they need, stored next to the tool that reads them |
| The change to the agent | The three tools attached to `civic_info_agent`, and the instructions extended: when to use a tool, ask for a missing number, what to say when a record is unknown; the facts and the knowledge base unchanged |
| The build order | Records and tools first, each tool imported, then the agent |
| The tests | The three questions of the Overview at least, each with the expected record |

Read the three descriptions with care. They are what the agent reads when it decides which tool to call, and a description that says "Looks up a permit" without saying "by its permit number" leaves the agent to guess what the parameter is. If a description is vague, ask Bob to make it specific.

## 6.5 Approve the design

Mode: Plan, same conversation.

Read the design once. If a description is vague or a record is missing, ask Bob to change it, as in chapter 4. When it says what you mean, it is approved: the approval is the first line of the next prompt.

## 6.6 Agent mode: build and test

Mode: Agent, in a new conversation.

```
The design in @design/city-services-tools-design.md is approved. Build it.
```

The @ mention tells Bob to read the design file. This is the first build with code in it. Bob:

1. **Writes the three record files**, one CSV per kind of record, with your records and its own.
2. **Writes the three tools**, one Python file each, in the `tools` folder. Open one while Bob continues; 6.7 explains what you see.
3. **Imports the tools.** For each one, the Orchestrate server packages the Python file with its record file and uploads them to the instance. The instance checks the code and the description; if it refuses one, Bob reads the error and corrects the file.
4. **Updates the agent**: the three tools are attached, the instructions are extended, and the agent is imported again, replacing the agent in Draft.
5. **Tests** the agent with the questions from the design and reports.

Approve each request as it comes.

## 6.7 What Bob built

Go to the `tools` folder in the File Explorer. A tool is the smallest thing Bob has built so far, and the one whose every line matters.

**A tool.** Open the permit tool. It is one Python function of about twenty lines. Three things in it are for the agent, not for the computer. The line above the function, `@tool`, marks it as a tool for watsonx Orchestrate. The text just under the function's name, between triple quotes, is the description: the sentence that says what the tool does, then a line for the parameter and a line for the result. It is the exact text that the agent reads when it decides. And the parameter, `permit_number`, with its type: the agent must find a value for it in the question before it can call the tool. The rest of the function opens the CSV file next to it, finds the row, and returns it. When the city gets a real permit system one day, that is the part that changes; the agent does not.

**The records.** Three CSV files next to the tools, one line per application, report or street. Find PP-2026-0412: under review, decision due 2026-10-12. This line is the answer that the resident of the Overview will get. The file travelled to the instance inside the tool's package, which is why it had to be kept next to the tool.

**The agent.** Open `agents/civic_info_agent.yaml`. Under `tools`, three names. The instructions have a new paragraph: use a tool for any question about one resident's application, report or street; ask for the number when it is missing; say when a record is unknown. The chapter 4 line that forbade looking anything up is gone. The facts of chapter 4 and the knowledge base of chapter 5 are still there, and the three ways of knowing now sit side by side in one file: what the agent is told, what it reads, and what it looks up.

Bob may have added files of its own, such as a requirements file for each tool or a test report. They are not part of the agent on the instance; read them if you are curious, and ignore them otherwise.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 6.8 Try it, and read the reasoning

A question sent through Bob reaches the agent in Draft, as in chapter 5. The agent deployed in Live still knows nothing about permit numbers until 6.9.

**Using Bob.** Ask the three questions from the Overview, one per message:

```
Ask civic_info_agent: "Where is my permit application PP-2026-0412?"
```

```
Ask civic_info_agent: "Has my pothole report RQ-2026-1187 been scheduled?"
```

```
Ask civic_info_agent: "Which day is the grey bin collected on Elm Street?"
```

Read each answer with your records of 6.3 next to you. The application is under review, with a decision due by 12 October. The pothole repair is scheduled for 9 October. The grey bin on Elm Street is collected on Monday. Each answer ends with the department's contact, because the instructions ask for it.

Then ask as residents do:

- A question without a number: "Where is my permit application?" The agent asks for the permit number.
- A number that does not exist: "Where is my permit application PP-2026-9999?" The agent says that it has no record under that number and gives the contact of Permits and Planning. Nothing is invented.
- A question that needs a tool and a document: "My application PP-2026-0412 is for a shed. Can I start building while I wait?" The agent looks up the application, under review, and finds in the building permit guide that work must not start before the decision. One answer, two sources.
- A question that needs a tool and the facts: "The grey bin on Elm Street was not collected today. Who do I call?" Monday was the day, and the contact is Waste and Recycling.

**From watsonx Orchestrate, with the reasoning.** Open your instance in the browser, go to Manage agents, select Utopia city information, and use the preview panel, which talks to the agent in Draft. Type the first question, about PP-2026-0412. With the answer, the chat offers to show how the agent got there. Open it. You see the steps: the agent decided to call `get_permit_status`, passed `PP-2026-0412` as the permit number, received the record, and wrote the answer from it. Now type the shed question of the previous list and open the steps again: a tool call, then a search of the knowledge base, then the answer.

This is the view you come back to whenever an agent with tools answers wrongly. If the agent called the wrong tool, the description of a tool is unclear. If it called the right tool with a wrong value, the parameter description is unclear. If it called nothing, the instructions do not say when to use a tool. Each of these is corrected with one sentence to Bob, as in 4.9.

## 6.9 Deploy the change in Live

Mode: Agent, same conversation.

The agent that looks up records exists in Draft. The agent deployed in Live still answers that a decision is given within 30 days. Deploy again:

```
Deploy civic_info_agent from draft to live.
```

Bob reports that the agent is deployed. Go to the watsonx Orchestrate chat and ask about PP-2026-0412: the resident of the Overview now gets the status of their application. On the Developer Edition, skip this step.

## 6.10 Summary

The agent can now answer questions that have a different answer for every resident: the status of an application, the date of a repair, the collection day of a street. Bob wrote the records, the tools and the change to the agent; you described the lookups, fixed the records, and read the agent's reasoning for the first time.

- A tool is a function that the agent calls while it answers, to fetch information or to act. The agent decides when to call it, from the tool's description and the question.
- The description and the parameter descriptions are written for the agent. They are the whole basis of its decision, and the first place to look when it decides wrongly.
- An agent can combine its sources in one answer: a tool for the resident's record, the knowledge base for the rule, the instructions for the contact.
- The agent's reasoning shows the steps between the question and the answer, including every tool call and its values. Read it to check an answer and to diagnose a wrong one.

The three tools read records; none of them changes anything. The next thing residents ask for is to report a pothole, not to check on one, and that means a tool that creates a record in the city's service desk, a service reached over an API with a key. That key must never appear in a chat, in a file in git or in a tool's code. In chapter 7, the agent gets a tool that reports an issue, and watsonx Orchestrate keeps the key for it: a connection.
