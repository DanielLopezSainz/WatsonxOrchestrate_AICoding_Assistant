# Chapter 4. Your first agent

Level: beginner. Time: about 45 minutes. Prerequisites: chapter 2 completed, chapter 3 read or skipped according to its reading table.

## Overview

The first agent of CivicPulse answers one kind of question: which city department handles this, and how do I reach it? A resident writes "there is a pothole on my street", and the agent answers with the department, its contact and its opening hours.

In this chapter, you create that agent with three prompts to Bob, one in each mode. Bob asks you what it needs to know, writes a design for your approval, builds the agent, and tests it. You then find an answer that is wrong, correct the agent, and confirm the correction. At the end, the agent runs in draft on your instance.

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

Send this prompt. It is a structured prompt written as running text (chapter 3, type 3): what the agent is for, example questions, what it must not do, and what you want in the answer.

```
I would like to build an information agent for the residents of the City of
Utopia with watsonx Orchestrate. It should answer questions like "there is a
pothole on my street, who do I contact?", "how do I apply for a building
permit?" and "when is the waste office open?". It answers from a fixed set of
facts about three city departments: Permits and Planning, Roads and
Infrastructure, and Waste and Recycling. It does not look anything up in other
systems and it does not create requests.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob queries the instance, which takes a few seconds, and answers. The answer usually has three parts:

1. What Bob understood. Read it against what you meant. If it is wrong, correct it now.
2. What already exists on the instance: the agents, tools, knowledge bases and connections, and whether the name of the new agent is free. Bob reads this from the instance.
3. The questions that Bob needs answered before it can write a design, for example the facts for each department, the format of the answers, what to say when a question is outside the facts, and the name of the agent.

The questions vary from one run to another. Answer them in the same conversation. The following answer covers what Bob needs, whatever the wording of its questions:

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

Bob confirms the answers and can outline a design in the chat. In Ask mode, Bob cannot write the design file. Writing the design is the next step.

## 4.3 Plan mode: write the design

Mode: Plan, in the same conversation, so that Bob keeps your answers.

Send this instruction (chapter 3, type 2):

```
Write the design for this agent into design/civic-info-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. The layout of the design is Bob's choice and varies. Check that the file contains the following:

| Content | What to check |
|---|---|
| What was asked | It matches your request |
| What exists on the instance | Nothing is reused or replaced |
| The agent | Its name, display name, model, and that it has no tools, no knowledge base and no collaborators |
| The instructions | The full text that the agent will read, with the facts for the three departments |
| The build steps | Write the file, import it, check the instance, test |
| The test questions | Each with what a correct answer contains |

Two entries in the description of the agent apply to every agent in this guide:

- The model. You did not name one, so the design uses the default model of the instance, `groq/openai/gpt-oss-120b`, which is available on every instance. If the design names another model, ask Bob to use the default.
- The description and the instructions. The description says what the agent is for; other agents and the Orchestrate interface read it to decide when to use this agent. The instructions say how the agent behaves; the agent reads them in every conversation.

## 4.4 Approve the design

Mode: Plan, same conversation.

Read the design. Everything that you want built must be in the design before you approve it.

The design has one gap: it does not say what a resident sees before typing a question. Request it:

```
Add a welcome message and two starter prompts to the design: the pothole
question and the building permit question.
```

Bob revises the file and waits again. When the design is complete, continue with 4.5. The approval is given there.

Note one point for section 4.8: the facts give opening hours for two departments and none for Roads and Infrastructure. Section 4.8 tests what the agent answers when a resident asks for them.

## 4.5 Agent mode: build and test

Mode: Agent, in a new conversation. Click the plus sign at the top of the chat panel, then select Agent in the mode dropdown. The build starts in a new conversation so that the planning discussion does not consume the context.

Send this instruction (chapter 3, type 2). It is also the approval of the design.

```
The design in @design/civic-info-design.md is approved. Build it.
```

Bob reads the design and performs the build steps:

1. It writes the definition of the agent to `agents/civic_info_agent.yaml` and asks for approval to write the file.
2. It imports the file into your instance and asks for approval. This is the first operation in the guide that creates something on the instance.
3. It lists the agents on the instance to confirm that `civic_info_agent` exists.
4. It sends the test questions from the design to the agent and reports the answers.

Compare each answer with the facts in 4.2. A correct answer names the right department and gives its contact.

If Bob reports the reasoning of the agent for a test, the reasoning is empty. This is expected. The reasoning lists the tools that an agent called and what they returned. This agent has no tools, so it answers from its instructions and the model alone. From chapter 6 onwards, the reasoning is the first place to look when an answer is wrong.

## 4.6 Read the definition

Open `agents/civic_info_agent.yaml` in the File Explorer. This file defines the agent. Bob wrote it. You read it and, when the agent must change, ask Bob to edit it.

| Field | Purpose |
|---|---|
| Name | The identifier of the agent: lower case, with underscores. Everything else refers to the agent by this name |
| Display name | The name that users see |
| Description | What the agent is for. Other agents and the Orchestrate interface read it |
| Instructions | How the agent behaves, and in this chapter, the facts that it knows |
| Model | The language model that the agent runs on |
| Tools, collaborators, knowledge base | Empty in this chapter. Chapters 5, 6 and 9 fill them |
| Welcome message and starter prompts | What a user sees before typing |

## 4.7 Check the agent on the instance

Open the watsonx Orchestrate panel. In the Explorer section, expand Agents and refresh the list. `civic_info_agent` appears next to the agents that were already there. An agent that appears in this list exists on the instance.

Then test the agent with two questions of your own, one that the facts cover and one that they do not. In the Agent-mode conversation, send for example:

```
Ask civic_info_agent: "My recycling bin was not collected this morning. Who do I contact?"
```

Nothing is deployed in this chapter. The agent is in draft: you can use it, and residents cannot.

## 4.8 Correct a wrong answer

Mode: Agent, same conversation.

Ask the agent for information that the facts do not contain:

```
Ask civic_info_agent: "What are the opening hours of Roads and Infrastructure?"
```

The facts give no opening hours for this department. Read the answer. A language model tends to complete missing information: the agent can answer that the department is reachable at any time, because the urgent line is, or give hours that are not in the facts. The instruction "never invent an answer" was written about questions outside the three departments, and does not clearly cover a missing detail about one of them.

An agent knows what its instructions say and nothing else. When an answer is wrong, the correction is made in the instructions. Send:

```
The facts gave no opening hours for Roads and Infrastructure. Add "Monday to
Friday 07:00 to 19:00" to that department in agents/civic_info_agent.yaml, and
change the last rule so that it also covers details that are not in the facts:
if a question asks for a detail that is not in the facts, the agent says that
it does not have that information. Import the agent again and ask it the same
question.
```

Bob edits the file and imports it again. An import with the name of an existing agent replaces that agent on the instance; no second agent is created, and no warning is shown. The agent now answers with the hours.

Ask one more question that the facts do not cover, for example "Who is the head of the Permits department?". The agent says that it does not have that information and gives the department's contact.

Every correction in this guide follows the same steps: read the answer, find what is missing in the instructions, ask Bob to change the file, import again, and ask again.

## 4.9 Export the agent

Mode: Agent, same conversation.

Send this instruction:

```
Export civic_info_agent from the instance to exports/civic_info_agent.yaml,
and tell me which fields the export contains that agents/civic_info_agent.yaml
does not.
```

The exported file is longer than the file that Bob wrote. The instance adds fields with their default values, such as settings for memory and for the display of reasoning. Nothing from the original file is lost.

Keep both files for different purposes:

- `agents/civic_info_agent.yaml` contains what you decided. Ask Bob to edit this file when the agent must change.
- The exported file is the complete definition as the instance holds it. Use it as a record of a finished agent.

## 4.10 Check the result

Ask the agent these three questions through Bob, and compare the answers.

| Question | A correct answer contains |
|---|---|
| There is a pothole on my street. Who do I contact? | Roads and Infrastructure, roads@utopia.example or 555 0120, the opening hours added in 4.8 |
| How do I apply for a building permit? | Permits and Planning, the online application address, the contact |
| Who is the head of the Permits department? | A statement that the agent does not have that information, and the contact of Permits and Planning |

If the first answer has no hours, the correction from 4.8 was not imported; ask Bob to import the file again. If the third answer contains a name, the last rule of the instructions is missing; ask Bob to show the instructions and to restore the rule.

## 4.11 Summary

- An agent project goes through Bob's three modes: Ask mode to understand the request, Plan mode to write the design, Agent mode to build and test.
- You approve the design before Bob builds. Anything that you want built must be in the design.
- An agent is defined by one file. Importing the file creates the agent in draft; importing it again replaces the agent.
- An agent without tools has empty reasoning.
- An agent knows what its instructions say and nothing else. A wrong answer is corrected in the instructions.

Chapter 5 gives the agent more information than its instructions can hold: the city's guides and regulations, as a knowledge base.
