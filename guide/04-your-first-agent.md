# Chapter 4. Your first Orchestrate Agent

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 2 completed, chapter 3 read or skipped according to its reading table.

## Overview

Suppose that the street light outside your house has been dark for a week. It is seven in the evening and the city offices are closed. You open the website of the City of Utopia and type: "The street light on my street has been out for a week. Who do I tell?" A few seconds later you have the answer: the Roads and Infrastructure department, the address to write to, and the hours when someone answers the phone.

That answer comes from the Agent that you create in this chapter, the first Agent of CivicPulse. It knows three city departments, what each one handles and how to reach them, and it knows what to say when a resident asks about something that it was never told.

You create the Agent in three steps, one in each of Bob's modes. Bob asks you what it needs to know, writes a design for your approval, builds the Agent, and tests it. Then you look for a gap in its facts: you ask it for a detail that the facts do not contain, read what it answers, and add the detail.

The Agent is intentionally simple. It consists of:

- One Orchestrate Agent, `civic_info_agent`, defined in one file.
- The default model of the instance.
- About twenty lines of instructions: the facts about three departments, the tone, and what to answer when a question is outside those facts.
- A welcome message and two starter prompts, shown before the resident types.

It has no Orchestrate Knowledge Base, no Orchestrate Tools and no Orchestrate Connection to any other system, so its instructions are the only source it has. The other components are added from chapter 5 onwards; section 1.2 describes them.

Skip this chapter if you have already created an Agent in watsonx Orchestrate with Bob. To continue with chapter 5 without building the Agent, send Bob this instruction in Agent mode: `Import walkthroughs/ch04/agents/civic_info_agent.yaml into my instance.`

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

On a new Developer Edition, Bob lists two Agents, DocProcessing and AskOrchestrate. On a new tenant, it lists AskOrchestrate. If the answer mentions a working directory, a forbidden path or an authentication problem, see section 2.8.

If the list already contains `civic_info_agent`, someone has run this chapter on the instance before. Ask Bob to remove it and to list the Agents again. Bob asks for your approval before removing it.

## 4.2 Ask mode: understand the request

Mode: Ask, in a new conversation.

This prompt tells Bob about the project for the first time. Its purpose is to confirm that Bob has understood what you want and to let Bob say what it still needs to know before a single file exists. It is much easier to correct a misunderstanding now than after the Agent is built.

Use Ask mode for this conversation: Bob can read your project and your instance, and cannot change anything.

The prompt is a structured prompt written as running text (chapter 3, type 3). It describes the Agent in plain words: who it is for, the kind of question that it answers, where its knowledge comes from, and what it must not do. It ends by asking Bob for three things in return.

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

Bob first looks at your instance, which takes a few seconds, so that its answer describes what is there. The answer usually has three parts:

1. What Bob understood. Read it against what you meant. If it is wrong, correct it now.
2. What already exists on the instance: the Agents, Tools, Knowledge Bases and Connections, and whether the name of the new Agent is free. Bob reads this from the instance.
3. The questions that Bob needs answered before it can write a design, for example the facts for each department, the format of the answers, what to say when a question is outside the facts, and the name of the Agent.

Bob's questions vary from one run to another, but they come down to the same points: the facts, the tone, the limits of the Agent, and its name. The following answer gives Bob all of them at once, so you can use it whatever the wording of Bob's questions. Send it in the same conversation.

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

Bob confirms the answers and may propose to switch to Agent mode and create the Agent at once. Do not switch yet; nothing has been created. The next step, in Plan mode, writes the design into a file that you approve.

## 4.3 Plan mode: write the design

Mode: Plan, in the same conversation.

In Plan mode, Bob writes a design document that defines the Agent.

Stay in the same conversation, so that Bob keeps everything that you have told it, and switch to Plan mode. The prompt is one line, an instruction (chapter 3, type 2).

```
Write the design for this agent into design/civic-info-design.md.
```

Bob writes the file after you approve the request, and shows a summary. Open the file and read it as the specification of what you are about to receive. The layout is Bob's choice and differs from one run to another, but the file must contain the following:

| Content | What to check |
|---|---|
| The purpose of the Agent | It matches your request |
| The Agent | Its name, display name, model, and that it has no Tools, no Knowledge Base and no collaborators |
| The facts | The three departments, with the contacts, hours and addresses exactly as you gave them |
| The instructions | The full text that the Agent will read: the facts and the rules for answering |
| The test questions | Each with what a correct answer contains |

Two entries in the description of the Agent apply to every Agent in this guide:

- The model. You did not name one, so the design uses the default model of the instance. The identifier of the default model depends on the instance and its version; on the instance used to prepare this guide, it is `groq/openai/gpt-oss-120b`.
- The description and the instructions. The description says what the Agent is for, and other Agents and the Orchestrate interface read it to decide when to use this Agent. The instructions are different: they say how the Agent behaves, and the Agent itself reads them in every conversation.

## 4.4 Approve the design

Mode: Plan, same conversation.

The design is a proposal, and this is the time to change it. Changing the design takes one prompt; changing the Agent after the build means importing and testing it again. Everything that you want built must be in the design before you approve it.

In the run, the design said nothing about what a resident sees before typing a question. Check yours, and if it is missing, request it:

```
Add a welcome message and two starter prompts to the design: the street light
question and the building permit question.
```

Bob revises the file and waits again, with a summary of what it changed. Do not take the summary on trust: open the design in the File Explorer and read the new lines. The welcome message should name the three departments, so that a resident knows what the Agent covers before typing, and the two starter prompts should be the two questions you asked for.

When the design says what you mean, it is approved. There is nothing to send: the approval is the first line of the prompt in 4.6.

The facts give opening hours for two departments and none for Roads and Infrastructure. The design does not say what the Agent should do about that. Section 4.9 shows what the Agent does with the gap.

## 4.5 The Draft and Live environments

An instance has two environments. Draft is the builders' environment: an Agent in Draft can be changed as often as you like, tested, corrected and imported again. Only the builders who work on the instance can reach it, from the Manage Agents page, where a preview panel lets you chat with it. Live is the residents' environment: the Agent deployed in Live is what residents find in the chat on the instance's landing page, and later on the city's website.

When Bob imports the Agent, or imports it again after a correction, it changes the Agent in Draft. The Agent in Live does not change until you deploy: one operation that takes the Agent as it is in Draft and deploys it in Live. Until then, residents keep talking to the previous deployment, so nobody meets an Agent that is being repaired. If a deployment turns out to be wrong, undeploying returns the Agent in Live to its previous deployment.

Everything that Bob does in the next sections happens in Draft: the build imports the Agent into Draft, the tests run against it, and the correction in 4.9 replaces it. Deploying the Agent in Live is one instruction to Bob at the end of 4.9. Chapter 11 describes deployment in full; here you perform it once.

The Developer Edition has only the Draft environment: its chat shows the Agents in Draft, and deploying is not possible there. If you use the Developer Edition, skip the deployment at the end of this chapter; chapter 11 returns to it on a tenant.

## 4.6 Agent mode: build and test

Mode: Agent, in a new conversation.

In this step, Bob builds the Agent from the approved design.

Start a new conversation with the plus sign at the top of the chat panel, then select Agent in the mode dropdown. Do not switch to Agent mode in the conversation you have been using.

In the current conversation, Bob has your request, its first proposal, the facts, perhaps a complete Agent that it laid out in the chat before you asked for a design, the design, and your revision. You approved some of that and not the rest. If Bob builds there, all of it is in view, and Bob may take a detail from its early draft instead of from the approved design. In a new conversation, Bob reads only the design file and builds what you approved.

For an Agent this small, the difference rarely shows. The difference matters from chapter 9 onwards, where a design covers four Agents and the discussion behind it is long, and Bob's documentation describes the same practice for moving from a plan to its implementation.

The prompt has two sentences: the first approves the design and the second starts the build. Bob takes everything else from the design file, which the @ mention tells it to read.

```
The design in @design/civic-info-design.md is approved. Build it.
```

The build takes Bob a minute or two. In the run, Bob:

1. Read the design, and then one of the Orchestrate skills loaded by the starting message in chapter 2, the one that knows how Agents are built and tested. Everything that follows comes from the design and from that skill, not from the prompt.
2. Wrote the Agent file `agents/civic_info_agent.yaml`, which is the design turned into the form that watsonx Orchestrate accepts: the name, the model, the instructions with the facts, and the welcome message and starter prompts in the exact structure the platform requires.
3. Imported it. The Agent then exists on the instance, in Draft, where only the builders can use it.
4. Sent the questions from the design, the street light, the fallen tree, the building permit, the bulky item, the property tax, and one of its own, a second question in the same conversation to check that the Agent remembers the first. It reported each answer with its verdict; every test passed.
5. Reported a table of the files it wrote, and a list of ways to try the Agent yourself.

## 4.7 Read the definition

The Agent has been created in watsonx Orchestrate. What you see in Bob is its definition file, `agents/civic_info_agent.yaml`, which Bob wrote and imported. Before Bob, builders wrote this file by hand; now Bob writes it, and you read it. Open it in the File Explorer. The table lists the fields that this guide refers to.

| Field | Purpose |
|---|---|
| Name | The identifier of the Agent: lower case, with underscores. Everything else refers to the Agent by this name |
| Display name | The name that users see |
| Description | What the Agent is for. Other Agents and the Orchestrate interface read it |
| Instructions | How the Agent behaves, and in this chapter, the facts that it knows |
| Model | The language model that the Agent runs on |
| Kind | The type of Agent. It is `native` for every Agent in this guide |
| Style | The reasoning strategy of the Agent. The guide uses the one that Bob selects by default. It appears under two names, `react_core` in the file and `react_intrinsic` on the instance, which are the same style |
| Tools, collaborators, Knowledge Base | Empty in this chapter. Chapters 5, 6 and 9 fill them |
| Welcome message and starter prompts | What a user sees before typing |

The file can contain other fields.

Save your work now, as section 3.6 describes: `Commit everything I changed with a short message saying what was built, and push.` From now on, any change to this file can be undone.

Read the file against the design. The two usually match, but not always. In the run, the design gave the display name Utopia city information and the file left it out, so the Agent appeared under its internal name. The correction in 4.9 includes this.

## 4.8 Meet your Agent

Mode: Agent, same conversation.

Open the watsonx Orchestrate panel. In the Explorer section, move the pointer over the Agents row, click the refresh icon that appears on it, and expand Agents. `civic_info_agent` is there, next to the Agents that were already on the instance.

Do not click the Agent's name. A click saves a copy of the Agent from the instance into the project folder and offers to replace the file that Bob wrote, in a longer format with every field the instance stores. If you click by mistake, choose Cancel in the dialog. If the file is replaced, it becomes a copy of the Agent as the instance holds it: the Agent itself is unchanged, but any change made to the file and not yet imported is lost, and the file you read in 4.7 changes shape. The restore request of section 3.6 brings the file back.

Now talk to it. Bob tested it with the questions from the design; this time the questions are yours. Ask through Bob, one question per message:

```
Ask civic_info_agent: "My recycling bin was not collected this morning. Who do I contact?"
```

Residents will not write their questions as neatly as the design does. Try these:

- The same question, typed in a hurry: "bin not collected today who do i call".
- A question with two departments in it: "I want to build a garden shed and I also need to get rid of the old one. Who do I contact?"
- A question in the middle of the night: "There is water flooding the street from a broken pipe. It is 2 am. What do I do?"
- A question outside its scope: "What time does the public swimming pool open?"
- A follow-up in the same conversation, after the recycling question: "And what if it happens again next week?"

Read each answer with the facts of 4.2 next to you. For the first three, the right department and its contact should be there, and the flooded street should get the urgent line; the swimming pool should get a polite refusal with a pointer to the department most likely to help. The follow-up should be answered as a question about waste collection, with the Waste and Recycling contact, without the Agent asking what "it" refers to.

Keep a note of any answer that contains something not in the facts; 4.9 shows what to do about it.

Until the end of the next section, the Agent exists in Draft only, where you can use it and residents cannot.

## 4.9 Correct a wrong answer

Mode: Agent, same conversation.

Now ask the Agent for something that its facts do not contain:

```
Ask civic_info_agent: "What are the opening hours of Roads and Infrastructure?"
```

The facts give no hours for this department. Inspect the answer. In the run, the Agent replied with Monday to Friday 09:00 to 17:00, which are the hours of Permits and Planning: a language model tends to fill a gap with the most plausible content, and the rule "never invent an answer" stands next to the rule about questions outside the three departments, so the model may read it as limited to those. If your Agent says instead that it has no hours for Roads and Infrastructure, it did better than ours; apply the correction below anyway, so that the hours are in the facts.

Tell Bob what was wrong and how the Agent must behave. Bob knows where the Agent is defined; you do not need to name the file.

```
civic_info_agent gave opening hours for Roads and Infrastructure that are not
in its facts. The hours of Roads and Infrastructure are Monday to Friday 07:00
to 19:00. When a question asks for a detail that is not in the facts, the agent
must say that it does not have that information. Also give the agent the
display name "Utopia city information", as in the design. Import the agent
again and ask it the same question.
```

Bob changes the definition file and imports it again before it asks the question. Bob may add the new hours to the design as well, so that the design and the Agent agree. The Agent now answers with the hours. Importing a file with the name of an existing Agent replaces that Agent instead of creating a second one.

Ask one more question that the facts do not cover, for example "Who is the head of the Permits department?". The Agent should now say that it does not have that information and give the department's contact.

**Deploy the Agent in Live**

The Agent is corrected and tested, but it exists only in Draft, so residents cannot see it. To deploy it in Live, send one instruction:

```
Deploy civic_info_agent from draft to live.
```

Bob runs the deployment and reports that the Agent was deployed. Open your watsonx Orchestrate instance in the browser: the Agent is now in the chat on the landing page, with its welcome message and its two starter prompts, for anyone who has access to the instance. On the Developer Edition, skip this step; deployment is not available there.

From now on, the Agent exists in both environments, and you need to know which one you are talking to. The next time you ask Bob to change the Agent, the change goes to Draft, and the Agent deployed in Live keeps answering as before until you deploy again. The same goes for questions: when you ask Bob to send a question to the Agent, it reaches the Agent in Draft, because the operation that Bob uses to chat with an Agent, `chat_with_agent` on the Orchestrate server, is built for Draft and has no option to point at Live. While you build, you test what you change, and residents never see it. To talk to the Agent deployed in Live, the one residents talk to, use the chat in watsonx Orchestrate.

## 4.10 Summary

A resident of Utopia can now ask who to tell about a dark street light and get the right department, with its contact and its hours, from an Agent that did not exist one hour ago. You described the Agent, approved a design and corrected one answer; Bob wrote everything else. Five things from this chapter apply to every Orchestrate Agent that follows:

- An Agent project goes through Bob's three modes: Ask mode to understand the request, Plan mode to write the design, Agent mode to build and test.
- You approve the design before Bob builds, and anything that you want built must be in the design.
- One file defines an Orchestrate Agent. Importing the file creates the Agent in Draft; importing it again replaces the Agent.
- The instructions are all that the Agent knows, so a wrong answer is corrected there.
- Until you deploy, the Agent exists in Draft only. Deploying puts the Agent as it is in Draft into Live, the environment that users see.

You built the first Agent, tested it, found a gap in its facts, corrected it and, on a tenant, deployed it in Live, in about one hour and without writing code. Every Orchestrate Agent in the rest of the guide is made the same way, and only the components change.

The Agent knows twenty lines of facts, and a city has far more than that. Can a shed be built without a permit, and which bin does a broken mirror go in? How loud can a party be after ten at night? The answers are in the city's guides and regulations, and no Agent instruction can hold pages like these. In chapter 5, Bob gives those documents to the Agent as an Orchestrate Knowledge Base, and the Agent answers from them and names the document.
