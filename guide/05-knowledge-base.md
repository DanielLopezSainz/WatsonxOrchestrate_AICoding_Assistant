# Chapter 5. Give the agent the city's regulations

Level: beginner. Time: about 60 minutes. Prerequisites: chapter 4 completed, or its agent imported from the walkthrough folder as the chapter's Overview describes.

## Overview

Suppose that you want to build a garden shed. It is nine in the evening, and you do not want a phone number: you want to know whether you need a permit. You ask CivicPulse. The agent from chapter 4 can only tell you that Permits and Planning handles permits and when they open. It knows twenty lines of facts, and the answer to your question is on page three of the city's building permit guide.

In this chapter, the agent gets the city's guides and regulations: the building permit guide, the waste sorting rules and the noise ordinance. Bob writes the three documents for the City of Utopia, puts them into a knowledge base, and connects the agent to it. The agent then answers from the documents: whether a shed needs a permit, which bin a broken mirror goes in, how loud a party can be after ten at night, and it names the document that the answer came from.

The component introduced in this chapter is the knowledge base. Everything else stays as in chapter 4: one agent, the same facts in its instructions, no tools.

Skip this chapter if you have already connected a knowledge base to an agent with Bob. To continue with chapter 6 without building it, send Bob these instructions in Agent mode: `Import walkthroughs/ch05/knowledge-bases/city_regulations.yaml into my instance, wait until the knowledge base is ready, then import walkthroughs/ch05/agents/civic_info_agent.yaml.`

## 5.1 Before you start

- The setup from chapter 2, complete.
- The agent `civic_info_agent` from chapter 4 on your instance, in draft, with the correction of section 4.9. If you skipped chapter 4, import it as described in that chapter's Overview.
- A new conversation in Bob for this chapter.

Check that the agent is there: in Ask mode, ask `Which agents exist on my instance?` and confirm that `civic_info_agent` is listed.

## 5.2 What a knowledge base is

An agent's instructions can hold a page of facts. A city's regulations run to hundreds of pages, change every year, and are written by people who will never see the agent's instructions. A knowledge base is how an agent uses documents like these.

A knowledge base is a set of documents that watsonx Orchestrate indexes, so that an agent can search them. When a resident asks a question, the agent looks for the passages of the documents that are closest to the question, reads them, and answers from them. The documents stay as they are; nobody rewrites a regulation into instructions.

**When a knowledge base is the right component**

The question to ask about any information that an agent must know is where it lives and who maintains it. Instructions are right for a small, stable set of facts that the agent's builder owns, like the three departments of chapter 4. A knowledge base is right when the information:

- Is too large for instructions. A permit guide, a product catalogue, an employee handbook.
- Already exists as documents, written and maintained by other people. The legal department updates the regulation; the HR team updates the handbook; the agent must follow without anyone touching its definition.
- Must be quoted, not paraphrased. A resident who asks about a fee or a deadline wants the official wording and the document it comes from.

Typical knowledge bases in real deployments: the policies and procedures of a company for an employee assistant; product documentation and troubleshooting guides for a support agent; contracts, terms and tariffs for a customer service agent; regulations and forms for a public service, which is this chapter's case. In each one, the documents exist before the agent does, and they keep changing after the agent is built.

A knowledge base is not the right component for information about one person or one case, such as the status of a permit application or a customer's last order. That information lives in a system, changes by the minute, and is fetched with a tool, the subject of chapter 6.

**What to know before building one**

- Documents are files: text, PDF, Word, PowerPoint, Excel, CSV or HTML. A knowledge base holds up to 100 of them, with size limits per type, for example 25 MB for a PDF and 5 MB for a text file. Plain text is the simplest format and the one that this chapter uses.
- Indexing takes time. After the import, the knowledge base is not ready at once; the platform processes the documents in the background, and an agent can use the knowledge base only when its status is ready. Bob checks the status for you.
- A knowledge base belongs to the instance, not to one state of an agent. It is shared by the draft and the live copies of every agent that uses it, so a change to the documents reaches residents at once, without a deployment.
- watsonx Orchestrate also has a feature called chat with documents, which lets a user attach a file to one conversation. It is not a knowledge base: the file is not indexed for other conversations, and this guide does not use it.

An agent uses a knowledge base when its definition names it. The agent's instructions decide when to search: in this chapter, for every question about a rule or a procedure, while the contacts and hours stay in the instructions.

**The documents of this chapter**

In a real project, the city's documents would exist and you would give them to Bob. The City of Utopia is fictional, so in this chapter you give Bob the rules and Bob writes the documents. Everything else, the knowledge base, the agent, the questions, works exactly as it would with real documents.

**How it works, in a few lines**

What you built in this chapter is what the industry calls retrieval-augmented generation, RAG for short: the agent retrieves passages from documents and the language model generates the answer from them. In watsonx Orchestrate it works like this.

- At import, each document is split into passages, and each passage is converted into a list of numbers that captures its meaning, called an embedding. An embedding model does the conversion; the built-in knowledge base uses an IBM model named `slate-125m-english-rtrvr-v2` unless you choose another. The passages and their embeddings are stored in a vector database that comes with the platform, Milvus. This is the indexing that made Bob wait.
- At question time, the resident's question is converted the same way, the database returns the passages whose embeddings are closest to it, and the language model writes the answer from those passages. The agent named the document in its answers because its instructions asked for it; the passages themselves carry the document they came from.
- The built-in database is one option. If your organisation already keeps its documents in Milvus, Elasticsearch, OpenSearch or Astra DB, a knowledge base can point at that index instead of importing files, and the agent uses it the same way.

## 5.3 Ask mode: describe the knowledge

Mode: Ask, in a new conversation.

The purpose of this prompt is the same as in chapter 4: before anything is written, Bob must understand what you want, and tell you what it needs to know. This time the request has two parts, the documents and the change to the agent, and the documents do not exist yet. Bob will write them, and it needs to know what they must contain.

The prompt says which documents the city needs, what each one covers, the questions that residents must get answered, and that the documents are fictional and Bob's to write.

```
I want civic_info_agent to answer questions from the City of Utopia's guides
and regulations, not only from the facts in its instructions. Three documents
to start with: the building permit guide (when a permit is needed, how to
apply, fees and processing time), the waste sorting rules (which bin for which
waste, glass, bulky items, hazardous waste), and the noise ordinance (quiet
hours, construction work, private events, how to complain). The documents do
not exist yet; they are fictional and you will write them. Residents must get
answers to questions like "Do I need a permit for a garden shed?", "Which bin
does a broken mirror go in?" and "How loud can a party be after 10 pm?".

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob queries the instance and answers with the three parts you know from chapter 4. Its questions are about the format and tone of the documents, the kind of knowledge base, the numbers to use in the rules, and how the agent's instructions should change.

Bob may end its answer with a set of suggested answers to click. They are Bob's own defaults, and some of them, such as Markdown for the documents, are not what this chapter needs. Do not click any of them; type the answer below instead.

The second prompt is your answer to Bob's questions, as in chapter 4. Its purpose is to give Bob the content of the documents and your decisions, so that Bob can write the design in the next step. Nothing is created: Ask mode is still the right mode, and Bob only records the answers. The rules in the answer are the facts of this chapter; everything that the agent answers about regulations must come from them.

```
These are my answers. The documents are plain text files with the .txt
extension, not Markdown, written as plain-language handouts for residents with
short sections. The knowledge base is the built-in one of the instance. Use the
following rules as they are.

Building permit guide. A permit is required for any new building, extension
or structure, except detached garden structures with a floor area under 10
square metres and a height under 2.5 metres, which need no permit. Applications
are submitted online at https://services.utopia.example/permits with a site
plan and drawings. The fee is 120 for structures under 50 square metres and 300
above. A decision is given within 30 days. Work must not start before the
decision.

Waste sorting rules. Four bins: green for food and garden waste, blue for paper
and cardboard, yellow for plastic and metal packaging, grey for everything
else. Glass bottles and jars go to the street containers, not to the bins.
Broken mirrors, window glass and drinking glasses are not accepted as glass:
wrap them and put them in the grey bin. Bulky items are collected on request,
booked online at https://services.utopia.example/bulky, up to three items per
booking, within ten working days. Paint, batteries and chemicals go to the
recycling centre at 14 Mill Road, open Saturdays 08:00 to 13:00.

Noise ordinance. Quiet hours are 22:00 to 07:00 from Sunday to Thursday and
23:00 to 08:00 on Friday and Saturday. During quiet hours, music must not be
audible outside the property. Construction work is allowed from 07:00 to
19:00 on weekdays and 08:00 to 13:00 on Saturdays, and never on Sundays.
A private event can get a one-night exemption, requested online at
https://services.utopia.example/noise at least five days in advance. Noise
complaints are reported at the same address.

The knowledge base is named city_regulations and is attached to the agent;
the chat with documents feature stays off. The agent keeps its current facts
and instructions, and searches the knowledge base for any question about a
rule, a procedure, a fee or a deadline. An answer taken from a document can be
longer than three sentences, up to a short paragraph, and still ends with the
contact of the department when one is involved. When a question is about a rule that
the documents do not cover, the agent says that it does not have that
information. In every answer taken from a document, the agent names the
document.
```

Bob confirms the answers. As in chapter 4, it might outline the documents or the design in the chat. The design is written in the next step.

## 5.4 Plan mode: write the design

Mode: Plan, in the same conversation.

This design has more in it than the one in chapter 4: three documents to write, a knowledge base to define, and a change to an existing agent. That is why it is worth a document of its own that you read before anything is built.

```
Write the design for this change into design/city-regulations-design.md.
```

Bob asks for approval to write the file, writes it, and shows a summary. Open the file and check that it contains the following:

| Content | What to check |
|---|---|
| The three documents | A name and an outline for each, covering every rule from your answer, as plain text files in the `knowledge-bases` folder |
| The knowledge base | Its name, `city_regulations`, its description, and the three documents |
| The change to the agent | The knowledge base attached to `civic_info_agent`, and the instructions extended: search for rules, say when a rule is not covered, name the document; the facts of chapter 4 unchanged |
| The build order | Documents first, then the knowledge base, then wait for it to be ready, then the agent |
| The tests | The three questions of the Overview at least, each with what a correct answer contains and which document it comes from |

The build order matters here for the first time. The agent must not be imported with a knowledge base that is not ready; the design should say so, and Bob should wait.

## 5.5 Approve the design

Mode: Plan, same conversation.

Read the design once. If a rule is missing or a test question is wrong, ask Bob to change it, as in chapter 4. When it says what you mean, it is approved: the approval is the first line of the next prompt.

## 5.6 Agent mode: build and test

Mode: Agent, in a new conversation.

```
The design in @design/city-regulations-design.md is approved. Build it.
```

This build creates more than the one in chapter 4, and part of it takes time. Bob:

1. **Writes the three documents**, the building permit guide, the waste sorting rules and the noise ordinance, as text files in the `knowledge-bases` folder. Open one while Bob continues: residents' answers will come from these pages.
2. **Writes the knowledge base definition**, a short file that names `city_regulations` and lists the three documents.
3. **Imports the knowledge base and waits.** The platform indexes the documents in the background; Bob checks the status until it is ready, which takes a few minutes on a tenant.
4. **Updates the agent**: the knowledge base is attached, the instructions are extended, and the agent is imported again, replacing the draft.
5. **Tests** the agent with the questions from the design and reports.

Approve each request as it comes. If an import fails, Bob reads the error and corrects the file before continuing.

## 5.7 What Bob built

Bob has just produced the three pieces of a knowledge base, and the easiest way to understand what a knowledge base is, is to open them. Go to the `knowledge-bases` folder in the File Explorer.

**The documents.** Three text files: the building permit guide, the waste sorting rules and the noise ordinance. Open the permit guide. It reads like a leaflet from a city office: a title, a few headings, and under each one the rule in plain sentences, with the numbers you gave Bob. Bob may have added examples of its own, such as a shed of 8 square metres that needs no permit and one of 12 that does. These three pages are the agent's new knowledge. When a resident asks about a shed, the agent finds the right passage in this file and answers from it, and when the city changes the rule one day, this is the file that changes; the agent does not.

**The knowledge base definition.** A short file named `city_regulations.yaml`. It is the label on the box: the name of the knowledge base, a sentence describing what the documents cover, so that the agent knows when to look inside, and the list of the three documents. Nothing in it is a rule; it only says which files belong together.

**The agent.** Open `agents/civic_info_agent.yaml` and look for two changes. The name `city_regulations` now appears under `knowledge_base`: the agent has access to the box. And the instructions have a new paragraph that tells the agent what to do with it: search the documents for any question about a rule, say which document the answer comes from, and admit it when the documents do not cover a question. Everything from chapter 4, the three departments and their contacts, is still there.

Bob may also have left files of its own, such as a scripts folder or a test report. They are Bob's working notes, not part of the agent; read them if you are curious, and ignore them otherwise.

Save your work: `Commit everything I changed with a short message saying what was built, and push.`

## 5.8 Ways to interact with watsonx Orchestrate agents

There are two ways to talk to an agent.

- **Using Bob.** You send the question to the agent through Bob: "Ask civic_info_agent: ...". Bob shows you the answer, and because Bob has seen it, you can ask Bob to correct the agent in your next message. This is how the chapters test every agent.
- **From watsonx Orchestrate.** You open your instance in the browser and type the question yourself, in the chat that residents use for the live agent, or in the preview of the draft agent on the Manage agents page.

Remember from chapter 4 that the agent exists in two copies, and keep in mind which one you are talking to. A question sent through Bob always reaches the draft, the copy you are developing. In watsonx Orchestrate you can reach both: the preview of the agent on the Manage agents page talks to the draft, and the chat on the landing page talks to the live copy. The two are not necessarily at the same level: right now the draft searches the documents and the live copy does not, and they stay different until you deploy in 5.9.

In this section you try both. The documents in your knowledge base were written by your Bob, in its own words, but from the rules you gave in 5.3, so the answers to the questions below are in them whatever the wording. If an answer differs from what the rules say, open the document: if the rule is there, ask Bob to correct the agent as you did in chapter 4; if it is missing, ask Bob to add it to the document and import the knowledge base again.

**Using Bob.** Ask the three questions from the Overview, one per message:

```
Ask civic_info_agent: "Do I need a permit for a garden shed of 8 square metres?"
```

```
Ask civic_info_agent: "Which bin does a broken mirror go in?"
```

```
Ask civic_info_agent: "How loud can a party be after 10 pm on a Saturday?"
```

Read each answer with your rules of 5.3 next to you. The shed needs no permit, because it is under 10 square metres, provided it is under 2.5 metres high. The mirror goes wrapped in the grey bin, not to the glass containers. On a Saturday, music must not be audible outside the property after 23:00, and a one-night exemption can be requested five days ahead. Each answer names its document, because the instructions ask for it.

Then ask as residents do:

- A question that needs a document and the facts: "I want to build a 60 square metre extension. What does it cost, and who do I call?" The fee is 300, and the contact is Permits and Planning.
- A question with a day in it: "Can the builders work on Sunday morning?" Never on Sundays.
- A question about a rule that the documents do not cover: "Can I keep chickens in my garden?" The agent says that it does not have that information.

**From watsonx Orchestrate.** The agent that searches the documents is still the draft; the live agent is the chapter 4 version until section 5.9. So do not use the chat on the landing page yet: it answers with contacts and hours and no documents. Open your instance in the browser, go to Manage agents, select Utopia city information, and use the preview panel, which talks to the draft. Type the shed question; the same answer comes back, with its document named.

## 5.9 Make the change live

Mode: Agent, same conversation.

The agent that searches the documents is a draft. The live agent from chapter 4 still answers from its twenty lines of facts. Deploy again:

```
Deploy civic_info_agent from draft to live.
```

Bob reports that the agent is live and tells you where residents can find it: in the watsonx Orchestrate chat, with the environment switched to Live in the top-right corner, under its display name, Utopia city information. Go there and ask the shed question. The answer that was only in the draft an hour ago is now the one every resident gets. On the Developer Edition, skip this step.

## 5.10 Summary

The agent can now answer from the city's regulations: a question about a shed, a mirror or a party gets the rule, not a phone number, with the document it came from. Bob wrote the documents, defined the knowledge base, waited for it to be ready, and changed the agent; you described the rules and approved the design.

- A knowledge base is a set of documents that the platform indexes and an agent searches. It holds files, not instructions. An agent that answers this way is what the industry calls retrieval-augmented generation, RAG: when you hear that an agent "uses RAG", it has a knowledge base.
- After the import, the platform needs a few minutes to index the documents. The knowledge base can be attached to an agent only when its status is ready.
- The agent's instructions decide when to search and what to say when the documents have no answer.
- A knowledge base belongs to the instance. A change to its documents reaches the draft and the live agent at once.

The agent knows what the city has written down. It still cannot look anything up about a particular resident: whether their permit application has been approved, or when their street's bins are collected. That information is not in a document; it is in the city's systems. In chapter 6, Bob gives the agent its first tools, and the answers start depending on who is asking.
