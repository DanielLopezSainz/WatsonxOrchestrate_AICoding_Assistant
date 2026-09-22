# Chapter 3. How to work with Bob

Level: beginner. Time: about 40 minutes of reading; nothing is built. Prerequisites: none, though the examples refer to the project folder from chapter 2.

## What this chapter is about

The subject. How to talk to Bob so that it builds what you meant, and not something else. It is the part that decides whether the rest of the guide is a pleasant experience or a frustrating one. All the walkthroughs from chapter 4 onwards follow the same way of working, so once it is clear here you will not need to think about it again.

What you will be able to do afterwards:

- Split any piece of Orchestrate work into the three phases the guide uses, Discover, Design and Build, and match each one to Bob's Ask, Plan and Agent modes.
- Name the two moments where Bob must stop and wait for you, and what you are approving at each.
- Choose among five kinds of prompt, question, conversational, structured, specification and follow-up, according to what you want back, and write each one.
- Turn a weak prompt into one that says what "done" looks like and when Bob should stop and ask.
- Say what the files Bob reads at the start of every conversation are for, without having opened them.

Skip this chapter if you already work with Bob in its three modes and write prompts that state the deliverable, the verification and the stopping rule. Read section 3.3 anyway, because the structured prompt with its six parts is used verbatim from chapter 4 on, and the walkthroughs do not explain it again.

The way of working described here fits Bob's three modes, Ask, Plan and Agent, exactly, and the rest of the guide relies on that fit. From here on, "the assistant" means Bob: the word is kept because the prompts, the rules and the habits are about working with an assistant, and Bob is the one this guide uses.

## 3.1 The three phases

Building an Orchestrate agent with an assistant goes through three phases, called Discover, Design and Build in this guide. Each phase gives the assistant a bit more freedom than the previous one, and in Bob each phase is simply one of the modes you choose from the dropdown at the bottom of the chat window.

In the Discover phase (Ask mode in Bob) the assistant is only allowed to read. It can read your project files, it can look at what already exists on your Orchestrate instance (the agents, the tools, the connections, and so on) and it can search the Orchestrate documentation. It cannot write files and it cannot run commands. The expected result of this phase is that the assistant tells you, in its own words, what it has understood of your request, which questions it needs answered, and what already exists on your instance. Read the restatement carefully. If the assistant has misunderstood something, this is the cheapest moment to correct it; later it becomes expensive.

In the Design phase (Plan mode in Bob) the assistant can also write files, but still no commands and still nothing that creates artifacts on the instance. The expected result is a design document written into the project: which agents there will be, which tools each one gets, which external systems need a connection and of which kind, which documents will become a knowledge base, which workflows if any, and in which order all of it must be built. This document is what you approve before anything gets created. Section 3.2 comes back to this approval.

In the Build phase (Agent mode in Bob) the assistant has all its capabilities. It writes the YAML and Python files, it imports them into your Orchestrate instance in the right order, it chats with the resulting agent to test it, it reads the reasoning of the agent to see what really happened, it fixes what failed and it repeats until the tests pass. At the end of this phase the artifacts are in the draft environment of your instance, together with a short report of what was built.

The same thing as a table, for reference:

| Phase | Bob mode | The assistant can | You get at the end |
|---|---|---|---|
| Discover | Ask | Read files, look at what exists on the instance, search the documentation | A restatement of your request, the open questions, an inventory of what exists |
| Design | Plan | The above, plus write files | A design document in the project, waiting for your approval |
| Build | Agent | Everything | The artifacts imported in draft, a test transcript, a short report |

Why three phases and not one? Because an assistant in Agent mode that receives a vague request starts creating things immediately. Creating things on the instance is fast and costs nothing, so within a few seconds it will have imported an agent, discovered that a tool was missing, created the tool, imported the agent again, and so on. You end up with a collection of half-thought artifacts on your instance, with names you did not choose, and you have to review what was built instead of reviewing a design. This happened more than once while preparing this guide. Ask mode forces the assistant to think before it can act, and Plan mode forces it to write its plan down where you can read it. Only after that does it get the keys.

Note: you change the mode with one click on the dropdown, with the shortcut `⌘ .` on a Mac (`Ctrl .` on Windows and Linux), or by typing `/ask`, `/plan` or `/agent` in the chat. Bob often suggests a mode change itself when it notices the request needs one, and you can accept the suggestion.

## 3.2 The two approval points

There are only two moments where the assistant has to stop and wait for you. This guide calls them gates.

The first gate is between Design and Build. What you approve here is a list, nothing more: which agents exist and what each one is for, which tools each agent has, which external systems need a connection, which documents become knowledge, and the order in which it will all be built. A practical test: if you cannot explain that design to a colleague by reading the list, send it back to the assistant with your questions. When it is right, the approval is one line, and in chapter 4 that line is the whole Build prompt, so that switching to Agent mode and approving are the same step. A design that you understand is the difference between a walkthrough that takes one hour and one that takes the whole afternoon.

The second gate is at the end of Build, before anything goes live. Everything the assistant creates lands in the draft environment of your instance. Nothing reaches your end users until an agent is deployed, and deploying is done with a command of the ADK, not through the assistant's normal operations on the instance (chapter 1 explains why, and chapter 11 shows the command). Before that command the assistant has to switch the ADK to the right tenant. Be careful here: that switch changes the active environment for every assistant on your machine at the same time, Bob included, which is one more reason to make it an explicit decision and not something the assistant does on its own.

IMPORTANT: the rules in the project folder, the instructions file described in chapter 2, tell the assistant to never deploy, never switch the environment, never set a credential and never remove anything without asking you first. If you see it doing one of those things without a question, the rules are not being read, and you should go through the checklist at the end of chapter 2 again.

Apart from these two gates, let the assistant work. If you interrupt it in the middle of the Build phase to approve every single file, you lose the benefit of Agent mode. Control during Build does not come from approving each step; it comes from the verification habits described in section 3.4.

## 3.3 The types of prompts

A prompt is simply what you type in the chat to the assistant. There is no single correct way to write one, but there are a few clearly different types, each good for something and bad for something else, and knowing which type fits which situation is what you will use most from this chapter. This section lists the five types used in this guide, explains what each one is for, gives its advantages and its limits, and shows an example. Section 3.6 then puts weak and better prompts side by side.

Before the types, the four rules that Bob's documentation gives for any prompt, because they apply to all five: be specific and clear, since vague prompts produce vague output; give an example of the output you want when the format matters; reference files with `@` mentions instead of pasting their content; and start in Plan mode for anything new, so that a plan exists before code does.

### Type 1: the question

A question is a prompt that asks the assistant to find something out and tell you, without changing anything. "Which agents exist on my instance?", "What does the description of lab_order_agent say?", "Why did the last test answer that the order was unknown?" are questions.

What it is good for: understanding your project or your instance, understanding why something happened, and checking the assistant's own understanding before you give it work. Questions belong in Ask mode, where the assistant cannot act, which makes them completely safe.

Limits: nothing gets built. And the answer is only as good as what the assistant read; if you want it to look at a particular file or a particular test, mention it, otherwise it answers from memory.

Example:

```
Chat with lab_order_agent asking "Where is order LL-1001?" with reasoning included.
Show me every tool call and every tool result from the reasoning, exactly as
returned. If a result contains an error, quote it and tell me what you think
caused it. Do not change anything.
```

### Type 2: the conversational prompt

A conversational prompt describes what you want in your own words, as you would to a colleague, and ends with one sentence that asks the assistant to propose before it acts. This is the type IBM's own accelerator for Bob uses to start a project, and its example looks like this:

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

IBM's own Bob training states the rule behind this type in one line: a good prompt is a use case brief, not a question. Its brief answers six things, who, what, how it is consumed, which data, which products, and what is out of scope, and anything left out is filled with a generic default. For an Orchestrate agent the six become:

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which of them exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

A conversational prompt that covers the six needs few follow-up questions. One that covers two or three, like the first prompt of chapter 4, gets the rest back as questions, which is fine when you are still finding out what you want and slow when you already know.

What it is good for: starting a project, exploring, and any moment when you do not yet know exactly what you want. The assistant's questions help you find out. It needs no format to learn, and the example user sentences you include tell the assistant more than any title would.

Limits: it is only as clear as you are. Anything you leave out, the assistant will guess, and it will not tell you it guessed. The last sentence depends on the mode. In Agent mode it is the only thing that stops the assistant from building straight away, so it must be there. In Ask mode the mode itself prevents building, and the Discover rules in the project folder already tell the assistant to answer with a restatement and questions rather than a design, so the closing sentence only needs to say what you want back. Use it in Discover and for the first version of a design, and add facts to it as you learn them.

### Type 3: the structured prompt

A structured prompt has parts, each answering one question the assistant would otherwise have to guess. The labels are for you, not for Bob: they are a checklist that keeps you from forgetting what done looks like and when to stop, and Bob understands the same content written as ordinary sentences. This guide uses six parts:

```
Goal:        what should exist when this is done, in one sentence
Context:     the files, folders and data to use, by name, with @ mentions
Constraints: names to keep, the model to use, what not to touch, limits from the design
Deliverable: exactly what you want back (a file, an import, a chat transcript, a report)
Verify:      how the assistant proves that it worked, in a way you can check yourself
Stop:        when it should ask you instead of guessing
```

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

What it is good for: the Build phase, and any task where the assistant creates or changes something on your instance. This is the type to use when mistakes cost time. Why it works better there than a conversational prompt: each of the six parts closes one door to guessing. Goal stops the assistant from doing more than asked; Context stops it from inventing data; Constraints stop it from renaming or "improving" things; Deliverable tells it what to hand back; Verify replaces its own idea of "done" (usually "the command did not fail") with a check you can repeat; Stop tells it what to do when it is unsure, which is the moment most surprises come from. The result is a prompt that two different people, or two different assistants, would execute the same way.

Limits: it takes longer to write, it can feel bureaucratic for a small task, and you need to know the names of things (files, agents, tools) to fill it in. It is the wrong type when you are still exploring.

The two parts people leave out most often are Verify and Stop, and they are the two that matter most when the check and the stopping condition are specific to the task. A structured prompt without them is a conversational prompt with headings. There is one legitimate reason to leave a part out: its content would only repeat what the project's rules or an approved design already say. A part is there to carry what is specific to the task; repeating the rules in every prompt is noise, and in chapter 4 the whole Build prompt is one line for exactly that reason.

### Type 4: the specification prompt

A specification prompt asks for one file and lists what the file must contain. IBM's Planning Analytics workshop uses this type to have Bob write agent definitions:

```
Generate a ready-to-import agent YAML with these properties:
- name: lab_order_agent
- description: answers questions about the shipping status of customer orders
- llm: groq/openai/gpt-oss-120b
- style: react_core
- no tools or collaborators yet, they are added in the next step
Follow the spec_version v1, kind native schema. Return only the YAML.
```

What it is good for: small, well-understood artifacts that you want quickly and predictably. Every property is listed, the schema is named, and "return only the YAML" avoids a page of explanation you did not ask for. It is a structured prompt reduced to what one file needs.

Limits: it only works when you already know the fields of the file. It produces the file and nothing else; importing it and testing it is a separate prompt. Used on its own, it skips the design conversation, so keep it for artifacts whose design is already approved.

### Type 5: the follow-up

A follow-up is a short correction inside a conversation that is already going: "Use LL-1003 as the example instead", "Shorter, under 100 words", "You changed the agent's name; put it back", "Show me the reasoning for that last test". Bob's documentation calls this iterating.

What it is good for: adjusting a result you mostly like. It is the fastest type by far, because all the context is already in the conversation.

Limits: it only works while the conversation is short and focused. After many follow-ups the assistant starts to lose track of earlier constraints; the remedy is to start a new chat with a fresh, complete prompt and the current files mentioned. A useful rule: three follow-ups on the same problem means the original prompt was missing something, so rewrite the prompt instead of sending a fourth.

### Choosing the type

| You want to | Type | Bob mode |
|---|---|---|
| Understand something, or check what the assistant understood | Question | Ask |
| Start a project, explore, get a first proposal | Conversational, ending with what you want back: questions in Ask mode, a proposal to approve in Plan mode | Ask, then Plan |
| Revise a design | Structured, or a follow-up if the change is small | Plan |
| Create or change anything on the instance | Structured, with Verify and Stop filled in | Agent |
| Get one file whose contents you already know | Specification | Plan or Agent |
| Adjust a result you mostly like | Follow-up | Whatever mode you are in |

Whatever type you use, two things must always be present in a prompt that asks for work: what "done" looks like, and when the assistant should stop and ask. The conversational prompt carries them in its last sentence; the structured prompt has a line for each; the specification prompt has "return only the file". A prompt without them is the source of most of the surprises people report with coding assistants.

## 3.4 Keeping control during the Build phase

Three habits, all enforced by the rules installed in chapter 2, keep the Build phase under control without you approving every step. The first is to verify after every change: the assistant looks at the instance after each import, because the platform sometimes reports success when it has actually logged an error, and the only way to know is to look. The second is to read the reasoning of the agent when testing it, because that is where tool calls and their real results appear, and a polite final answer can hide a runtime error. The third is to restart the Orchestrate server from Bob's MCP tab before giving up on an operation, because some failures live in that connection rather than in your files. The walkthroughs show each of these habits at the moment it matters, and chapter 15 collects the cases behind them.

## 3.5 How much you need to say

The walkthroughs ask less of you as they go. In chapter 4 you write one prompt per phase and read every operation the assistant performs. In chapters 5 and 6 the Build prompt covers several artifacts and you only check the result. From chapter 9 on you describe the business need once, approve one design, and read the report.

The assistant writes the YAML and the Python; you do not need to learn that. What you need to learn is when to be precise and when to delegate, and the only way to learn it is to start precise and loosen as you see what the assistant gets right on its own. So chapter 4 is slow on purpose. By chapter 9 the same assistant will need one paragraph from you.

## 3.6 Prompts, weak and better

Writing good prompts is the most important thing to learn in this guide, so this section gives one weak prompt and one better prompt for the same situation, five times, with a line on why the better one works. Each pair uses one of the types from section 3.3. The walkthroughs contain the real answers the assistant gave.

Starting a project (conversational). Weak, typed in Agent mode:

```
Build me a customer service agent for Lumen Logistics that can track orders,
answer policy questions and give shipping quotes.
```

Better, in Ask mode:

```
I would like to build a customer service front door for Lumen Logistics with
watsonx Orchestrate. Users will ask things like "where is order LL-1003",
"what is the hotel limit in Paris" and "how much to ship 3 kg to Germany".
The orders are in @lab/data/orders.json, the policies are the two documents
in @lab/knowledge/docs, and there is already a carrier quote tool in
@lab/tools/lab_get_carrier_quote.py that needs the connection lab_carrier_api.
No agent should have more than ten tools and collaborators combined, and
please reuse what already exists on the instance.

Tell me what you understood, what you would need to know, and what already
exists on the instance.
```

Why it is better: the weak prompt lets the assistant guess the data, invent tools and start importing before you have seen a name. The better one gives three example user sentences, points at the real files, states the one hard limit, and ends by saying what it wants back. The Ask mode it is typed in keeps the assistant from building, and the Discover rules keep the answer to understanding and questions.

Adding one tool (structured). Weak:

```
Add the order status tool to the agent.
```

Better:

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

Why it is better: the weak prompt does not say which file, which agent, or what proves success, so the assistant may create the tool from scratch, rename it, or declare victory when the import returns. The better one names both files, fixes the name, says what to hand back and how it will be checked, and says what to do on error.

Investigating a failure (question). Weak:

```
The agent does not work, fix it.
```

Better:

```
Chat with lab_order_agent asking "Where is order LL-1001?" with reasoning
included. Show me every tool call and every tool result from the reasoning,
exactly as returned, before proposing any change. If a result contains an
error or a traceback, quote it and tell me what you think caused it.
Do not modify anything yet.
```

Why it is better: "fix it" invites the assistant to patch the first thing it sees. The better prompt brings the evidence into the open first; most runtime problems (a tool that imported but cannot run, a parameter the agent invented, a tool that was never called) are visible in the reasoning and nowhere else.

Asking for a single file (specification). Weak:

```
Write me an agent YAML for order tracking.
```

Better:

```
Generate a ready-to-import agent YAML with these properties:
- name: lab_order_agent
- description: answers questions about the shipping status of customer orders
- llm: groq/openai/gpt-oss-120b
- style: react_core
- no tools or collaborators yet, they are added in the next step
Follow the spec_version v1, kind native schema. Return only the YAML.
```

Why it is better: every property the file needs is listed and the schema is named, so the file is predictable. The weak prompt produces a plausible file with a made-up name and whatever fields the assistant remembers.

Adjusting a result (follow-up). Weak:

```
That's not right, try again.
```

Better:

```
The table is right but the answer is too long. Keep the table, remove the
introduction, and keep the whole answer under 80 words.
```

Why it is better: "try again" gives the assistant nothing to change, so it changes something at random. The better one says what to keep, what to remove, and the limit to respect.

Two patterns run through all five pairs. The better prompt always points at real files instead of describing them, and it always says what the assistant should hand back and when it should stop. Keep those two things and the rest of the wording can be as informal as you like.

The same lessons as a table of prompts to avoid, in the style IBM's Bob training uses:

| Prompt | Why it fails | What to write instead |
|---|---|---|
| "Build me a customer service agent" | The assistant invents the users, the facts, the tools and the names | The six-item brief above, in Ask mode |
| "Give it tools, a knowledge base and a few collaborators" | Every component is a place an answer can go wrong; with all of them at once, nothing can be traced | One component per iteration, starting with instructions alone, as the walkthroughs do |
| "It does not work, fix it" | The assistant patches the first thing it sees | Ask for the reasoning of the failing test first, then decide |
| "Make it production ready" | Everything lands in draft; going live is a decision at the second gate, not a prompt | Build and test in draft; deploy in chapter 11 |
| "Do not delete anything, ask before importing, verify afterwards" | Repeats what the rules already enforce, and teaches the reader that the prompt is the safeguard | Only what is specific to the task; the rules do the rest |

## 3.7 What runs behind the scenes

Bob reads a small set of files from the project folder automatically, at the start of each conversation, and those files are what allow the prompts in this guide to stay short. You do not need to know their contents now; they came with the repository you cloned in chapter 2, and later chapters open them one at a time when a walkthrough needs to explain something they do. For the moment it is enough to know what kinds of files exist and what each kind is for.

The project instructions. A short text file in the root of the project, `AGENTS.md`, that describes the project to the assistant: how the folders are organised, which naming rules apply, how it must work with your Orchestrate instance, and which actions require asking you first.

The phase rules. Three short files, one for each phase, holding the rules that apply only during Discover, Design or Build. Each one is tied to a mode, so the right rules load themselves when you switch modes.

The connection settings. The file the extension wrote in chapter 2, which tells Bob how to reach your Orchestrate instance and the Orchestrate documentation, and which project folder it is allowed to read and write on your behalf. Chapter 4 is the first time you see it in action.

All of these live under the `.bob` folder of the project, with `AGENTS.md` next to it. The repository also carries the equivalent files for other assistants, mentioned in chapter 2; they play no part in this guide.

One last practical point. Keep one task per chat. When a phase of a walkthrough ends, start a new conversation for the next phase and give it the design document as context. Long conversations are where the assistant starts to forget constraints that it accepted an hour ago. Bob's documentation calls this context poisoning, and the remedy is a fresh chat, with the right file mentioned at the start.

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

