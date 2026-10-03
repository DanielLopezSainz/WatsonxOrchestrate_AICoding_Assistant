# Chapter 4. Your first agent

Level: beginner. Time: about 45 minutes. Prerequisites: chapter 2 completed, chapter 3 read or skipped according to its reading table.

## Overview

Suppose that the street light outside your house has been dark for a week. It is seven in the evening and the city offices are closed. You open the website of the City of Utopia and type: "The street light on my street has been out for a week. Who do I tell?" A few seconds later you have the answer: the Roads and Infrastructure department, the address to write to, and the hours when someone answers the phone.

That answer comes from the agent that you create in this chapter, the first agent of CivicPulse. It knows three city departments, what each one handles, and how to reach them. It also knows what to say when a resident asks about something that it was never told.

You create the agent in three steps, one in each of Bob's modes. Bob asks you what it needs to know, writes a design for your approval, builds the agent, and tests it. Then you make the agent fail: you ask it for a detail that is missing from its facts, read the answer that it invents, and correct it. That correction demonstrates the rule that every later chapter relies on: an agent knows what it was told, and nothing else.

The agent is intentionally simple. It consists of:

- One agent, `civic_info_agent`, defined in one file.
- The default model of the instance.
- About twenty lines of instructions: the facts about three departments, the tone, and what to answer when a question is outside those facts.
- A welcome message and two starter prompts, shown before the resident types.

It has no knowledge base, no tools and no connection to any other system, so every answer can be traced to its instructions. The other components are added from chapter 5 onwards; section 1.2 describes them.

Skip this chapter if you have already created an agent in watsonx Orchestrate with Bob. To continue with chapter 5 without building the agent, send Bob this instruction in Agent mode: `Import walkthroughs/ch04/agents/civic_info_agent.yaml into my instance.`

## 4.1 Before you start

This chapter requires the setup from chapter 2, completed in full:

- The guide's repository cloned and open in Bob (chapter 2, step 1).
- The watsonx Orchestrate ADK extension installed and the workspace initialised in that folder (steps 2 and 3).
- Bob's starting message sent, so that the Orchestrate skills are loaded (step 4).
- An environment active in the Environment Manager, connected to your Developer Edition or your tenant (step 5).
- The approvals set as in step 7: Read and MCP on, Edit and Execute off. With Edit and Execute on, Bob writes files and runs commands without the approval requests that this chapter mentions.

Check that Bob reaches your instance. Start a new conversation in Ask mode and send:

```
Which agents exist on my instance?
```

On a new Developer Edition, Bob lists two agents, DocProcessing and AskOrchestrate. On a new tenant, it lists AskOrchestrate. If the answer mentions a working directory, a forbidden path or an authentication problem, see section 2.8.

If the list already contains `civic_info_agent`, someone has run this chapter on the instance before. Ask Bob to remove it and to list the agents again. Bob asks for your approval before removing it.

## 4.2 Ask mode: understand the request

Mode: Ask, in a new conversation.

This is the first time that you tell Bob about the project, and the purpose of this first prompt is not to get anything built. It is to make sure that Bob has understood what you want, and to let Bob tell you what it still needs to know, before a single file exists. A misunderstanding found now takes one sentence to correct. Found after the build, it means building again.

Ask mode is the right place for this conversation: Bob can read your project and look at your instance, and it cannot change anything.

The prompt describes the agent in plain words: who it is for, the kind of question that it answers, where its knowledge comes from, and what it must not do. It ends by asking Bob for three things in return. It is a structured prompt written as running text (chapter 3, type 3).

```
I would like to build an information agent for the residents of the City of
Utopia with watsonx Orchestrate. It should answer questions like "the street
light on my street has been out for a week, who do I tell?", "how do I apply
for a building permit?" and "when is the waste office open?". It answers from
a fixed set of facts about three city departments: Permits and Planning, Roads
and Infrastructure, and Waste and Recycling. It does not look anything up in
other systems and it does not create requests.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob does not answer immediately. It first looks at your instance, which takes a few seconds, so that its answer is about your instance and not about watsonx Orchestrate in general. The answer usually has three parts:

1. What Bob understood. Read it against what you meant. If it is wrong, correct it now.
2. What already exists on the instance: the agents, tools, knowledge bases and connections, and whether the name of the new agent is free. Bob reads this from the instance.
3. The questions that Bob needs answered before it can write a design, for example the facts for each department, the format of the answers, what to say when a question is outside the facts, and the name of the agent.

Now it is your turn to answer. Bob's questions vary from one run to another, but they come down to the same points: the facts, the tone, the limits of the agent, and its name. The following answer gives Bob all of them at once, so you can use it whatever the wording of Bob's questions. Send it in the same conversation.

```
Use these facts as they are.

Permits and Planning: permits@utopia.example, 555 0110, Monday to Friday 09:00
to 17:00. Building permit applications are submitted online at
https://services.utopia.example/permits.
Roads and Infrastructure: roads@utopia.example, 555 0120. Potholes, street
lights and damaged signs. Urgent hazards on a public road, such as a burst
water main or a fallen tree: 555 0199 at any time.
Waste and Recycling: waste@utopia.example, 555 0130, Monday to Friday 08:00 to
16:00. Bulky item collection is booked online at
https://services.utopia.example/bulky.

Answers: two or three sentences, plain language, always with the contact.
English only.
If a question is outside the three departments, say so and name the department
most likely to help. Never invent an answer.
Name the agent civic_info_agent, with the display name "Utopia city information".
Keep the facts in the agent's instructions. Do not use a knowledge base.
```

Bob confirms the answers and often goes further: it can lay out the complete agent in the chat, with its definition and example answers, and suggest switching to Agent mode to create it at once. Do not switch to Agent mode yet. Nothing has been created so far, and that is the result of this step: you and Bob now agree on what the agent is. The next step writes the design into a file that you approve, in Plan mode, before anything is built.

## 4.3 Plan mode: write the design

Mode: Plan, in the same conversation.

You and Bob agree on what the agent must do. This step turns that agreement into a design: a document that states exactly what will be built, which you can read, question and correct while it is still only a document.

Stay in the same conversation, so that Bob keeps everything that you have told it, and switch to Plan mode. The prompt is one line, an instruction (chapter 3, type 2). Bob already has the facts; the only thing missing is where to write the design.

```
Write the design for this agent into design/civic-info-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. Open the file and read it as the specification of what you are about to receive. The layout is Bob's choice and differs from one run to another, but the file must contain the following:

| Content | What to check |
|---|---|
| The purpose of the agent | It matches your request |
| The agent | Its name, display name, model, and that it has no tools, no knowledge base and no collaborators |
| The facts | The three departments, with the contacts, hours and addresses exactly as you gave them |
| The instructions | The full text that the agent will read: the facts and the rules for answering |
| The test questions | Each with what a correct answer contains |

Two entries in the description of the agent apply to every agent in this guide:

- The model. You did not name one, so the design uses the default model of the instance. The identifier of the default model depends on the instance and its version; on the instance used to prepare this guide, it is `groq/openai/gpt-oss-120b`.
- The description and the instructions. The description says what the agent is for; other agents and the Orchestrate interface read it to decide when to use this agent. The instructions say how the agent behaves; the agent reads them in every conversation.

## 4.4 Approve the design

Mode: Plan, same conversation.

The design is a proposal, and this is the moment to change it. Changing a paragraph in a document takes one prompt. Changing an agent that is already built means building it again. Everything that you want built must be in the design before you approve it.

The design has one gap: it does not say what a resident sees before typing a question. Request it:

```
Add a welcome message and two starter prompts to the design: the street light
question and the building permit question.
```

Bob revises the file, summarises what it changed, and waits again. Do not take the summary on trust: open the design in the File Explorer and read the new lines. The welcome message should name the three departments, so that a resident knows what the agent covers before typing, and the two starter prompts should be the two questions you asked for. This habit, reading what Bob changed rather than what Bob says it changed, costs a few seconds here and saves hours later, when the changes are to agents on an instance rather than to a document.

When the design says what you mean, it is approved. The approval itself is the first line of the next section, so there is nothing more to send here.

Before you leave the design, notice one thing about the facts: two departments have opening hours and Roads and Infrastructure has none. The design does not say what the agent should do about that, and neither did you. Section 4.8 finds out what the agent does with the gap.

## 4.5 Agent mode: build and test

Mode: Agent, in a new conversation.

Everything so far was preparation. In this step, Bob builds the agent.

Start a new conversation with the plus sign at the top of the chat panel, then select Agent in the mode dropdown. Switching to Agent mode in the conversation you have been using would work too, so the new conversation deserves an explanation.

Think of what Bob has in front of it in that conversation: your request, its first proposal, the facts, a complete agent it drafted before you asked for a design, the design, and your revision. Some of that you approved; some of that you did not. If Bob builds in the same conversation, all of it is in view, and Bob may take a detail from its early draft rather than from the design you approved. In a new conversation, Bob has one source of truth: the design file, which the @ mention in the prompt tells it to read. What you approved is exactly what gets built, which is the point of approving it.

For an agent this small, the difference would rarely show. The habit pays off from chapter 9 onwards, where a design covers four agents and the discussion that produced it runs to pages. It is also how Bob's own documentation recommends moving from a plan to its implementation.

The prompt has two sentences. The first is your approval of the design. The second starts the build. Bob takes everything else from the design file, which the @ mention tells it to read. It is an instruction (chapter 3, type 2).

```
The design in @design/civic-info-design.md is approved. Build it.
```

What happens next takes Bob a minute or two, and it is the whole of this guide in miniature: from one approved document, Bob produces a working agent on your instance and proves that it works.

**What Bob did on the run behind this chapter**

1. **Read.** Bob read the design, and then one of the Orchestrate skills loaded in chapter 2, the one that knows how agents are built and tested. Everything that follows comes from the design and from that skill, not from the prompt.
2. **Wrote the agent.** The file `agents/civic_info_agent.yaml` is the design turned into the form that watsonx Orchestrate accepts: the name, the model, the instructions with the facts, and the welcome message and starter prompts in the exact structure the platform requires.
3. **Imported it.** The agent now exists on your instance, in the draft environment, where only you can use it.
4. **Tested it.** Bob sent the questions from the design, the street light, the fallen tree, the building permit, the bulky item, the property tax, and a second question in the same conversation to check that the agent remembers the first. It wrote the answers and its verdicts into a test report. Every test passed.
5. **Reported.** A table of the files it wrote, and a list of ways to try the agent yourself.

## 4.6 Read the definition

The agent has been created in watsonx Orchestrate. What you see in Bob is its definition file, `agents/civic_info_agent.yaml`, which Bob wrote and imported. Before Bob, this file was written by hand, field by field, from the product documentation; now Bob writes it from the design, and you read it. Open it in the File Explorer. The table lists the fields that this guide refers to.

| Field | Purpose |
|---|---|
| Name | The identifier of the agent: lower case, with underscores. Everything else refers to the agent by this name |
| Display name | The name that users see |
| Description | What the agent is for. Other agents and the Orchestrate interface read it |
| Instructions | How the agent behaves, and in this chapter, the facts that it knows |
| Model | The language model that the agent runs on |
| Kind | The type of agent. It is `native` for every agent in this guide |
| Style | The reasoning strategy of the agent. The guide uses the one that Bob selects by default |
| Tools, collaborators, knowledge base | Empty in this chapter. Chapters 5, 6 and 9 fill them |
| Welcome message and starter prompts | What a user sees before typing |

The file can contain other fields. The table lists the ones that this guide refers to.

Read the file against the design. Bob writes the file from the design, and most of the time the two match, but not always. On the run behind this chapter, the design named a display name, Utopia city information, and the file had none, so the agent appeared under its internal name. Section 4.8 corrects this together with the other correction of the chapter.

## 4.7 Meet your agent

Mode: Agent, same conversation.

Open the watsonx Orchestrate panel. In the Explorer section, move the pointer over the Agents row, click the refresh icon that appears on it, and expand Agents. `civic_info_agent` is there, next to the agents that were already on the instance. Ten minutes ago it was a paragraph in a design document.

Now talk to it. Bob tested it with the questions from the design; this time the questions are yours. Ask through Bob, one question per message:

```
Ask civic_info_agent: "My recycling bin was not collected this morning. Who do I contact?"
```

Then try to catch it out. Residents do not write like a design document, and the agent should cope:

- The same question, written badly: "bin not collected today who do i call".
- A question with two departments in it: "I want to build a garden shed and I also need to get rid of the old one. Who do I contact?"
- A question in the middle of the night: "There is water flooding the street from a broken pipe. It is 2 am. What do I do?"
- A question that is none of its business: "What time does the public swimming pool open?"
- A follow-up in the same conversation, after the recycling question: "And what if it happens again next week?"

Read each answer with the facts of 4.2 next to you. For the first four, the right department and its contact should be there, the flooded street should get the urgent line, and the swimming pool should get a polite refusal with a pointer to the department most likely to help. The follow-up shows whether the agent remembers what you were talking about.

Keep a note of any answer that contains something not in the facts. Section 4.8 shows what to do about it.

The agent is in draft: you can use it, and residents cannot. Nothing is deployed in this chapter.

## 4.8 Correct a wrong answer

Mode: Agent, same conversation.

Now ask the agent for something that its facts do not contain:

```
Ask civic_info_agent: "What are the opening hours of Roads and Infrastructure?"
```

The facts give no hours for this department. Inspect the answer. On the run behind this chapter, the agent replied with Monday to Friday 09:00 to 17:00, which are the hours of Permits and Planning. A language model fills a gap with the most plausible content, and the rule "never invent an answer" was written for questions outside the three departments, not for a missing detail inside one of them.

The correction is made in the instructions, by asking Bob:

```
In agents/civic_info_agent.yaml: add the opening hours "Monday to Friday
07:00 to 19:00" to Roads and Infrastructure. Change the rules so that, when a
question asks for a detail that is not in the facts, the agent says that it
does not have that information. Also add the display name from the design,
"Utopia city information". Import the agent again and ask it the same question.
```

Bob edits the file, imports it again, and asks the question. The agent now answers with the hours. Importing a file with the name of an existing agent replaces that agent; no second agent is created.

Ask one more question that the facts do not cover, for example "Who is the head of the Permits department?". The agent should now say that it does not have that information and give the department's contact.

## 4.9 Export the agent

Mode: Agent, same conversation.

The file that Bob wrote contains what you decided. The instance stores more than that. The last step of the chapter asks Bob to bring back the agent as the instance holds it, so that you can compare the two.

```
Export civic_info_agent from the instance to exports/civic_info_agent.yaml,
and tell me which fields the export contains that agents/civic_info_agent.yaml
does not.
```

Bob creates the `exports` folder if it does not exist, and asks for approval to write the file. The exported file is longer than the file that Bob wrote. The instance adds fields with their default values, such as settings for memory and for the display of reasoning. Nothing from the original file is lost.

Keep both files for different purposes:

- `agents/civic_info_agent.yaml` contains what you decided. Ask Bob to edit this file when the agent must change.
- The exported file is the complete definition as the instance holds it. Use it as a record of a finished agent. It is not updated when you import the agent again; repeat the export to record the change.

## 4.10 Check the result

Mode: Agent, same conversation.

The agent has been built, corrected once and exported. Three questions confirm that it is in the state that chapter 5 expects: one that the facts cover, one that the correction from 4.8 fixed, and one that the facts will never cover. Ask them through Bob, as in 4.7, and compare the answers with the table.

| Question | A correct answer contains |
|---|---|
| The street light on my street has been out for a week. Who do I tell? | Roads and Infrastructure, roads@utopia.example or 555 0120, the opening hours added in 4.8 |
| How do I apply for a building permit? | Permits and Planning, the online application address, the contact |
| Who is the head of the Permits department? | A statement that the agent does not have that information, and the contact of Permits and Planning |

If the first answer has no hours, the correction from 4.8 was not imported; ask Bob to import the file again. If the third answer contains a name, the last rule of the instructions is missing; ask Bob to show the instructions and to restore the rule.

## 4.11 Summary

A resident of Utopia can now ask who to tell about a dark street light and get the right department, with its contact and its hours, from an agent that did not exist an hour ago. You wrote three prompts and one correction; Bob wrote everything else. Four things from this chapter apply to every agent that follows:

- An agent project goes through Bob's three modes: Ask mode to understand the request, Plan mode to write the design, Agent mode to build and test.
- You approve the design before Bob builds, and anything that you want built must be in the design.
- An agent is defined by one file. Importing the file creates the agent in draft; importing it again replaces the agent.
- An agent knows what its instructions say and nothing else. A wrong answer is corrected in the instructions.

The agent's knowledge is twenty lines of facts, and a city has more to say than that: regulations, procedures, opening hours for every service. In chapter 5, the agent gets the city's guides and regulations as a knowledge base, and starts answering questions that no instruction could hold.
