# Chapter 3. How to work with Bob

Level: beginner. Time: about 20 minutes of reading. Prerequisites: none.

## Overview

What Bob builds depends on which mode you use for each step, when you approve, and what you write in a prompt. This chapter describes the workflow that the guide follows in every later chapter, with one Agent of the City of Utopia as the example throughout.

The workflow has three steps, one per Bob mode:

- Ask mode, to make sure that Bob has understood what you want before anything is written.
- Plan mode, to obtain a design that you read and approve.
- Agent mode, to build the Agent from the approved design and test it.

Sections 3.3 and 3.4 cover the three kinds of prompt; section 3.6 covers git.

What to read, depending on your experience:

| If you | Read | Skip |
|---|---|---|
| Have not used an AI assistant for work before | The whole chapter | Nothing |
| Use ChatGPT, Claude or a similar assistant, but not Bob | 3.1, 3.2 and 3.5, which are specific to Bob and to watsonx Orchestrate | 3.3 and 3.4, on writing prompts, and 3.6 if you know git |
| Already use Bob in its three modes | 3.2 and 3.5 | The other sections |

## 3.1 The recommended workflow

You describe the problem and take the decisions; Bob writes the files, imports and tests them, and reports the result, including failures. Follow these practices when you work with Bob:

- Start new projects and complex features in Plan mode, so that a plan exists before anything is built.
- Start a new conversation for each task, with a specific aim, and reference files with @ mentions instead of pasting their content. Before implementing a plan, start a new conversation, so that the planning discussion does not consume the context and Bob does not mix planning and implementation.
- Approve according to risk. Three strategies are available: manual approval of every action, auto-approval of specific actions, and a hybrid that auto-approves low-risk actions and requires approval for the rest. Chapter 2 configured the hybrid.

A mode determines what Bob is allowed to do in a conversation. Bob has three modes.

### Ask mode

Ask mode is for asking questions and getting explanations. In this mode, Bob can read files, use the connected servers, which for Orchestrate means querying the instance and searching the documentation, and load skills. Bob cannot write files or run commands; use Ask mode when you need information without making changes.

In this guide, every Agent project starts in Ask mode. Bob restates the request, lists what already exists on the instance, and asks the questions that must be answered before a design can be written. Bob's standard workflow starts new work in Plan mode, but this guide starts in Ask mode so that the request is understood before the design is written.

Example. The same Agent is used in all three modes below: an Agent that tells the residents of the City of Utopia which city department handles their question. In Ask mode, you write:

```
I would like to build an information agent for the residents of the City of
Utopia. It answers questions like "the street light on my street has been out
for a week, who do I tell?" from a fixed set of facts about three city departments. Tell me what
you understood, what you need to know from me, and what already exists on my
instance.
```

Bob queries the instance, then answers with three parts: what it understood, a table of the Agents, Tools and Connections that already exist, and a numbered list of questions, for example which facts it must know and what to answer when a question is outside the three departments. Nothing is written or created, and you answer the questions in the same conversation.

### Plan mode

Plan mode is for planning a task. Bob analyses the requirements, researches the project and designs the implementation steps. It can do everything that Ask mode allows, and it can also write files; it cannot run commands. It asks clarifying questions, requests your approval before writing the plan files, and writes them into the project as Markdown. Review the plan for three things: the scope matches your request, the plan names concrete files and avoids vague language, and nothing is missing. Request revisions in the same conversation.

Bob writes the plan as a design document in the `design` folder; you approve it before anything is built.

Example, continued. In the same conversation, you switch to Plan mode and write:

```
Write the design for this agent into design/civic-info-design.md.
```

After you approve writing the file, Bob writes it and shows a summary: what was asked, what exists on the instance, the proposed Agent with its name and model, the facts it will know, how it behaves, the build order, and the test questions with the expected answers. You read the file and, if something is missing, request a change in the same conversation; Bob revises the file and waits again.

### Agent mode

Agent mode is for implementing an idea or a plan. It has the fewest restrictions: Bob reads and writes files, runs commands, uses the servers, switches modes, and can delegate work to subagents. Reserve it for building: features, bug fixes, and anything that changes the instance. Start Agent mode in a new conversation, with a prompt that references the plan with an @ mention.

In this guide, Agent mode is where Bob writes the definition and Tool files, imports them, tests the Agent, reads the Agent's reasoning, corrects what failed, and reports.

Example, continued. You start a new conversation, switch to Agent mode, and write:

```
The design in @design/civic-info-design.md is approved. Build it.
```

Bob writes `agents/civic_info_agent.yaml`, asks for approval to import it, imports it, checks that the Agent appears on the instance, sends the test questions from the design to the Agent, and reports the answers. After this, the Agent exists in Draft on your instance; chapter 4 repeats every step, with the full output.

### Switching modes

You can switch modes in four ways:

- The mode dropdown at the bottom of the chat input, or the commands `/ask`, `/plan` and `/agent` typed in the chat.
- The shortcut `⌘ .` on a Mac or `Ctrl .` on Windows and Linux.
- Accepting a switch that Bob proposes when a request requires another mode.
- A switch that Bob performs itself during a task, which happens without a request only if Mode is switched on under the Permissions button.

The three modes as this guide uses them:

| Mode | Used to | Bob can | Result |
|---|---|---|---|
| Ask | Understand the request | Read files, query the instance, search the documentation | A restatement of the request, the open questions, an inventory of the instance |
| Plan | Write the design | The above, and write files | A design document, awaiting your approval |
| Agent | Build and test | Everything | The artifacts in Draft on the instance, a test transcript, a report |

## 3.2 What you approve, and when

You approve twice in every Agent project: the design, before Bob builds it, and the deployment, before an Agent reaches its users.

The design approval takes place between Plan mode and Agent mode. You approve a list: which Agents exist and what each one is for, which Tools each Agent has, which external systems need a Connection, which documents become knowledge, and the build order. If the list is not clear, return it to Bob with your questions. When the design is correct, the approval is one line. Agent mode starts in a new conversation, so in chapter 4 that line, with the design file referenced, is the complete prompt.

The deployment approval takes place when the Agent is built and tested. Every Agent, Tool and Knowledge Base that Bob imports is stored in the Draft environment of the instance. An Agent reaches its users only when it is deployed; deployment is done with an ADK command that Bob never runs on its own initiative. Chapter 4 performs it once, with a single instruction; chapter 11 describes it in full. If you built the Agent in the Developer Edition and deploy it to a SaaS tenant, the active environment must be switched to the tenant before the deployment. The switch affects Bob and any other coding assistant on the machine, so switch only when you mean to.

Example. In chapter 4, Bob writes the design for the city information Agent and waits for your approval. You read the file and notice that it says nothing about what a resident sees before typing a question. You write, in the same Plan-mode conversation:

```
Add a welcome message and two starter prompts to the design: the street light
question and the building permit question.
```

Bob revises the file and waits again. When the design is complete, you start a new conversation in Agent mode and write:

```
The design in @design/civic-info-design.md is approved. Build it.
```

This line is the design approval. Bob builds and tests the Agent, and the Agent exists in Draft. For the deployment approval, in chapter 11, you ask Bob to deploy the Agent; Bob shows the deployment command and asks for confirmation before running it. Until you confirm, the Agent is in Draft, where only the builders of the instance reach it.

IMPORTANT: deploying, switching environment, setting a credential and removing an artifact are not among the operations pre-approved in chapter 2, so Bob asks for approval before each of them. If Bob performs one of these actions without asking, the approval settings differ from chapter 2. Go through the checklist in section 2.7.

Between these two approvals, Bob requests approval for each file it writes and each command it runs, as chapter 2 configured; approve each request as it comes, and read the file that Bob proposes to import. After each import, ask Bob to list the artifacts on the instance and confirm that the new one appears; when testing, ask for the reasoning and read it.

## 3.3 The types of prompts

A prompt is the text that you type in the chat. This guide distinguishes three kinds by what they ask Bob to do: a question asks for information, an instruction asks for one action, and a structured prompt describes a task with several parts and states how to check the result. The names are for this guide; Bob does not know them.

The following practices apply to every prompt:

- Be specific, because Bob fills any gap with its own assumptions.
- Show an example of the output when its format matters.
- Refer to files with @ mentions instead of pasting their content.
- Plan before building.

### Type 1: the question

A question asks Bob for information. Examples:

```
Which tools does civic_info_agent have, and what does each one do?
```

```
Why did civic_info_agent answer that permit BP-2041 was unknown in the last test?
```

Use a question to understand the project or the instance, to find out why something happened, or to check what Bob understood before assigning it work. Questions belong in Ask mode, where Bob cannot make changes.

Name the file or the test that Bob must examine; otherwise, Bob may answer from its general knowledge.

### Type 2: the instruction

An instruction tells Bob to perform one action, in a plain imperative sentence. It has three typical uses.

To perform an action on the project or the instance:

```
Import agents/civic_info_agent.yaml into my instance.
```

```
Send the test questions from design/civic-info-design.md to civic_info_agent,
with reasoning, and show the answers next to the expected ones.
```

To request a file, listing what the file must contain:

```
Write the definition file for an agent named permits_agent that answers
questions about the status of building permit applications, with no tools yet.
Return only the file.
```

To correct Bob's previous answer, in a conversation that is already in progress:

```
Use permit BP-2043 as the example instead.
```

```
You changed the agent's name; put it back.
```

Use an instruction for a single action whose expected result is obvious from the action itself: an import, a test run, an export, a file, a change to the last answer. Instructions that change the instance belong in Agent mode, where Bob asks for approval before the operation. When requesting a file, add "Return only the file", so that Bob returns the file without an explanation.

For an action with several steps, or one whose result must be checked in a particular way, use a structured prompt. After many corrections in one conversation, Bob loses track of earlier constraints; in that case, start a new conversation with a complete prompt and references to the current files.

### Type 3: the structured prompt

A structured prompt is divided into parts, each answering one question that Bob would otherwise have to guess. It has two uses in this guide, with a template for each. The templates are checklists for the writer: the same content can be sent as labelled lines or as running text.

The first use is to describe what you want at the start of an Agent project, in Ask mode. The template answers six questions. A question left unanswered comes back from Bob as a question, or is settled by an assumption that Bob does not report.

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

A shorter form, with a title, a description, example prompts and the business value, is enough to open the conversation:

```
I would like to develop an AI agent with watsonx Orchestrate. Here is my use case:

Title: Permit status agent
Description: Answers residents' questions about the status of their building permit applications.
Example prompts:
  "Where is my permit application PP-2026-0412?"
  "How long does a permit review take?"
Value: fewer calls to the Permits and Planning desk about applications in progress

Please propose the agent, tools, knowledge base and connections first
and wait for my approval before making changes.
```

The first prompt of chapter 4 answers only two or three of the six questions, and Bob asks the rest.

The second use is to specify a task in Agent mode, when the task creates or changes something on the instance and the check is specific to the task. The template has six parts:

```
Goal:        what must exist when the task is done, in one sentence
Context:     the files, folders and data to use, by name, with @ mentions
Constraints: names to keep, the model to use, what not to change
Deliverable: what Bob must return: a file, an import, a chat transcript, a report
Verify:      how Bob proves that the task worked, in a way that you can repeat
Stop:        the condition under which Bob must ask you instead of continuing
```

Example, for the permit Tool of chapter 6, written as if no design existed:

```
Goal: the permit status tool exists on the instance and civic_info_agent can call it.
Context: @tools/get_permit_status.py and @agents/civic_info_agent.yaml.
Constraints: import the tool from that file. Keep the name get_permit_status.
  Add one paragraph to the agent's instructions saying when to call it; change
  nothing else.
Deliverable: the tool imported, the agent re-imported, and one chat asking
  "Where is my permit application PP-2026-0412?" with reasoning included.
Verify: the list of tools shows get_permit_status with permit_number in its input
  schema, and the chat reasoning shows one call to it returning "under review".
Stop: if the import returns an error, show me the exact text and wait.
```

Verify and Stop are recommended for any prompt that changes the instance. Omit a part when an approved design already states it; in chapter 4, the Agent-mode prompt is a single instruction for this reason.

## 3.4 Prompts, weak and better

A weak prompt does not name the files, the Agent or the data involved, and does not state the expected result; Bob fills the gaps with choices of its own. A better prompt references the files with @ mentions, names the Agent and the data, and states what Bob must return and, where the change matters, how to check it.

The following table shows a weak prompt and a better prompt for the same situation.

| Situation | Weak | Better | Why |
|---|---|---|---|
| Starting an Agent project (structured prompt) | "Build me a citizen services agent for the City of Utopia that can track permits, answer questions about regulations and take problem reports.", typed in Agent mode | The structured prompt with the six questions: three example user sentences, the data files and the existing Tool referenced with @, and "Tell me what you understood, what you need to know, and what exists on the instance", in Ask mode | The weak prompt leaves Bob to assume the data, invent Tools and import before you have seen a name |
| Running a test (instruction) | "Test the agent." | "Send the test questions from design/civic-info-design.md to civic_info_agent, with reasoning, and show the answers next to the expected ones." | "Test the agent" leaves Bob to choose the questions and the way to report. The better prompt names the questions, the Agent and the form of the answer |
| Adding one Tool (structured prompt) | "Add the permit status tool to the agent." | The six-part prompt shown in 3.3 | The weak prompt names neither a file nor an Agent, and gives no proof of success. Bob might create the Tool from scratch, rename it, or report success as soon as the import returns |
| Investigating a failure (question) | "The agent does not work, fix it." | "Why did civic_info_agent answer that permit BP-2041 was unknown in the last test? Look at the reasoning of that test and tell me which tool was called and what it returned." | "Fix it" leads Bob to change the first thing it finds. The question asks for the cause first, and the reasoning is where to look for it |
| Requesting a file (instruction) | "Write me an agent definition for permit tracking." | The file request shown in 3.3, with the Agent's name, purpose and Tools listed, ending "Return only the file" | The name, the purpose and the Tools are stated. The weak prompt produces a plausible file with an invented name |
| Correcting a previous answer (instruction) | "That's not right, try again." | "The table is right but the answer is too long. Keep the table, remove the introduction, and keep the whole answer under 80 words." | "Try again" gives Bob nothing to change, so it guesses what was wrong |

Prompts to avoid:

| Prompt | Why it fails | What to write instead |
|---|---|---|
| "Build me a citizen services agent" | Bob invents the users, the facts, the Tools and the names | The structured prompt with the six questions, in Ask mode |
| "Give it tools, a knowledge base and a few collaborators" | Each component is a possible cause of a wrong answer. With several added together, finding the cause takes much longer | One component per iteration, as the walkthroughs do |
| "It does not work, fix it" | Bob guesses what is wrong and changes that | Request the reasoning of the failing test first |
| "Make it production ready" | The prompt names no check that Bob can perform, and what Bob builds stays in Draft until you deploy it | Build and test in Draft; deploy in chapter 11 |

## 3.5 What Bob reads from the project folder

Two items in the project folder, both written by the watsonx Orchestrate ADK extension in chapter 2, are available to Bob in every conversation: the settings file `.bob/mcp.json`, from which Bob starts the Orchestrate server and the documentation server and which sets the folder that Bob can work in, and the Orchestrate skills in `.bob/skills`, which Bob activates when a task matches their description. Neither needs editing.

Bob does not read the other files of the project automatically. Reference a file with an @ mention when Bob must read it, for example the design file in an Agent-mode prompt.

Use one conversation per task. Ask mode and Plan mode share one conversation, because the design needs your answers; Agent mode uses a separate conversation with the design file referenced, because over a long exchange Bob loses track of constraints that it accepted earlier.

## 3.6 Bob with Git

Git keeps a history of the files that Bob writes into the project folder, the designs and the definitions, one version per commit. Bob runs the git commands: you describe the operation in a sentence, in Agent mode, and Bob shows the command it is about to run and asks for your approval. When you do not specify a commit message, Bob writes one from the files that changed.

The project folder is already a git repository, because it is a clone of the guide's repository. One thing is needed before the first commit: a repository of your own to push to, because readers cannot write to the guide's repository. Create an empty repository in your git account, copy its address, and send:

```
Rename the remote named origin to guide. Add <the address you copied> as the
new origin and push the current branch to it, setting it as the upstream.
```

After this, your work is saved to your own repository, named `origin`, and the guide's repository remains available under the name `guide`, so that you can still receive updates to the chapters. The first push asks for your git credentials, once.

After that, the following requests cover daily use. Each one is a plain instruction, and Bob asks for approval before each command it runs.

| You want to | Send |
|---|---|
| Save your work | `Commit everything I changed with a short message saying what was built, and push.` |
| Save only some files | `Commit the files in the design folder with the message "City information agent design v2" and push.` |
| See what changed since the last save | `Show me which files changed since the last commit and summarise the changes.` |
| See the history | `List the last ten commits with their dates and messages.` |
| Get the latest version of the guide | `Merge the main branch of the remote named guide into my current branch. Do not rebase.` |
| Discard the uncommitted changes to a file | `Restore agents/civic_info_agent.yaml to the version in the last commit.` |
| See an earlier version of a file | `Show me what agents/civic_info_agent.yaml looked like three commits ago.` |
| Work on a change without touching the main version | `Create a branch named roads-hours and switch to it.` |
| Bring a finished branch back | `Switch to the main branch and merge roads-hours into it, then push.` |

If a merge produces conflicts, Bob stops and reports them instead of continuing. The guide only ever changes the `guide` and `walkthroughs` folders and the README, and your work lives in the other folders, so a conflict arises only if you edit a chapter file in your clone. Keep notes outside the `guide` folder.

Files that are specific to your machine, the Python environment, Bob's settings folder and `.env`, are ignored by git and are not committed. The Source Control view, described in section 2.3, provides the same operations by clicking.
