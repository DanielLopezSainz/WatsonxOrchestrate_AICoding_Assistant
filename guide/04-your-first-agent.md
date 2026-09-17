# Chapter 4. Your first agent

Level: beginner. Time: about 45 minutes. Prerequisites: every line of the checklist at the end of chapter 2 answered yes, and chapter 3 read.

## What this chapter is about

The agent. An internal helpdesk for Lumen Logistics employees. People ask it who to call for a badge that does not work, how to reset a password, or when HR is open, and it answers with the right team, contact and hours. Small, but real enough that the questions you ask it are questions a colleague would ask.

Its components. Of everything an Orchestrate agent can be made of, this chapter uses the smallest set that still produces a working agent: one agent, one model, and a block of instructions. Every other component is deliberately absent, and each one is introduced by a later chapter, on the same agent or one next to it.

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

What you will be able to do afterwards:

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

- The folder open in Bob is the one you cloned and initialised in chapter 2. The file `AGENTS.md` is visible at the top of Bob's file list, next to the `agents` and `design` folders, and the MCP tab of Bob's settings shows the two Orchestrate servers as connected. If any of that is not so, go through the checklist in section 2.8 before continuing.
- Bob can reach your instance. Start a new chat in Ask mode and ask "Which agents exist on my instance?" On a new Developer Edition Bob lists two stock agents, DocProcessing and AskOrchestrate; on a new tenant it lists one. Bob should not ask for approval to do this, because listing was pre-approved in step 5 of chapter 2; if it does ask, approve it and revisit that step afterwards. Any answer that mentions a working directory, a forbidden path or an authentication problem is one of the failures described in section 2.9. If the list already contains `lumen_helpdesk_agent`, someone has run this chapter on the instance before you. Ask Bob to remove it and list the agents again; Bob asks for your approval first, because removing anything without asking is forbidden by the instructions file, and that approval request is the first sign in this guide that the file is being read.
- You have about an hour of uninterrupted time. The chapter is short, but the reading between steps is where the learning happens.

No starting-state pack is needed for this chapter, because it starts from nothing.

## 4.2 Discover

Switch Bob to Ask mode (the dropdown at the bottom of the chat, or type `/ask`). Start a new chat. Then give it this prompt.

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

Bob starts with a line such as "Let me look at your instance and workspace before asking questions" and pauses for a few seconds. That pause is Bob querying the instance, and it is the reason the answer that follows is about your instance and not about Orchestrate in general. This is what Bob answered on the run behind this chapter, with the prompt above:

> **What I understood.** You want a single internal helpdesk agent for Lumen Logistics employees. Employees ask it free-text questions about three teams, IT, HR, and Facilities, and it answers from a fixed, curated fact base. It does not call any external system, does not open or close tickets, and does not look anything up dynamically. The badge-door example, the password-reset example, and the HR-hours example are all representative of the scope. The agent's job is: receive question, find the right fact, answer in plain English. Nothing else.
>
> **What already exists on your instance**
>
> | Category | What's there | Reusable? |
> |---|---|---|
> | Agents | DocProcessing (document processing demo) and AskOrchestrate (empty assistant) | Neither is reusable; no name clash with lumen_helpdesk_agent |
> | Tools | example_document_processing_flow (flow tool, tied to DocProcessing) | No |
> | Knowledge bases | None | |
> | Toolkits | None | |
> | Connections | Three voice-webhook connections (unconfigured, unrelated) | No |
>
> Your instance is essentially clean for this work. Nothing will be replaced or overwritten.
>
> **Questions I need answered before writing a design**
>
> 1. The facts themselves. Do you already have the contact numbers, email addresses, hours, and procedures for IT, HR, and Facilities written down somewhere? Or do I need to draft placeholder content and you'll fill it in?
> 2. Delivery format. When the agent answers, should it give a short conversational reply, or a more structured response with a team name, contact, and hours laid out clearly?
> 3. Out-of-scope questions. If an employee asks something the fact base doesn't cover, what should the agent say? A polite "I don't have that information" and stop, or redirect to a specific contact?
> 4. Language. English only, or does Lumen Logistics need other languages?
> 5. Agent name. Do you have a preferred name for the agent (the internal system name, e.g. lumen_helpdesk_agent) and a display name employees will see in the chat UI?
> 6. Architecture preference. For a fixed fact base there are two clean options: (a) embed the facts directly in the agent's instructions (simple, no moving parts, works well for a small set), or (b) load them into a knowledge base and let the agent retrieve from it (scales better if facts grow). Do you have a preference, or should I recommend one?
>
> Waiting for your answers before the Design phase.

Your wording will differ; the parts will not, because the Discover rules prescribe them. Take them in order.

- The restatement. Read it against what you meant. The last line, "receive question, find the right fact, answer, nothing else", is Bob's understanding of the scope in nine words, and if it is wrong this is the cheapest moment to say so.
- The inventory. Bob read it from the instance, not from memory, and it answers two questions at once: is there anything to reuse, and does the chosen name clash with something already there. It also lists things Bob did not understand, such as three unconfigured voice connections, rather than leaving them out. The sentence after the table is the conclusion the table exists to support.
- The questions. Six on this run, numbered, all at once. Each one is a gap in the prompt: the prompt said what the agent does and gave three examples, and nothing about who uses it, in which language, in what format it answers, what it says when it does not know, what it is called, or where its facts live. A brief that covers the six items of chapter 3 pre-empts most of these; the short prompt was chosen here so that you would see the questions once. The last question is the first design decision of the guide, and Bob gave the two options with their trade-off; the answer is (a) here because the facts fit on half a page, and chapter 8 is where (b) becomes the right one.
- The name. Bob proposed `lumen_helpdesk_agent` on its own. It had seen the finished file in the walkthrough folder of the repository, which is the folder doing its job as context. Readers who prefer another name can say so now.
- The closing line. That is the Discover rules speaking, and it is also the check that they loaded: a design at this point, instead of that line, means they did not, and the checklist in section 2.8 is where to look.

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

Switch to Plan mode (`/plan`) in the same chat, so that Bob keeps your answers. One prompt.

Prompt type: structured (chapter 3, type 3), reduced to a single Deliverable line, in Plan mode.

```
Write the design for this agent into design/helpdesk-design.md.
```

One line, because everything else is decided elsewhere. The Design rules in the project folder, one of the files described in section 3.7, tell Bob the seven sections a design document has and their order, that it must show you the file, and that it must wait for your approval before anything is built. The prompt adds the one thing the rules cannot know, the file name, which the Build prompt in 4.5 refers to. Every design document in this guide has the same shape for the same reason. Bob writes the file and shows it to you. This is the first time you see what an agent is made of, so it is worth reading the design slowly. On the run it proposed one agent named `lumen_helpdesk_agent`, with a display name "Lumen Logistics helpdesk", no tools, no collaborators and no knowledge base ("all the facts fit in the instructions"), the three blocks of facts, the behaviour rules from your answer, and a build order of four steps: write the definition file, import it into the instance, test it with three questions, report.

Two things in the design deserve a word of explanation now, because every agent you build from here on has them.

The first is the model. Every agent runs on a language model, and the design names it: `groq/openai/gpt-oss-120b`. That is the model watsonx Orchestrate uses by default, it is available on every instance, and this guide uses it everywhere. You do not need to choose one; you need to know that the line exists, because an agent definition without it is incomplete.

The second is the difference between the description and the instructions. The description is what other agents and the Orchestrate interface read to decide when this agent is the right one to ask; it says what the agent is for and what it is not for. The instructions are what the agent itself reads on every conversation; they say how to behave and, in this chapter, contain the facts. The two are written for different readers, and later chapters will show that a good description matters as much as good instructions.

## 4.4 The first gate

Read the design as if a colleague had written it. Can you say, from the file alone, what the agent will and will not answer? If yes, approve it with one line ("Approved, go ahead"). If something is missing, say so now; the assistant will revise the file and wait again.

A small exercise, if you want one: the design says what happens for questions outside the three teams. Ask yourself whether it also says what happens for a question about one of the three teams that the facts do not cover, for example the name of the HR manager. On the run behind this chapter, it did not, and section 4.8 shows the consequence.

## 4.5 Build

Switch to Agent mode (`/agent`).

Prompt type: structured (chapter 3, type 3), in Agent mode, with three of its six parts. This is the prompt for anything that creates or changes something on the instance.

```
Goal: the agent described in design/helpdesk-design.md exists on my instance
  in draft and passes the tests listed in the design.
Context: @design/helpdesk-design.md
Constraints: add two starter prompts, the badge question and the password
  question, and a short welcome message. Keep everything else as designed.
```

Three parts are missing on purpose, and the reason matters for every Build prompt you will write. Deliverable, Verify and Stop carry what is specific to a task. Here the design already lists the tests and what a correct answer contains, so a Verify line would repeat it; and the Build rules in the project folder already say to write the file before importing, to check the instance after every import, to stop and report when something is not there, and to end with a report, so Deliverable and Stop would repeat them. What remains is what neither the rules nor the design know: the two starter prompts and the welcome message, which the design did not mention. Chapter 5 shows a Build prompt where all six parts are needed, because the checks there are specific to a tool's behaviour.

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

Ask the assistant to chat with the agent with two questions of your own. Choose one that the facts cover and one that they do not, and read the answers with the facts next to you.

Then look at the agent outside the chat. Click the watsonx Orchestrate icon in Bob's left bar; the Explorer section of its panel lists what is on your instance, read from the instance itself and not from your files. Refresh it and find `lumen_helpdesk_agent` under Agents, next to the stock agents. An agent that appears there has really been imported, whatever the chat said, and this is the check the rules make the assistant do after every import. On a tenant you can also open the Orchestrate web interface, Manage agents, and find "Lumen Logistics helpdesk" among the draft agents, with the welcome message and the two starter prompts from the definition file. Nothing is deployed in this chapter; the agent exists in draft, visible to you and not to end users.

[Placeholder: one screenshot of the Explorer section with the agent listed, to be decided.]

## 4.8 When an answer is not quite right

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

Before moving on, ask the agent these three questions through the assistant and compare.

| Question | A correct answer contains |
|---|---|
| My badge does not open the warehouse door, who do I call? | Facilities, extension 4300, the 07:00 to 19:00 hours, and extension 4444 for emergencies |
| How do I reset my password? | The self-service link, and IT at extension 4100 as the fallback |
| What is the name of the HR manager? | A statement that it does not have that information, and HR's contact |

If the first answer has no hours, the fix from 4.8 was not imported; ask for the list of agents and check the instructions. If the third answer contains a name, the last rule of the instructions is missing or was weakened; read the file. If an answer mentions a team or a number that is not in the facts, the model is guessing, and the remedy is always the same: make the instruction explicit and import again.

## 4.11 What you learned

The three phases in practice: a conversational prompt in Ask mode that asks for understanding and questions rather than a proposal, a design file in Plan mode, one structured prompt in Agent mode, and two gates in between. An agent definition is a short file with a name, a description for other agents, instructions for itself, a model, and lists of tools, collaborators and knowledge that are empty for now. Everything the assistant creates lands in draft, and importing the same name again is how it is updated. Empty reasoning means no tool was called. And the agent knows exactly what its instructions say, and nothing more, which is why the first fix you made was to the instructions.

Chapter 5 gives this agent something to do beyond reciting facts: tools that look up orders, and with them the first reasoning you will actually have to read.
