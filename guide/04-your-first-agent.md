# Chapter 4. Your first agent

Level: beginner. Time: about 45 minutes. Prerequisites: every line of the checklist at the end of chapter 2 answered yes, and chapter 3 read.

## Overview

This chapter builds one agent with Bob, from a request to a tested agent in draft on your instance, using the three phases of chapter 3 with one prompt each.

The agent is an internal helpdesk for Lumen Logistics employees. People ask it who to call for a badge that does not work, how to reset a password, or when HR is open, and it answers with the right team, contact and hours. Small, but real enough that the questions you ask it are questions a colleague would ask.

Of everything an Orchestrate agent can be made of, this chapter uses the smallest set that still produces a working agent: one agent, one model, and a block of instructions. Every other component is deliberately absent, and each one is introduced by a later chapter, on the same agent or one next to it.

| Component | In this chapter | Introduced in |
|---|---|---|
| Agents | One native agent, `lumen_helpdesk_agent`, defined in one YAML file | |
| Collaborator agents | None. The agent answers every question itself and delegates nothing | Chapter 9 |
| Tools | None. No Python tools, no OpenAPI tools; the agent cannot look anything up or act on anything | Chapter 5 |
| Connections to external systems | None. Nothing leaves the Orchestrate instance | Chapter 6 |
| MCP toolkits | None | Chapter 7 |
| Knowledge base | None. The facts the agent knows are written into its instructions, not indexed from documents | Chapter 8 |
| Flows | None. Every answer is produced by the model reasoning over the instructions | Chapter 10 |
| Model and reasoning style | `groq/openai/gpt-oss-120b`, the instance default, with the `react_core` style | |
| Instructions | About twenty lines: the facts for three teams, the tone, and the rule for questions the facts do not cover | |
| Conversation surface | A welcome message and two starter prompts, shown before the user types | |
| Environment | Draft only. The agent is never deployed in this chapter and no end user sees it | Chapter 11 |

The consequence of that list is what makes the chapter useful: the agent's behaviour is entirely determined by the text of its instructions. When an answer is right, it is because the fact was there; when an answer is wrong, the gap is in that text and nowhere else. Later chapters add components one at a time, and each time the question "where did this answer come from" gets one more possible answer.

After completing this chapter, you can:

- Take a request from a sentence to a tested agent on your instance with Bob, using the three phases of chapter 3 with one prompt each, and recognise the two moments where you approve.
- Read an agent definition file and say what each of its parts is for: name, description, instructions, model, and the lists of tools, collaborators and knowledge that later chapters fill.
- Tell from the reasoning of a test conversation whether the agent called anything or answered from its instructions alone.
- Find a gap in an agent's instructions from a wrong answer, fix the file, and update the agent on the instance by importing it again.
- Export an agent from the instance and know which of the two files, yours or the exported one, to edit and which to keep.

Skip this chapter if you have already built an agent from a definition file through Bob, updated it by re-importing, and read the reasoning of a test chat. Chapter 5 starts from the agent built here, and the finished files are in `walkthroughs/ch04` for anyone who did not build it: copy `agents/lumen_helpdesk_agent.yaml` into your `agents` folder and ask Bob to import it, and you are where this chapter ends.

Everything shown in this chapter, Bob's answers and the agent's answers, was captured from a real run on a Developer Edition, with the folder from chapter 2 open in Bob. Your wording will differ a little; the substance should not.

 Your wording will differ a little; the substance should not.

## 4.1 Before you start

Check these three things. Each one takes a minute, and a missing one will cost you far more later.

- The folder open in Bob is the one you cloned and initialised in chapter 2. The file `AGENTS.md` is visible at the top of Bob's file list, next to the `agents` and `design` folders, and the MCP tab of Bob's settings shows the two Orchestrate servers as connected. If any of that is not so, go through the checklist in section 2.6 before continuing.
- Bob can reach your instance. Start a new chat in Ask mode and ask "Which agents exist on my instance?" On a new Developer Edition Bob lists two stock agents, DocProcessing and AskOrchestrate; on a new tenant it lists one. Bob should not ask for approval to do this, because listing was pre-approved in step 5 of chapter 2; if it does ask, approve it and revisit that step afterwards. Any answer that mentions a working directory, a forbidden path or an authentication problem is one of the failures described in section 2.7. If the list already contains `lumen_helpdesk_agent`, someone has run this chapter on the instance before you. Ask Bob to remove it and list the agents again; Bob asks for your approval first, because removing anything without asking is forbidden by the instructions file, and that approval request is the first sign in this guide that the file is being read.
- You have about an hour of uninterrupted time. The chapter is short, but the reading between steps is where the learning happens.

No starting-state pack is needed for this chapter, because it starts from nothing.

## 4.2 Discover

Mode: Ask, in a new chat. Switch with the dropdown at the bottom of the chat or by typing `/ask`. Then give Bob this prompt.

Prompt type: conversational (chapter 3, type 2), in Ask mode. Your own words, a few example questions, and a closing sentence that says what you want back. Nothing in the prompt needs to stop Bob from building, or from answering with a finished design instead of questions: Ask mode prevents the first, and the Discover rules in the project folder, described in section 3.7, prevent the second. This is the first prompt in the guide where those rules are at work, and Bob's answer shows whether they are being read.

```
I would like to build an internal helpdesk agent for Lumen Logistics employees
with watsonx Orchestrate. It should answer questions like "my badge does not
open the warehouse door, who do I call?", "how do I reset my password?" and
"when is HR open?". It answers from a fixed set of facts about three teams,
IT, HR and Facilities; it does not look anything up in other systems and it
does not create tickets.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob starts with a line such as "Let me look at your instance and workspace before asking questions" and pauses for a few seconds. That pause is Bob querying the instance, and it is the reason the answer that follows is about your instance and not about Orchestrate in general. The answer has four parts, because the Discover rules ask Bob for them; the wording and the layout vary from run to run.

1. What I understood. A restatement of the request in Bob's words, ending on the run with a nine-word version of the scope: "receive question, find the right fact, answer in plain English. Nothing else." Read it against what you meant. If it is wrong, this is the cheapest moment to say so.
2. What already exists on your instance. A table with one row per category, agents, tools, knowledge bases, toolkits, connections, saying what is there and whether it can be reused. On the run it listed the two stock agents, one demo tool, no knowledge bases, no toolkits, three unconfigured voice connections it did not understand but reported anyway, and concluded that nothing would be replaced and that the name `lumen_helpdesk_agent` clashed with nothing. Bob read all of this from the instance, not from memory; the table answers whether there is anything to reuse and whether the chosen name is free.
3. Questions I need answered before writing a design. Six on the run, numbered, all at once: whether the facts exist already or should be drafted as placeholders; whether answers should be short and conversational or laid out as team, contact and hours; what to say when a question is outside the facts; which languages; the agent's name and display name; and whether the facts should live in the instructions or in a knowledge base, with the two options and their trade-off spelled out. Each question is a gap in the prompt: it said what the agent does and gave three examples, and nothing about the users, the language, the format, the unknowns, the name or the source of the facts. A brief that covers the six items of chapter 3 pre-empts most of them; the short prompt was chosen here so that you would see the questions once. The last question is the first design decision of the guide; the answer is "instructions" because the facts fit on half a page, and chapter 8 is where a knowledge base becomes the right choice. Bob also proposed the name on its own, having seen the finished file in the walkthrough folder of the repository.
4. The closing line, "Waiting for your answers before the Design phase." That is the Discover rules speaking, and it is also the check that they loaded: a design at this point, instead of that line, means they did not, and the checklist in section 2.6 is where to look.

Answer the questions in a follow-up, in plain text and in order. Here is the answer given on the run, which is also the data every later chapter reuses:

```
1. The facts are below; use them as they are.
2. Short conversational replies, two or three sentences, always with the contact.
3. If a question is outside the three teams, say you do not have that
   information and point to the team most likely to help. Never invent an answer.
4. English only.
5. Name lumen_helpdesk_agent, display name "Lumen Logistics helpdesk".
6. Facts in the agent's instructions; there are only a handful per team.

IT service desk: it-help@lumen-logistics.example, extension 4100, Monday to
Friday 08:00 to 18:00. Password resets are self-service at
https://it.lumen-logistics.example/reset.
HR: hr@lumen-logistics.example, extension 4200, Monday to Friday 09:00 to 17:00.
Payslips are in the HR portal, not by email.
Facilities: facilities@lumen-logistics.example, extension 4300. Badge and door
access problems go to Facilities. Urgent building problems such as water, power
or alarms go to extension 4444 at any time.
```

Bob confirms the answers in a sentence or two, asks about anything still missing, and tells you to switch to Plan mode for the Design phase. That is the Discover rules again: they stop Bob from designing in this phase even once it has everything it needs, so that the design lands in a file you can approve rather than in a chat message.

Note: keep the facts short and exact. Everything the agent will ever say comes from this text, and later in the chapter you will see what happens when a fact is missing.

## 4.3 Design

Mode: Plan, in the same chat, so that Bob keeps your answers. Switch with `/plan`. Prompt type: structured, reduced to one Deliverable line.

```
Write the design for this agent into design/helpdesk-design.md.
```

One line is enough. The Design rules in the project folder tell Bob what a design has to let you judge, to show you the file, and to wait for your approval. The prompt adds only the file name. You write nothing in any particular format, here or anywhere in this guide; the rules are instructions to Bob, not to you.

What Bob does: says the requirements are settled, asks your approval to write the file, since writing files is not pre-approved in the chapter 2 setup, writes it, and answers with a short summary, ending "Waiting for your approval before the Build phase." Bob may mention using one of its own planning skills on the way.

What Bob's design covered on the run. The headings and the layout are Bob's choice and will differ on yours; the content should not.

| Part of the design | What it holds |
|---|---|
| What was asked | The scope in two sentences |
| What exists on the instance | The inventory from Discover, every item marked unrelated and untouched; no name clash |
| The proposed agent | A table of the agent's fields: name, display name, kind, style, model; tools, knowledge bases, collaborators all none |
| Tools, connections, knowledge bases | None, with the reason: the facts fit in the instructions |
| Behaviour | Tone, length, the rule for unknowns, language, and the full instruction text the agent will read, facts included |
| Build order | Write the file, import, check the agent list, test |
| Tests | Four questions with what each correct answer must contain, the fourth an out-of-scope probe |

Two fields of the proposed agent deserve a word, because every agent from here on has them.

- The `llm` row, `groq/openai/gpt-oss-120b`, is the model the agent runs on. You did not name one and Bob did not ask: the value comes from the instructions file in the project, which lists it as the default model, along with the `react_core` style in the row above it. It is Orchestrate's default, available on every instance, and used throughout this guide. A definition without this line is incomplete.
- Description versus instructions. The description is read by other agents and by the Orchestrate interface to decide when this agent is the right one to ask. The instructions are read by the agent itself on every conversation. Different readers, different texts; the instruction text in the design is the second, and later chapters show why the first matters as much.

The file is in `design/` in your project and, from the run, in the walkthrough folder of the repository.

## 4.4 The first gate

Mode: still Plan, same chat.

Read the design as if a colleague had written it. Can you say, from the file alone, what the agent will and will not answer? Anything you want built has to be in the design before you approve it; the Build prompt is not the place to add things.

The design from 4.3 has one gap of that kind: it says nothing about what an employee sees before typing. Ask for it, in plain words:

```
Add a welcome message and two starter prompts to the design: the badge
question and the password question.
```

Bob revises the file and waits again. That is the first gate at work. When the design says what you mean, go to 4.5; the approval is given there.

A question to keep in mind for later: the design says what happens with questions outside the three teams. Does it say what happens with a question about one of the three teams that the facts do not cover, such as the name of the HR manager? Section 4.8 shows why that matters.

## 4.5 Build

Mode: Agent, in a new conversation. Click the plus sign at the top of the chat to start it, then choose Agent in the dropdown. IBM's workflow starts implementation in a fresh conversation so that the planning discussion does not weigh on it; the @ mention gives Bob the design.

```
The design in @design/helpdesk-design.md is approved. Build it.
```

That is the whole prompt, and it is also the approval from the first gate. Bob reads the design from the mention; it says what to build and how it will be tested. The Build rules say how Bob goes about it: file first, then the import, then a look at the instance, then the tests with their reasoning, then a report. Nothing is left for the prompt to add. Chapter 5 is where a Build prompt needs more, because the checks there depend on how a tool behaves, which no design can know in advance.

Now watch what Bob does, because this is the whole Build phase in miniature. It reads the design. It writes the definition file. It imports the file into your instance; Bob shows this as an approval request, since importing is not among the operations pre-approved in chapter 2, and it is the first time in the guide that something is created on the instance. Approve it. It looks at the instance to confirm the agent is there. Then it runs the tests from the design, asking for the reasoning each time, and reports the answers.

These are the three answers from the run, exactly as the agent gave them:

Badge question:

```
Your badge issue should be handled by Facilities. You can email
**facilities@lumen-logistics.example** or call **extension 4300**. If it's an
urgent building problem (e.g., water, power, alarm), call **extension 4444**
at any time.
```

Password question:

```
You can reset your password yourself at the self-service portal:
[https://it.lumen-logistics.example/reset](https://it.lumen-logistics.example/reset).
If you run into any issues, contact the IT service desk at
**it-help@lumen-logistics.example** or extension **4100** (Monday–Friday, 08:00-18:00).
```

Working-from-home question:

```
I'm sorry, but I don't have that information. Please contact **HR** at
hr@lumen-logistics.example or extension 4200 (Mon-Fri 09:00-17:00) for details
on the work-from-home policy.
```

All three are right. The agent also added bold to the contacts on its own; nobody asked for that, and it is harmless.

One more thing to notice in the assistant's report. Each test conversation was asked for reasoning, and each time the reasoning came back empty. That is not a fault. The reasoning of an agent lists the tools it called and what they returned, and this agent has no tools, so there is nothing to list. From chapter 5 on, the reasoning is where you will look first when an answer is wrong, so it is useful to have seen the empty case now: empty reasoning means the agent answered from its instructions and the model alone.

## 4.6 Reading the definition

Mode: none; this section is reading only.

Open `agents/lumen_helpdesk_agent.yaml`, the file the assistant wrote. It is about fifty lines, and this is the moment to read it once from top to bottom. The version from the run is in the walkthrough files that accompany this guide; the parts that matter are these.

```yaml
spec_version: v1
kind: native
name: lumen_helpdesk_agent
display_name: Lumen Logistics helpdesk
description: >
  Answers Lumen Logistics employees' questions about how to contact the IT
  service desk, HR and Facilities, including opening hours and what each team
  handles. Use it for "who do I call for..." questions. It does not create
  tickets or look up personal data.
llm: groq/openai/gpt-oss-120b
style: react_core
instructions: |
  You are the Lumen Logistics employee helpdesk, operating within watsonx Orchestrate.
  Answer only from the facts below. Keep answers to two or three sentences and always
  include the contact the employee should use.

  IT service desk: it-help@lumen-logistics.example, extension 4100, ...
  HR: hr@lumen-logistics.example, extension 4200, ...
  Facilities: facilities@lumen-logistics.example, extension 4300. ...

  If a question is about anything other than these three teams, say that you do
  not have that information and suggest the team most likely to help. Do not guess.
collaborators: []
tools: []
knowledge_base: []
starter_prompts:
  ...
welcome_content:
  ...
```

Line by line, what each part is for:

- `spec_version` and `kind` say what kind of file this is. They are always `v1` and `native` for the agents in this guide.
- `name` is the identifier: lower case, underscores, no spaces. It is how everything else refers to the agent. `display_name` is what people see.
- `description` is for other agents and for the interface, as explained in 4.3.
- `llm` is the model, and `style` is how the agent reasons; `react_core` is the current recommended style and the only one this guide uses. If you list the agent on the instance you may see it reported as `react_intrinsic`, which is the same style under an older name.
- `instructions` is the agent's operating manual, and in this chapter also its only source of facts.
- `collaborators`, `tools` and `knowledge_base` are empty lists here. Chapter 5 fills `tools`, chapter 8 `knowledge_base` and chapter 9 `collaborators`.
- `starter_prompts` and `welcome_content` are what a user sees in the chat window before typing: a greeting and two clickable example questions.

You will not write this file by hand in this guide; the assistant does it. But you will read files like it often, and you will change lines in them, as the next sections show.

## 4.7 Try it yourself

Mode: Agent, same conversation as the build.

Ask the assistant to chat with the agent with two questions of your own. Choose one that the facts cover and one that they do not, and read the answers with the facts next to you.

Then look at the agent outside the chat. Click the watsonx Orchestrate icon in Bob's left bar; the Explorer section of its panel lists what is on your instance, read from the instance itself and not from your files. Refresh it and find `lumen_helpdesk_agent` under Agents, next to the stock agents. An agent that appears there has really been imported, whatever the chat said, and this is the check the rules make the assistant do after every import. On a tenant you can also open the Orchestrate web interface, Manage agents, and find "Lumen Logistics helpdesk" among the draft agents, with the welcome message and the two starter prompts from the definition file. Nothing is deployed in this chapter; the agent exists in draft, visible to you and not to end users.

[Placeholder: one screenshot of the Explorer section with the agent listed, to be decided.]

## 4.8 When an answer is not quite right

Mode: Agent, same conversation as the build.

On the run behind this chapter, the badge conversation was continued with one more question in the same thread:

```
And what are their opening hours?
```

The agent answered:

```
Facilities does not have listed opening-hour restrictions; you can reach them
anytime by emailing **facilities@lumen-logistics.example** or calling
**extension 4300**. If the problem is urgent (e.g., water, power, alarm), use
**extension 4444**, which is staffed 24/7.
```

Read that against the facts. The facts gave no opening hours for Facilities, and the instruction said "do not guess" about other teams, not about missing details of the three teams. So the agent did what language models do with a gap: it filled it, and "anytime" is not true. This is the most useful thing that happened in the whole run, because it shows the two rules that govern every agent you will build: the agent knows exactly what its instructions say and nothing more, and the rule about what to do with missing information has to be explicit.

The fix is a follow-up.

Prompt type: follow-up (chapter 3, type 5), in the same Agent-mode chat. It says what was wrong, what to change, and how to check it.

```
The agent invented opening hours for Facilities. Add "Monday to Friday 07:00
to 19:00" to the Facilities line in agents/lumen_helpdesk_agent.yaml, and
change the last rule so that it also covers details not in the facts: if a
question asks for a detail that is not in the facts above, say you do not
have that information. Import the agent again and ask the badge question
followed by "And what are their opening hours?" in the same conversation.
```

Two things happen that are worth understanding. First, the assistant edits the file and imports it again with the same name, and the import replaces the draft on the instance in place: there is still one `lumen_helpdesk_agent`, not two, which you can confirm by asking for the list of agents. Importing the same name again is how you update an agent, and there is no warning when it happens, which is why the rules from chapter 2 make the assistant say so before doing it in the later chapters. Second, the answers change:

```
Your badge issue should be routed to Facilities. You can email
**facilities@lumen-logistics.example** or call extension **4300**
(Monday-Friday 07:00-19:00). If it's an urgent building problem (e.g., water,
power, alarm), use extension **4444** at any time.
```

And to a question that the facts still do not cover, "What is the name of the HR manager?":

```
I'm sorry, I don't have that information. You may want to contact HR at
**hr@lumen-logistics.example** or call extension **4200** (Monday-Friday,
09:00-17:00).
```

That loop, read the answer, find the gap in the instructions, change the file, import again, ask again, is the Build phase for every agent in this guide. The only thing that changes in later chapters is where the gap turns out to be.

## 4.9 Round trip

Mode: Agent, same conversation as the build.

One last prompt for this chapter, to learn something about the files you will be keeping.

Prompt type: question (chapter 3, type 1) with a file as deliverable, in Agent mode because a file gets written. Nothing on the instance changes.

```
Export lumen_helpdesk_agent from the instance as a definition file to
agents/lumen_helpdesk_agent.exported.yaml, and tell me which fields the
export contains that my original file does not.
```

The exported file is about twice as long as the one the assistant wrote. On the run it added thirteen fields, all with their default values: things like `memory_enabled: false`, `hide_reasoning: false`, empty lists for `guidelines`, `toolkits` and `skills`, and a long `chat_with_docs` block that is switched off. It also moved `spec_version` to the last line and wrote `style: react_core` back exactly as it was. Nothing from the original was lost.

Two practical conclusions. The exported file is the complete truth about the agent as the instance holds it, so it is the one to keep in version control once an agent is finished. And the short file the assistant wrote is the one to edit, because it contains only what you decided; the defaults will be added again on import.

## 4.10 Checkpoint

Mode: Agent, same conversation as the build.

Before moving on, ask the agent these three questions through the assistant and compare.

| Question | A correct answer contains |
|---|---|
| My badge does not open the warehouse door, who do I call? | Facilities, extension 4300, the 07:00 to 19:00 hours, and extension 4444 for emergencies |
| How do I reset my password? | The self-service link, and IT at extension 4100 as the fallback |
| What is the name of the HR manager? | A statement that it does not have that information, and HR's contact |

If the first answer has no hours, the fix from 4.8 was not imported; ask for the list of agents and check the instructions. If the third answer contains a name, the last rule of the instructions is missing or was weakened; read the file. If an answer mentions a team or a number that is not in the facts, the model is guessing, and the remedy is always the same: make the instruction explicit and import again.

## 4.11 What you learned

The three phases in practice: a conversational prompt in Ask mode that asks for understanding and questions rather than a proposal, a design file in Plan mode, one line in Agent mode that approves the design and starts the build, and two gates in between. An agent definition is a short file with a name, a description for other agents, instructions for itself, a model, and lists of tools, collaborators and knowledge that are empty for now. Everything the assistant creates lands in draft, and importing the same name again is how it is updated. Empty reasoning means no tool was called. And the agent knows exactly what its instructions say, and nothing more, which is why the first fix you made was to the instructions.

Chapter 5 gives this agent something to do beyond reciting facts: tools that look up orders, and with them the first reasoning you will actually have to read.
