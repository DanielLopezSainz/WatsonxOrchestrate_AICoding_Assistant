# Chapter 3. How to work with Bob

Level: beginner. Time: about 30 minutes of reading; nothing is built. Prerequisites: none. The examples refer to the project folder from chapter 2.

## Overview

This chapter describes how to create agents in watsonx Orchestrate with Bob. The work follows Bob's three modes in turn: Ask mode to understand the request, Plan mode to write the design, Agent mode to build and test the agent. You approve the design before Bob builds it, and the deployment before an agent reaches its users. The chapter explains this workflow, then the prompts to use in each mode. The walkthroughs from chapter 4 on apply it without repeating it. In this guide, "the assistant" means Bob.

After completing this chapter, you can:

- Run an agent project through Bob's Ask, Plan and Agent modes in turn.
- Approve a design before Bob builds it, and know what to check before approving.
- Choose among five kinds of prompt and write each one.
- Rewrite a vague prompt into one that states the expected result and when Bob must stop.
- Explain what the files in the project folder tell Bob.

Skip this chapter if you already work with Bob in its three modes and write prompts that state the expected result and when Bob must stop. Section 3.3 describes the structured prompt used from chapter 5 on.

## 3.1 Bob proposed workflow

Bob is designed to do the work rather than to be supervised line by line. You describe the problem and take the decisions; Bob writes the files, imports and tests them, and reports the result, including failures. Three recommendations follow from this.

- Plan first. Always start new projects or complex features in Plan mode, so that a plan exists before anything is built. It prevents breaking changes and gives the work a clear direction.
- One task per conversation. Start new tasks regularly with specific aims, and reference files with @ mentions instead of pasting them. Before implementing a plan, start a new conversation, so that the planning discussion does not consume the context and Bob does not conflate planning and implementation.
- Approve according to risk. There are three approval strategies: manual approval of every action, auto-approval of specific actions, and a hybrid that auto-approves low-risk actions and asks for the rest. Chapter 2 set up the hybrid.

The mode is what makes this possible. A mode determines what Bob is allowed to do in a conversation, and Bob provides three.

### Ask mode

Ask mode is for asking questions and getting explanations. Bob can read your files, use the connected servers, which for Orchestrate means looking at your instance and searching the documentation, and load skills. It cannot write files or run commands. Use it when you need explanations or information without making changes.

In this guide, every agent project starts in Ask mode: Bob restates the request, looks at what exists on the instance, and asks its questions. Bob's standard workflow starts new work in Plan mode; this guide adds a read-only step in front, because Plan mode can already write files and the first contact with a request should change nothing.

### Plan mode

Plan mode plans tasks: it analyses requirements, researches, and designs the implementation steps. Bob can do everything Ask mode can, and write files; it still cannot run commands. In Plan mode, Bob asks clarifying questions, asks your approval before writing the plan files, and writes them into the project as Markdown. You review the plan for three things: that its scope matches your request, that it names concrete files rather than using vague language, and that nothing is missing. You ask for revisions in the same conversation.

In this guide, the plan is a design document written into the `design` folder, and it is what you approve before Bob builds.

### Agent mode

Agent mode takes an idea or a plan and implements it. Bob has every capability: read, write, run commands, use the servers, switch modes, delegate to subagents. Use it for implementing features, fixing bugs, and any task that modifies files. Enter it with a new conversation and a prompt that points at the plan with an @ mention.

In this guide, Agent mode is where Bob writes the definition and tool files, imports them, tests the agent, reads its reasoning, fixes what failed, and reports.

### Switching modes

There are four ways: the dropdown to the left of the chat input; the shortcut `⌘ .` on a Mac or `Ctrl .` elsewhere; accepting a switch Bob proposes when it notices the request needs another mode; and Bob switching by itself during a task when the work evolves. The slash commands `/ask`, `/plan` and `/agent` typed in the chat do the same as the dropdown.

The three modes as this guide uses them:

| Mode | Used to | Bob can | Ends with |
|---|---|---|---|
| Ask | Understand the request | Read files, look at the instance, search the documentation | Restatement, questions, inventory of the instance |
| Plan | Write the design | The above, plus write files | A design document, awaiting your approval |
| Agent | Build and test | Everything | Artifacts in draft on the instance, a test transcript, a report |

## 3.2 The two approvals

You approve twice in every agent project: the design, before Bob builds it, and the deployment, before an agent reaches its users.

The design approval comes between Plan mode and Agent mode. You approve a list: which agents exist and what each is for, which tools each has, which systems need a connection, which documents become knowledge, and the build order. If you cannot explain that list to a colleague from the file alone, send it back with your questions. When it is right, the approval is one line. Build starts in a new conversation, so in chapter 4 that line, with the design file mentioned, is the whole Build prompt.

The deployment approval comes when the agent is built and tested. Everything Bob creates lands in the draft environment of the instance. Nothing reaches end users until an agent is deployed, and deploying is done with an ADK command that Bob never runs on its own; chapter 11 shows it. Before that command, the active environment may have to be switched to the right tenant, and that switch affects every assistant on your machine at once, which is one more reason to make it an explicit decision.

IMPORTANT: the instructions file in the project folder tells Bob never to deploy, switch environment, set a credential or remove anything without asking you first. If Bob does one of those things without asking, the file is not being read; go through the checklist in section 2.6.

Between the two approvals, let Bob work. Approving every file in Agent mode removes its benefit; control comes from the checks in 3.4.

## 3.3 The types of prompts

A prompt is what you type in the chat. This guide uses five kinds; each fits a situation, and choosing the right kind matters more than the wording.

Four rules from Bob's documentation apply to all of them: be specific, since vague prompts produce vague output; show an example of the output when its format matters; refer to files with @ mentions instead of pasting their content; and plan before building.

### Type 1: the question

A question asks Bob to find something out and report, without changing anything. "Which agents exist on my instance?", "Why did the last test answer that the order was unknown?"

Use it to understand your project or your instance, to understand why something happened, or to check what Bob understood before giving it work. Questions belong in Ask mode, where Bob cannot act.

Limits: nothing gets built, and the answer is only as good as what Bob read. Name the file or the test you want it to look at; otherwise it answers from memory.

```
Chat with lab_order_agent asking "Where is order LL-1001?" with reasoning included.
Show every tool call and every tool result from the reasoning, exactly as
returned. If a result contains an error, quote it and say what caused it.
```

### Type 2: the brief

A brief describes what you want in your own words, as you would to a colleague. The watsonx Orchestrate accelerator for Bob starts a project this way:

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

The rule in one line: a good prompt is a use case brief, not a question. A complete brief answers six things; anything left out, Bob fills with a generic default. For an Orchestrate agent the six are:

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

Use a brief to start an agent project, in Ask mode. A brief that covers the six items gets few questions back; one that covers two or three, like the first prompt of chapter 4, gets the rest back as questions, which is appropriate when you are still deciding what you want.

Limits: it is only as clear as you are. Anything left out, Bob guesses, without saying so. The closing sentence depends on the mode: in Agent mode it is the only thing that stops Bob from building at once; in Ask mode the mode prevents building and the Ask-mode rules already ask for questions rather than a design, so the closing sentence only says what you want back.

### Type 3: the structured prompt

A structured prompt has parts, each answering one question Bob would otherwise guess. This guide uses six:

```
Goal:        what should exist when this is done, in one sentence
Context:     the files, folders and data to use, by name, with @ mentions
Constraints: names to keep, the model to use, what not to touch
Deliverable: what you want back: a file, an import, a chat transcript, a report
Verify:      how Bob proves that it worked, in a way you can check yourself
Stop:        when Bob should ask you instead of guessing
```

The labels are for you, not for Bob. They are a checklist so that you do not forget to state the expected result and when Bob must stop; Bob understands the same content written as plain sentences. Leave a part out when the project's rules or an approved design already say it: in chapter 4 the whole Build prompt is one line for that reason.

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

Use it in Agent mode, for anything that creates or changes something on the instance, when the check is specific to the task. Each part removes one reason for Bob to guess: Goal limits the work, Context names the data, Constraints keep names and settings, Deliverable says what to return, Verify gives a check you can repeat, Stop says what to do when unsure.

Limits: it takes longer to write, and you need the names of files, agents and tools to fill it in. It is not the right type while you are still exploring.

### Type 4: the specification prompt

A specification prompt asks for one file and lists what the file must contain. The Planning Analytics workshop for Bob uses it to write agent definitions:

```
Generate a ready-to-import agent YAML with these properties:
- name: lab_order_agent
- description: answers questions about the shipping status of customer orders
- llm: groq/openai/gpt-oss-120b
- style: react_core
- no tools or collaborators yet, they are added in the next step
Follow the spec_version v1, kind native schema. Return only the YAML.
```

Use it for small artifacts whose design is already approved and whose fields you know. "Return only the YAML" avoids a page of explanation.

Limits: it produces the file and nothing else; importing and testing are separate prompts. It skips the design conversation, so it is not for a new agent.

### Type 5: the follow-up

A follow-up is a short correction inside a conversation that is already going: "Use LL-1003 as the example instead", "Shorter, under 100 words", "You changed the agent's name; put it back". Bob's documentation calls this iterating.

Use it to adjust a result you mostly like. It is the fastest type, because the context is already in the conversation.

Limits: it works while the conversation is short. After many follow-ups Bob loses track of earlier constraints; start a new conversation with a complete prompt and the current files mentioned. Three follow-ups on the same problem mean the original prompt was missing something: rewrite it instead of sending a fourth.

### Choosing the type

| You want to | Type | Bob mode |
|---|---|---|
| Understand something, or check what Bob understood | Question | Ask |
| Start an agent project, explore, get a first proposal | Brief, ending with what you want back | Ask, then Plan |
| Revise a design | Structured, or a follow-up if the change is small | Plan |
| Create or change anything on the instance | Structured, or one line when the design and the rules carry the rest | Agent |
| Get one file whose contents you already know | Specification | Plan or Agent |
| Adjust a result you mostly like | Follow-up | The mode you are in |

Whatever the type, a prompt that asks Bob to do something must state two things: the expected result, and when Bob should stop and ask. The brief states them in its last lines, the structured prompt in Verify and Stop, the specification in "return only the file". Most unexpected results come from prompts that omit them.

## 3.4 Keeping control in Agent mode

Three checks, all required by the rules in the project folder, keep Agent mode under control without approving every step.

- Verify after every change. Bob looks at the instance after each import, because the platform sometimes reports success when it has logged an error.
- Read the reasoning when testing. Tool calls and their real results appear there, and a polite final answer can hide a runtime error.
- Restart the Orchestrate server before concluding that something is broken. Some failures are in the connection, not in your files; the restart control is in Bob's settings, MCP tab.

The walkthroughs show each check where it applies; chapter 15 collects the cases behind them.

## 3.5 How much to say

The walkthroughs ask less of you as they go. In chapter 4 you write one prompt per mode and read every operation Bob performs. In chapters 5 and 6 the Agent-mode prompt covers several artifacts and you check the result. From chapter 9 on, you describe the business need once, approve one design, and read the report.

Bob writes the YAML and the Python; you do not need to learn them. What you need to learn is when to be precise and when to delegate, and the way to learn it is to start precise and delegate more as you see what Bob gets right on its own. Chapter 4 is deliberately detailed.

## 3.6 Prompts, weak and better

A weak prompt and a better prompt for the same situation, one pair per type.

| Situation | Weak | Better | Why |
|---|---|---|---|
| Starting an agent project (brief) | "Build me a customer service agent for Lumen Logistics that can track orders, answer policy questions and give shipping quotes." typed in Agent mode | The six-item brief: three example user sentences, the data files and the existing tool named with @, the ten-tool limit, and "tell me what you understood, what you need to know, and what exists on the instance", in Ask mode | The weak prompt lets Bob guess the data, invent tools and import before you have seen a name |
| Adding one tool (structured) | "Add the order status tool to the agent." | The six-part prompt shown in 3.3 | The weak prompt names no file, no agent and no proof of success; Bob may create the tool from scratch, rename it, or report success as soon as the import returns |
| Investigating a failure (question) | "The agent does not work, fix it." | "Chat with lab_order_agent asking 'Where is order LL-1001?' with reasoning included. Show every tool call and result exactly as returned before proposing any change. Do not modify anything yet." | "Fix it" invites Bob to patch the first thing it sees; the evidence is in the reasoning and nowhere else |
| Asking for a single file (specification) | "Write me an agent YAML for order tracking." | The specification prompt shown in 3.3 | Every property is listed and the schema named; the weak prompt yields a plausible file with a made-up name |
| Adjusting a result (follow-up) | "That's not right, try again." | "The table is right but the answer is too long. Keep the table, remove the introduction, and keep the whole answer under 80 words." | "Try again" gives Bob nothing to change, so it changes something at random |

The better prompts have two things in common: they name real files instead of describing them, and they state what Bob should return and when it should stop. With those two, the rest of the wording can be as informal as you like.

Prompts to avoid:

| Prompt | Why it fails | What to write instead |
|---|---|---|
| "Build me a customer service agent" | Bob invents the users, the facts, the tools and the names | The six-item brief, in Ask mode |
| "Give it tools, a knowledge base and a few collaborators" | Every component is a place an answer can go wrong; with all of them at once, nothing can be traced | One component per iteration, as the walkthroughs do |
| "It does not work, fix it" | Bob patches the first thing it sees | Ask for the reasoning of the failing test first |
| "Make it production ready" | Everything Bob creates is a draft; deployment is a separate approval | Build and test in draft; deploy in chapter 11 |
| "Do not delete anything, ask before importing, verify afterwards" | Repeats what the rules in the project folder already require | Only what is specific to the task; the rules cover the rest |

## 3.7 The files behind the prompts

Bob reads a few files from the project folder at the start of every conversation. They are the reason the prompts in this guide are short. They came with the repository cloned in chapter 2; you do not edit them, and later chapters open them when a walkthrough needs to explain what they do.

| File | What it does |
|---|---|
| `AGENTS.md`, at the top of the folder | Describes the project to Bob: how the folders are organised, the naming rules, how to work with the instance, and which actions require asking you first |
| `.bob/rules-ask`, `.bob/rules-plan`, `.bob/rules-code` | One short file per mode, loaded when that mode is active: what an Ask-mode answer contains, what a design must let you judge, how a build is verified |
| `.bob/mcp.json` | Written by the extension in chapter 2: how Bob starts the Orchestrate server and the documentation server, and which folder it may work in |

One task per conversation. Ask mode and Plan mode share one conversation, because the design needs your answers; Agent mode starts a new one, with the design file mentioned. In long conversations Bob loses track of constraints it accepted earlier; Bob's documentation calls this context poisoning.

## 3.8 Keeping your work

The files Bob writes into the project folder, the designs and the definitions, are the result of your work. Keep them in git, so that any change can be undone and every version of an agent can be found again. The folder is a clone of the guide's repository, so git is already set up; what you need is a repository of your own to push to, because readers cannot write to the guide's repository.

Once, before the first commit: create an empty repository in your own git account, copy its address, and in Agent mode send:

```
Point this repository's origin at <the address you copied> and push the
current branch to it.
```

Bob shows the git commands and asks before running each; the first push asks for your git credentials, as any client does.

Then, at the end of every chapter:

```
Commit everything I changed with a short message saying what was built,
and push.
```

Bob composes the message and asks you to approve the commands. Files specific to your machine, the Python environment, the connection settings and `.env`, are ignored by git and never leave your computer. If you would rather click than type, the Source Control icon in the left bar does the same.
