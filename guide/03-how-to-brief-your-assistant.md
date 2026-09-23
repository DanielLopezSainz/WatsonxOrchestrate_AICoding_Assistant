# Chapter 3. How to work with Bob

Level: beginner. Time: about 30 minutes of reading. Prerequisites: none. The examples refer to the project folder from chapter 2.

## Overview

This chapter describes how to create agents in watsonx Orchestrate with Bob. The work follows Bob's three modes in turn: Ask mode to understand the request, Plan mode to write the design, and Agent mode to build and test the agent. You approve the design before Bob builds it, and you approve the deployment before an agent reaches its users. The chapter describes this workflow and the prompts to use in each mode. The walkthroughs from chapter 4 onwards apply the workflow without repeating it. In this guide, "the assistant" means Bob.

After completing this chapter, you can:

- Run an agent project through Bob's Ask, Plan and Agent modes.
- Review a design before approving it.
- Choose among three kinds of prompt and write each one.
- Rewrite a vague prompt so that it states the expected result and the condition under which Bob must stop.
- Describe the purpose of the files that Bob reads from the project folder.

Skip this chapter if you already work with Bob in its three modes and your prompts state the expected result and the stopping condition. Section 3.3 describes the structured prompt that is used from chapter 5 onwards.

## 3.1 Bob proposed workflow

Bob is designed to do the work rather than to be supervised line by line. You describe the problem and take the decisions. Bob writes the files, imports and tests them, and reports the result, including failures. Three recommendations follow from this design.

- Plan first. Start new projects and complex features in Plan mode, so that a plan exists before anything is built. A plan prevents breaking changes and gives the work a clear direction.
- One task per conversation. Start a new conversation for each task, with a specific aim, and reference files with @ mentions instead of pasting their content. Before implementing a plan, start a new conversation, so that the planning discussion does not consume the context and Bob does not mix planning and implementation.
- Approve according to risk. Three approval strategies are available: manual approval of every action, auto-approval of specific actions, and a hybrid that auto-approves low-risk actions and requires approval for the rest. Chapter 2 configured the hybrid.

A mode determines what Bob is allowed to do in a conversation. Bob provides three modes.

### Ask mode

Ask mode is for asking questions and getting explanations. In this mode, Bob can read files, use the connected servers, which for Orchestrate means querying the instance and searching the documentation, and load skills. Bob cannot write files or run commands. Use Ask mode when you need information without making changes.

In this guide, every agent project starts in Ask mode. Bob restates the request, lists what already exists on the instance, and asks the questions that must be answered before a design can be written. Bob's standard workflow starts new work in Plan mode. This guide adds a read-only step before it, because Plan mode can write files and the first exchange about a request must not change anything.

Example. The same agent is used in all three modes below: a helpdesk agent that tells Lumen Logistics employees whom to contact for IT, HR and Facilities questions. In Ask mode, you write:

```
I would like to build an internal helpdesk agent for Lumen Logistics employees.
It answers questions like "my badge does not open the door, who do I call?"
from a fixed set of facts about three teams. Tell me what you understood,
what you need to know from me, and what already exists on my instance.
```

Bob queries the instance, then answers with three parts: what it understood, a table of the agents, tools and connections that already exist, and a numbered list of questions, for example which facts it must know and what to answer when a question is outside the three teams. Nothing is written and nothing is created. You answer the questions in the same conversation.

### Plan mode

Plan mode is for planning a task: Bob analyses the requirements, researches the project, and designs the implementation steps. In this mode, Bob can do everything that Ask mode allows and can also write files. Bob cannot run commands. Bob asks clarifying questions, requests your approval before writing the plan files, and writes them into the project as Markdown. Review the plan for three things: the scope matches your request, the plan names concrete files rather than using vague language, and nothing is missing. Request revisions in the same conversation.

In this guide, the plan is a design document written into the `design` folder. This document is what you approve before Bob builds.

Example, continued. In the same conversation, you switch to Plan mode and write:

```
Write the design for this agent into design/helpdesk-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary: what was asked, what exists on the instance, the proposed agent with its name and model, the facts it will know, how it behaves, the build order, and the test questions with the expected answers. You read the file and, if something is missing, request a change in the same conversation; Bob revises the file and waits again.

### Agent mode

Agent mode is for implementing an idea or a plan. In this mode, Bob has every capability: read and write files, run commands, use the servers, switch modes, and delegate work to subagents. Use Agent mode for implementing features, fixing bugs, and any task that modifies files. Start Agent mode in a new conversation, with a prompt that references the plan with an @ mention.

In this guide, Agent mode is where Bob writes the definition and tool files, imports them, tests the agent, reads the agent's reasoning, corrects what failed, and reports.

Example, continued. You start a new conversation, switch to Agent mode, and write:

```
The design in @design/helpdesk-design.md is approved. Build it.
```

Bob writes `agents/lumen_helpdesk_agent.yaml`, asks for approval to import it, imports it, checks that the agent appears on the instance, sends the test questions from the design to the agent, and reports the answers. The agent now exists in draft on your instance. Chapter 4 runs this example in full.

### Switching modes

You can switch modes in four ways: the dropdown to the left of the chat input; the shortcut `⌘ .` on a Mac or `Ctrl .` on Windows and Linux; accepting a switch that Bob proposes when a request requires another mode; and an automatic switch by Bob during a task when the work requires it. The commands `/ask`, `/plan` and `/agent`, typed in the chat, have the same effect as the dropdown.

The three modes as this guide uses them:

| Mode | Used to | Bob can | Result |
|---|---|---|---|
| Ask | Understand the request | Read files, query the instance, search the documentation | A restatement of the request, the open questions, an inventory of the instance |
| Plan | Write the design | The above, and write files | A design document, awaiting your approval |
| Agent | Build and test | Everything | The artifacts in draft on the instance, a test transcript, a report |

## 3.2 What you approve, and when

You approve twice in every agent project: the design, before Bob builds it, and the deployment, before an agent reaches its users.

The design approval takes place between Plan mode and Agent mode. You approve a list: which agents exist and what each one is for, which tools each agent has, which external systems need a connection, which documents become knowledge, and the build order. If the list is not clear enough to explain to a colleague, return it to Bob with your questions. When the design is correct, the approval is one line. Agent mode starts in a new conversation, so in chapter 4 that line, with the design file referenced, is the complete prompt.

The deployment approval takes place when the agent is built and tested. Everything that Bob creates is stored in the draft environment of the instance. Nothing reaches end users until an agent is deployed. Deployment is done with an ADK command that Bob never runs on its own initiative; chapter 11 describes it. Before that command, the active environment might have to be switched to the target tenant. The switch affects every assistant on the machine, which is one more reason to make it an explicit decision.

Example. In chapter 4, Bob writes the design for the helpdesk agent and ends with "Waiting for your approval before building." You read the file and notice that it says nothing about what an employee sees before typing a question. You write, in the same Plan-mode conversation:

```
Add a welcome message and two starter prompts to the design: the badge
question and the password question.
```

Bob revises the file and waits again. When the design is complete, you start a new conversation in Agent mode and write:

```
The design in @design/helpdesk-design.md is approved. Build it.
```

This line is the design approval. Bob builds and tests the agent, and the agent exists in draft. For the deployment approval, in chapter 11, you ask Bob to deploy the agent; Bob shows the deployment command and asks for confirmation before running it. Until you confirm, the agent is visible to you and to nobody else.

IMPORTANT: the instructions file in the project folder tells Bob never to deploy, switch environment, set a credential or remove anything without asking you first. If Bob performs one of these actions without asking, the file is not being read. Go through the checklist in section 2.6.

Between these two approvals, let Bob work. Approving every file in Agent mode removes the benefit of the mode; the rules in the project folder require Bob to verify each import and to read the agent's reasoning when testing.

## 3.3 The types of prompts

A prompt is the text that you type in the chat. There is no official classification of prompts. This guide distinguishes three kinds by what they ask Bob to do: a question asks for information, an instruction asks for one action, and a structured prompt asks for a piece of work and states how to check it. The names are descriptive, not terms that Bob recognises.

The following practices apply to every prompt:

- Be specific. Vague prompts produce vague output.
- Show an example of the output when its format matters.
- Refer to files with @ mentions instead of pasting their content.
- Plan before building.

### Type 1: the question

A question asks Bob for information. Examples:

```
Which tools does lab_order_agent have, and what does each one do?
```

```
Why did lab_order_agent answer that order LL-1001 was unknown in the last test?
```

Use a question to understand the project or the instance, to find out why something happened, or to check what Bob understood before assigning it work. Questions belong in Ask mode, where Bob cannot make changes.

Name the file or the test that Bob must examine; otherwise, Bob answers from its general knowledge.

### Type 2: the instruction

An instruction tells Bob to perform one action, in a plain imperative sentence. It is the most common prompt in daily use. It has three typical uses.

To perform an action on the project or the instance:

```
Import agents/lumen_helpdesk_agent.yaml into my instance.
```

```
Send the four test questions from design/helpdesk-design.md to lumen_helpdesk_agent,
with reasoning, and show the answers next to the expected ones.
```

To request a file, listing what the file must contain. This form is used in the Planning Analytics workshop for Bob to obtain agent definitions:

```
Write the definition file for an agent named lab_order_agent that answers
questions about the shipping status of customer orders, with no tools yet.
Return only the file.
```

To correct Bob's previous answer, in a conversation that is already in progress:

```
Use LL-1003 as the example instead.
```

```
You changed the agent's name; put it back.
```

Use an instruction for a single action whose expected result is obvious from the action itself: an import, a test run, an export, a file, a change to the last answer. Instructions that change the instance belong in Agent mode, where Bob asks for approval before the operation. When requesting a file, the instruction "Return only the file" prevents an explanation that you do not need.

For an action with several steps, or one whose result must be checked in a particular way, use a structured prompt. After many corrections in one conversation, Bob loses track of earlier constraints; in that case, start a new conversation with a complete prompt and references to the current files.

### Type 3: the structured prompt

A structured prompt is divided into parts, each answering one question that Bob would otherwise have to guess. It has two uses in this guide, with a template for each. The templates are checklists for the writer: Bob does not define them, none of their parts is mandatory, and Bob reads the content and not the labels. The same content can be written as labelled lines or as running text.

To describe what you want at the start of an agent project, in Ask mode. The template answers six questions. For any question left unanswered, Bob makes an assumption and does not report it.

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

The watsonx Orchestrate accelerator for Bob uses a shorter form of the same idea, with a title, a description, example prompts and the business value:

```
I would like to develop an AI agent with watsonx Orchestrate. Here is my use case:

Title: Market analysis agent
Description: Tracks financial news, analyzes historical data, and forecasts trends.
Example prompts:
  "What's the recent trend in tech stocks?"
  "How has IBM's stock performed over the last week?"
Value: productivity improvement of a financial advisor by 10%

Please propose the agent, tools, knowledge base and connections first
and wait for my approval before making changes.
```

A description that answers the six questions receives few questions back from Bob. A description that answers two or three, like the first prompt of chapter 4, receives the others as questions, which is appropriate when the requirements are not yet settled.

To specify a task in Agent mode, when the task creates or changes something on the instance and the check is specific to the task. The template has six parts:

```
Goal:        what must exist when the task is done, in one sentence
Context:     the files, folders and data to use, by name, with @ mentions
Constraints: names to keep, the model to use, what not to change
Deliverable: what Bob must return: a file, an import, a chat transcript, a report
Verify:      how Bob proves that the task worked, in a way that you can repeat
Stop:        the condition under which Bob must ask you instead of continuing
```

Example, from the Agent-mode step of chapter 5:

```
Goal: the order status tool exists on the instance and lab_order_agent can call it.
Context: @lab/tools/lab_get_order_status.py and @agents/lab_order_agent.yaml.
Constraints: import the tool from that file. Keep the name lab_get_order_status.
  Do not change the agent's instructions.
Deliverable: the tool imported, the agent re-imported, and one chat asking
  "Where is order LL-1001?" with reasoning included.
Verify: the list of tools shows lab_get_order_status with order_id in its input
  schema, and the chat reasoning shows one call to it returning "in transit".
Stop: if the import returns an error, show me the exact text and wait.
```

Each part removes one reason for Bob to guess: Goal limits the work, Context names the data, Constraints preserve names and settings, Deliverable states what to return, Verify provides a repeatable check, and Stop defines when to ask. Verify and Stop are recommended for any prompt that changes the instance. Omit a part when the rules in the project folder or an approved design already state it; in chapter 4, the Agent-mode prompt is a single instruction for this reason.


## 3.4 Prompts, weak and better

A weak prompt leaves Bob to make assumptions: it does not name the files, the agent or the data involved, and it does not state the expected result. Bob completes the missing information with its own choices and does not report them. A better prompt supplies that information: it references the files with @ mentions, names the agent and the data, and states what Bob must return and, where the change matters, how to check it.

The following table shows a weak prompt and a better prompt for the same situation.

| Situation | Weak | Better | Why |
|---|---|---|---|
| Starting an agent project (structured prompt) | "Build me a customer service agent for Lumen Logistics that can track orders, answer policy questions and give shipping quotes.", typed in Agent mode | The structured prompt with the six questions: three example user sentences, the data files and the existing tool referenced with @, the ten-tool limit, and "Tell me what you understood, what you need to know, and what exists on the instance", in Ask mode | The weak prompt leaves Bob to assume the data, invent tools and import before you have seen a name |
| Running a test (instruction) | "Test the agent." | "Send the four test questions from design/helpdesk-design.md to lumen_helpdesk_agent, with reasoning, and show the answers next to the expected ones." | "Test the agent" leaves Bob to choose the questions and the way to report. The better prompt names the questions, the agent and the form of the answer |
| Adding one tool (structured prompt) | "Add the order status tool to the agent." | The six-part prompt shown in 3.3 | The weak prompt names no file, no agent and no proof of success. Bob might create the tool from scratch, rename it, or report success as soon as the import returns |
| Investigating a failure (question) | "The agent does not work, fix it." | "Why did lab_order_agent answer that order LL-1001 was unknown in the last test? Look at the reasoning of that test and tell me which tool was called and what it returned." | "Fix it" leads Bob to change the first thing it finds. The question asks for the cause first, and the cause is in the reasoning |
| Requesting a file (instruction) | "Write me an agent definition for order tracking." | The file request shown in 3.3, with the agent's name, purpose and tools listed, ending "Return only the file" | Every property is listed. The weak prompt produces a plausible file with an invented name |
| Correcting a previous answer (instruction) | "That's not right, try again." | "The table is right but the answer is too long. Keep the table, remove the introduction, and keep the whole answer under 80 words." | "Try again" gives Bob nothing to change, so it changes something arbitrary |

The better prompts have two properties in common: they reference real files instead of describing them, and they state what Bob must return and when it must stop. With these two properties, the rest of the wording can be informal.

Prompts to avoid:

| Prompt | Why it fails | What to write instead |
|---|---|---|
| "Build me a customer service agent" | Bob invents the users, the facts, the tools and the names | The structured prompt with the six questions, in Ask mode |
| "Give it tools, a knowledge base and a few collaborators" | Each component is a possible cause of a wrong answer. With several added together, the cause cannot be traced | One component per iteration, as the walkthroughs do |
| "It does not work, fix it" | Bob changes the first thing it finds | Request the reasoning of the failing test first |
| "Make it production ready" | Everything that Bob creates is a draft. Deployment is a separate approval | Build and test in draft; deploy in chapter 11 |
| "Do not delete anything, ask before importing, verify afterwards" | Repeats what the rules in the project folder already require | Only what is specific to the task; the rules cover the rest |

## 3.5 The files that Bob reads

Bob reads a few files from the project folder at the start of every conversation. These files are the reason the prompts in this guide are short. They are part of the repository cloned in chapter 2. You do not edit them. Later chapters open them when a walkthrough needs to explain what they do.

| File | Purpose |
|---|---|
| `AGENTS.md`, at the top of the folder | Describes the project to Bob: how the folders are organised, the naming rules, how to work with the instance, and which actions require asking you first |
| `.bob/rules-ask`, `.bob/rules-plan`, `.bob/rules-code` | One short file per mode, loaded when that mode is active: what an Ask-mode answer contains, what a design must include, how a build is verified |
| `.bob/mcp.json` | Written by the extension in chapter 2: how Bob starts the Orchestrate server and the documentation server, and which folder Bob can work in |

One task per conversation. Ask mode and Plan mode share one conversation, because the design needs your answers. Agent mode starts a new conversation, with the design file referenced. In long conversations, Bob loses track of constraints that it accepted earlier.

## 3.6 Keeping your work

The files that Bob writes into the project folder, the designs and the definitions, are the result of your work. Keep them in git, so that any change can be undone and every version of an agent can be retrieved. The folder is a clone of the guide's repository, so git is already configured. You need a repository of your own to push to, because readers cannot write to the guide's repository.

Once, before the first commit, create an empty repository in your own git account, copy its address, and send this prompt in Agent mode:

```
Point this repository's origin at <the address you copied> and push the
current branch to it.
```

Bob shows the git commands and asks for approval before running each one. The first push asks for your git credentials.

At the end of every chapter, send:

```
Commit everything I changed with a short message saying what was built,
and push.
```

Bob composes the commit message and asks you to approve the commands. Files that are specific to your machine, the Python environment, the connection settings and `.env`, are ignored by git and never leave your computer. The Source Control icon in the left bar provides the same operations by clicking.
