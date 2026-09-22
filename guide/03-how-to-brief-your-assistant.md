# Chapter 3. How to work with Bob

Level: beginner. Time: about 30 minutes of reading; nothing is built. Prerequisites: none. The examples refer to the project folder from chapter 2.

## Overview

This chapter describes how to work with Bob on a piece of watsonx Orchestrate work: the three phases, the two points where you approve, and the prompts each phase needs. Every walkthrough from chapter 4 on follows this way of working without explaining it again. In this guide, "the assistant" means Bob.

After completing this chapter, you can:

- Split a piece of work into the Discover, Design and Build phases and run each one in the matching Bob mode.
- Identify the two points where Bob stops for your approval, and what you approve at each.
- Choose among five kinds of prompt and write each one.
- Rewrite a weak prompt so that it states what done looks like and when Bob must stop.
- Describe the files Bob reads at the start of every conversation and what each one does.

Skip this chapter if you already work with Bob in its three modes and write prompts that state the deliverable, the check and the stopping rule. Read 3.3 in any case: the structured prompt described there is used from chapter 5 on without further explanation.

## 3.1 IBM's way of working with Bob

Bob is designed to do the work, not to be supervised line by line. IBM's guidance divides the labour: you frame the problem and decide at a few points; Bob turns the intent into working artifacts, runs and tests them, and reports what happened, failures included. Three principles from IBM's documentation follow from that division.

- Plan first. "Always start complex projects or features in Plan mode" to produce a plan you can read before anything is built. IBM's reason: it prevents breaking changes and gives the work a clear direction.
- One task per conversation. "Start new tasks regularly with specific aims", and reference files with @ mentions instead of pasting them. Before implementing a plan, IBM's tutorial starts a new conversation on purpose, so that the planning discussion does not consume the context and Bob does not conflate planning and implementation.
- Approve in proportion to risk. IBM describes three strategies, manual approval of every action, auto-approval of specific actions, and a hybrid that auto-approves low-risk actions and confirms the rest. Chapter 2 set up the hybrid.

The instrument for all three is the mode. A mode decides what Bob is allowed to do in a conversation, and Bob ships with three.

### Ask mode

IBM's definition: "Ask questions and get explanations." Bob can read your files, use the connected servers, which for Orchestrate means looking at your instance and searching the documentation, and load skills. It cannot write files or run commands. IBM recommends it "when you need explanations or information without making changes".

In this guide, Ask mode is where every piece of work starts, as the Discover phase: Bob restates the request, looks at what exists on the instance, and asks its questions. IBM's own workflow starts new work in Plan mode; this guide adds a read-only step in front, because Plan mode can already write files and the first contact with a request should change nothing.

### Plan mode

IBM's definition: "Plans tasks: analyzes requirements, researches and designs implementation steps." Bob can do everything Ask mode can, and write files; it still cannot run commands. In IBM's tutorial, Plan mode asks clarifying questions, asks your approval before writing the plan files, and writes them into the project as Markdown. You review the plan for three things, that its scope matches your request, that it names concrete files rather than using vague language, and that nothing is missing, and you ask for revisions in the same conversation.

In this guide, Plan mode is the Design phase. The plan is a design document written into the `design` folder, and it is the object of the first approval.

### Agent mode

IBM's definition: "Take your idea, or plan, and bring it to life." Bob has every capability: read, write, run commands, use the servers, switch modes, delegate to subagents. IBM recommends it "for implementing features, fixing bugs, and any tasks requiring file modifications", and its tutorial enters it with a new conversation and a prompt that points at the plan with an @ mention.

In this guide, Agent mode is the Build phase: Bob writes the definition and tool files, imports them, tests the agent, reads its reasoning, fixes what failed, and reports.

### Switching modes

Four ways, all from IBM's documentation: the dropdown to the left of the chat input; the shortcut `⌘ .` on a Mac or `Ctrl .` elsewhere; accepting a switch Bob proposes when it notices the request needs another mode; and Bob switching by itself during a task when the work evolves. The slash commands `/ask`, `/plan` and `/agent` typed in the chat do the same as the dropdown.

The three phases of this guide, side by side with IBM's terms:

| This guide | Bob mode | Bob can | Ends with |
|---|---|---|---|
| Discover | Ask | Read files, look at the instance, search the documentation | Restatement, questions, inventory of the instance |
| Design | Plan | The above, plus write files | A design document, awaiting your approval |
| Build | Agent | Everything | Artifacts in draft on the instance, a test transcript, a report |

## 3.2 The two approval points

Bob stops and waits for you at two points. This guide calls them gates.

The first gate is between Design and Build. You approve a list: which agents exist and what each is for, which tools each has, which systems need a connection, which documents become knowledge, and the build order. If you cannot explain that list to a colleague from the file alone, send it back with your questions. When it is right, the approval is one line. Following IBM's workflow, Build starts in a new conversation, so in chapter 4 that line, with the design file mentioned, is the whole Build prompt.

The second gate is at the end of Build, before anything goes live. Everything Bob creates lands in the draft environment of the instance. Nothing reaches end users until an agent is deployed, and deploying is done with an ADK command that Bob never runs on its own; chapter 11 shows it. Before that command, the active environment may have to be switched to the right tenant, and that switch affects every assistant on your machine at once, which is one more reason to make it an explicit decision.

IMPORTANT: the instructions file in the project folder tells Bob never to deploy, switch environment, set a credential or remove anything without asking you first. If Bob does one of those things without asking, the file is not being read; go through the checklist in section 2.6.

Between the two gates, let Bob work. Approving every file during Build removes the benefit of Agent mode; control during Build comes from the checks in 3.4.

## 3.3 The types of prompts

A prompt is what you type in the chat. Five kinds are used in this guide; each fits a situation, and the choice matters more than the wording.

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

A brief describes what you want in your own words, as you would to a colleague. IBM's accelerator for Bob starts a project this way:

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

IBM's Bob training states the rule in one line: a good prompt is a use case brief, not a question. A complete brief answers six things; anything left out, Bob fills with a generic default. For an Orchestrate agent the six are:

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

Use a brief to start a project, in Ask mode. A brief that covers the six items gets few questions back; one that covers two or three, like the first prompt of chapter 4, gets the rest back as questions, which is fine when you are still finding out what you want.

Limits: it is only as clear as you are. Anything left out, Bob guesses, without saying so. The closing sentence depends on the mode: in Agent mode it is the only thing that stops Bob from building at once; in Ask mode the mode prevents building and the Discover rules already ask for questions rather than a design, so the closing sentence only says what you want back.

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

The labels are for you, not for Bob. They are a checklist that keeps you from forgetting what done looks like and when to stop; Bob understands the same content as plain sentences. Leave a part out when the project's rules or an approved design already say it: in chapter 4 the whole Build prompt is one line for that reason.

Example, from the Build phase of chapter 5:

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

Use it in Build, for anything that creates or changes something on the instance, whenever the check is specific to the task. Each part closes one way of guessing: Goal limits the work, Context stops invented data, Constraints stop renaming, Deliverable says what to hand back, Verify replaces Bob's idea of done with a check you can repeat, Stop says what to do when unsure.

Limits: it takes longer to write, and you need the names of files, agents and tools to fill it in. It is the wrong type while you are still exploring.

### Type 4: the specification prompt

A specification prompt asks for one file and lists what the file must contain. IBM's Planning Analytics workshop uses it to have Bob write agent definitions:

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

Limits: it produces the file and nothing else; importing and testing are separate prompts. It skips the design conversation, so it is not for new work.

### Type 5: the follow-up

A follow-up is a short correction inside a conversation that is already going: "Use LL-1003 as the example instead", "Shorter, under 100 words", "You changed the agent's name; put it back". Bob's documentation calls this iterating.

Use it to adjust a result you mostly like. It is the fastest type, because the context is already in the conversation.

Limits: it works while the conversation is short. After many follow-ups Bob loses track of earlier constraints; start a new chat with a complete prompt and the current files mentioned. Three follow-ups on the same problem mean the original prompt was missing something: rewrite it instead of sending a fourth.

### Choosing the type

| You want to | Type | Bob mode |
|---|---|---|
| Understand something, or check what Bob understood | Question | Ask |
| Start a project, explore, get a first proposal | Brief, ending with what you want back | Ask, then Plan |
| Revise a design | Structured, or a follow-up if the change is small | Plan |
| Create or change anything on the instance | Structured, or one line when the design and the rules carry the rest | Agent |
| Get one file whose contents you already know | Specification | Plan or Agent |
| Adjust a result you mostly like | Follow-up | The mode you are in |

Whatever the type, a prompt that asks for work must say two things: what done looks like, and when Bob should stop and ask. The brief carries them in its last lines, the structured prompt in Verify and Stop, the specification in "return only the file". Prompts without them are the source of most surprises.

## 3.4 Keeping control during Build

Three checks, all enforced by the rules in the project folder, keep Build under control without approving every step.

- Verify after every change. Bob looks at the instance after each import, because the platform sometimes reports success when it has logged an error.
- Read the reasoning when testing. Tool calls and their real results appear there, and a polite final answer can hide a runtime error.
- Restart the Orchestrate server before giving up. Some failures live in the connection, not in your files; the restart control is in Bob's settings, MCP tab.

The walkthroughs show each check at the moment it matters; chapter 15 collects the cases behind them.

## 3.5 How much to say

The walkthroughs ask less of you as they go. In chapter 4 you write one prompt per phase and read every operation Bob performs. In chapters 5 and 6 the Build prompt covers several artifacts and you check the result. From chapter 9 on, you describe the business need once, approve one design, and read the report.

Bob writes the YAML and the Python; you do not need to learn them. What you need to learn is when to be precise and when to delegate, and the way to learn it is to start precise and loosen as you see what Bob gets right on its own. Chapter 4 is slow on purpose.

## 3.6 Prompts, weak and better

One weak prompt and one better prompt for the same situation, one per type.

| Situation | Weak | Better | Why |
|---|---|---|---|
| Starting a project (brief) | "Build me a customer service agent for Lumen Logistics that can track orders, answer policy questions and give shipping quotes." typed in Agent mode | The six-item brief: three example user sentences, the data files and the existing tool named with @, the ten-tool limit, and "tell me what you understood, what you need to know, and what exists on the instance", in Ask mode | The weak prompt lets Bob guess the data, invent tools and import before you have seen a name |
| Adding one tool (structured) | "Add the order status tool to the agent." | The six-part prompt shown in 3.3 | The weak prompt names no file, no agent and no proof of success; Bob may create the tool from scratch, rename it, or declare victory when the import returns |
| Investigating a failure (question) | "The agent does not work, fix it." | "Chat with lab_order_agent asking 'Where is order LL-1001?' with reasoning included. Show every tool call and result exactly as returned before proposing any change. Do not modify anything yet." | "Fix it" invites Bob to patch the first thing it sees; the evidence is in the reasoning and nowhere else |
| Asking for a single file (specification) | "Write me an agent YAML for order tracking." | The specification prompt shown in 3.3 | Every property is listed and the schema named; the weak prompt yields a plausible file with a made-up name |
| Adjusting a result (follow-up) | "That's not right, try again." | "The table is right but the answer is too long. Keep the table, remove the introduction, and keep the whole answer under 80 words." | "Try again" gives Bob nothing to change, so it changes something at random |

Two patterns run through the better column: point at real files instead of describing them, and say what Bob should hand back and when it should stop. Keep those two and the rest of the wording can be as informal as you like.

Prompts to avoid, in the form IBM's Bob training uses:

| Prompt | Why it fails | What to write instead |
|---|---|---|
| "Build me a customer service agent" | Bob invents the users, the facts, the tools and the names | The six-item brief, in Ask mode |
| "Give it tools, a knowledge base and a few collaborators" | Every component is a place an answer can go wrong; with all of them at once, nothing can be traced | One component per iteration, as the walkthroughs do |
| "It does not work, fix it" | Bob patches the first thing it sees | Ask for the reasoning of the failing test first |
| "Make it production ready" | Everything lands in draft; going live is a decision at the second gate | Build and test in draft; deploy in chapter 11 |
| "Do not delete anything, ask before importing, verify afterwards" | Repeats what the rules already enforce, and teaches that the prompt is the safeguard | Only what is specific to the task; the rules do the rest |

## 3.7 The files behind the prompts

Bob reads a few files from the project folder at the start of every conversation. They are the reason the prompts in this guide stay short. They came with the repository cloned in chapter 2; you do not edit them, and later chapters open them when a walkthrough needs to explain what they do.

| File | What it does |
|---|---|
| `AGENTS.md`, at the top of the folder | Describes the project to Bob: how the folders are organised, the naming rules, how to work with the instance, and which actions require asking you first |
| `.bob/rules-ask`, `.bob/rules-plan`, `.bob/rules-code` | One short file per phase, loaded with the matching mode: what a Discover answer contains, what a design must let you judge, how a build is verified |
| `.bob/mcp.json` | Written by the extension in chapter 2: how Bob starts the Orchestrate server and the documentation server, and which folder it may work in |

One practical rule, from IBM's best practices: one task per conversation. Discover and Design share one conversation, because the design needs your answers; Build starts a new one, with the design file mentioned. Long conversations are where Bob forgets constraints it accepted an hour ago; Bob's documentation calls this context poisoning.

## 3.8 Keeping your work

The files Bob writes into the project folder, the designs and the definitions, are the product of this guide. Keep them in git, so that any chapter can be undone and every version of an agent can be found again. The folder is a clone of the guide's repository, so git is already there; what is missing is a place of your own to push to, because the guide's repository is not writable by readers.

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
