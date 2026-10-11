# Chapter 10. CivicPulse on WhatsApp: the Orchestrate Channel

Level: intermediate. Time: about 45 minutes. Prerequisites: chapter 9 completed, or its four Agents imported from the walkthrough folder as that chapter's Overview describes, and deployed in Live.

## Overview

Saturday morning at the gym. A dumbbell slips out of your hand, and the mirror behind the rack comes down in pieces. The manager arrives with a broom, looks at the pieces, looks at you, and says the glass container outside is full of bottles and nobody ever told him where a mirror goes. He looks angry, and you had better have an answer. In your phone you have the WhatsApp contact of the City of Utopia. You send a WhatsApp message: "Does a broken mirror go in the glass bin?" After a few seconds, you get the answer. You did not need to call the 311 Call Center, or even log in to the city's website. An Orchestrate Channel saved your gym membership.

In this chapter, the front desk Agent of chapter 9 gets a WhatsApp number. Bob creates an Orchestrate Channel for it, and Twilio, the telephony service that carries the messages, connects the number to the Agent.

To use the Orchestrate Agents you are not limited to a standard chatbot page: an Orchestrate Channel connects an Agent to different messaging services like WhatsApp, SMS, Slack, Teams...

This chapter needs an Orchestrate instance: Channels are not available on the Developer Edition, and a messaging service cannot reach an Agent that runs on your machine. On the Developer Edition, read the chapter without running it. No later chapter depends on it.

## 10.1 Before you start

- The setup from chapter 2, complete, with your environment active in the Environment Manager and the Orchestrate server connected in Bob's MCP tab. An activated environment lasts two hours (section 2.4), and a server that shows as disconnected is restarted from the tab (section 2.8).
- The four Agents of chapter 9 deployed in Live: `civic_info_agent`, `permits_agent`, `roads_agent` and `waste_agent`. If you imported them from the walkthrough folder, deploy them as in section 9.9.
- A phone with WhatsApp.
- A Twilio account, created in 10.3. The free trial is enough: it needs no payment card and includes the test number that this chapter uses.
- A new conversation in Bob for this chapter.

To verify that the chapter 9 Agent is in Live, ask in the watsonx Orchestrate chat: `There is a pothole at 7 harbour ln, and which day is the green bin collected there?`. The answer has a request number and a collection day.

## 10.2 What an Orchestrate Channel is

An Orchestrate Channel connects an Agent to a messaging service, a website or a contact-centre platform. The Agent you created does not change; the Channel receives each message from the service, passes it to the Agent, and sends the answer back the same way.

An Agent can have several Channels, one of each type: the same Agent can answer residents on WhatsApp, visitors of the website, and employees in Slack or Teams.

**How a message travels**

When Bob creates a Channel, the platform gives it an event URL, an address on the instance that belongs to that Channel. The outside service, Twilio here, is told to send every incoming message to that address. The platform runs the Agent and returns the answer to Twilio, which delivers it to the phone. A Channel holds the credentials of the outside service, in this case Twilio's two values, so that the platform can send answers through it.

**Draft and Live**

A Channel is attached to an Agent in one environment. A Channel on the Agent in Draft is for testing by builders; a Channel on the Agent in Live is for residents. The two are separate assets with separate event URLs. This chapter creates the Channel in Live, because the Agent there is the one chapter 9 deployed, and because the test from your phone is the test that residents will make.

**Twilio and its test number**

Twilio is a service that companies use to send and receive SMS and WhatsApp messages from their applications. A business number on WhatsApp requires a business account approved by Meta; for development, Twilio provides a shared test number, the Sandbox, that any phone can join by sending it a code. The Sandbox is what this chapter uses. Its limits: a phone stays joined for three days and then sends the code again; a trial account lasts 30 days and includes 100 WhatsApp messages; messages can only be exchanged with phones that joined. For the city's real number, the city applies for a WhatsApp business account through Twilio and the Channel stays the same.

**Where you will use it**

A Channel is how an Agent leaves the builder's screen. The Agents you build after this guide will answer employees in Slack or Teams, customers on WhatsApp, and callers of a contact centre, with the same definition that you test in the Orchestrate chat. The work of each new Channel is on the side of the outside service, an account and an address to set; on the Orchestrate side it is one definition and one command.

IMPORTANT: a Channel holds credentials, like a Connection. The two Twilio values go into `.env` as in chapter 7 and reach the instance through the command that Bob runs, never through the chat or a file of the project.

## 10.3 Create the Twilio account and join the test number

The Orchestrate Agent that you created in the previous chapters will be reachable through WhatsApp. For the test, you use your own phone: a free Twilio account, created with your phone number, lets your WhatsApp talk to the Agent. Create the account as described below; this section is done by hand, in Twilio's console and on your phone, and Bob takes over in 10.4.

1. Create a free account at twilio.com. Twilio asks for an email address, then for your phone number, which it verifies by SMS. No payment card is asked. Answer the questions of the sign-up as you like.
2. In the left menu, open **Messaging**, then **Try it out**, then **Send a WhatsApp message**. The page has two tabs. The first, **Sandbox**, shows Twilio's test number, `+1 415 523 8886`, your join code, `join` followed by two words, and a QR code.

Screenshot: the Sandbox tab, with the number, the join code and the QR code.

3. Scan the QR code with your phone, or open WhatsApp and send the join code to the test number. Twilio replies in WhatsApp that you are all set. Your number then appears under Sandbox Participants on the second tab of the page.

**The two values that the Channel needs**

The Channel sends Twilio two values: the **Account SID** and the **Auth Token**. You can get them in the Twilio home page, Console, under Account Info. Open `.env` in your project folder and add them as you can see below:

```
WO_INSTANCE=<the URL of your instance>
WO_API_KEY=<the API key of your instance>
UTOPIA_311_API_KEY=<the value from chapter 7>
TWILIO_ACCOUNT_SID=<the Account SID, which starts with AC>
TWILIO_AUTH_TOKEN=<the Auth Token>
```

## 10.4 Ask mode: describe the Channel

Mode: Ask, in a new conversation.

Use a similar structure for any prompt that you use in the future to create a WhatsApp Channel. This prompt gives Bob the five requisites described below and mentions the ADK. You also need to add a "no number needed" instruction; otherwise Bob will try to get one. Last, name the command line of the ADK, `orchestrate channels create`.

A Twilio WhatsApp Channel needs:

- The Orchestrate asset named, as in chapter 8: a Channel of type Twilio WhatsApp, the type as the ADK lists it.
- The Agent and the environment: `civic_info_agent` in Live.
- A name for the Channel.
- The two Twilio values, the Account SID and the Auth Token, in `.env`.
- No phone number: the number is Twilio's.

A Channel is created with one ADK command that takes the two values from the `.env` file.

```
I want to add an Orchestrate channel of type Twilio WhatsApp to
civic_info_agent. The city uses Twilio; the account SID and the auth token are
in .env as TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. A Twilio WhatsApp channel
needs only these two values, no sender number. The channel is named CivicPulse
WhatsApp and is created on civic_info_agent in live with the command line of
the ADK, orchestrate channels create, run in the shell with .env loaded so
that the two values are read from the environment variables; do not use the
channel operation of the Orchestrate server, which would need the values in
the chat. The agent is deployed in live and must not change.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Look for these points in Bob's answer:

- Bob understood a Channel of type Twilio WhatsApp on `civic_info_agent` in the Live environment, created with `orchestrate channels create` in the shell and the two values from `.env`.
- Bob finds on the instance the four Agents of chapter 9 and no Channel on any of them.
- Bob shows the command it will run, with `--field account_sid=$TWILIO_ACCOUNT_SID` and `--field twilio_authentication_token=$TWILIO_AUTH_TOKEN`, and asks whether you run it yourself or it runs it in Agent mode. Section 10.5 answers that. If Bob asks for a description of the Channel, it can choose one itself.

## 10.5 Agent mode: create the Channel

Mode: Agent, in the same conversation as 10.4. Do not start a new conversation: Bob's answer of 10.4 is the context of this step.

In the previous chapters, Bob wrote a design, you approved it, and the build prompt was one line. A Channel is too small for that: one command creates it. So this chapter skips Plan mode and goes from Ask mode to Agent mode in the same conversation, where Bob keeps what it found in 10.4, with the structured prompt of chapter 3, the one with six parts. Each part answers a question that Bob would otherwise decide alone:

- Goal: what must exist when Bob is done.
- Context: the files and the environment Bob works with.
- Constraints: the command to use, the two fields, no sender number, nothing shown in the chat, the Agent untouched.
- Deliverable: what Bob must show you at the end, here the event URL.
- Verify: how Bob proves that the Channel exists, so that its answer ends with a check and not with "done".
- Stop: when Bob must ask you instead of continuing.

Use the same structure for any prompt that creates a WhatsApp Channel in the future: the Constraints part carries the same lines as in 10.4, the command line of the ADK, the two fields and "no sender number", and the Verify part asks for the list of the Agent's Channels.

Stay in the conversation of 10.4, switch to Agent mode, and send:

```
Goal: residents reach civic_info_agent on WhatsApp through Twilio.
Context: the Twilio account SID and auth token are in @.env as
  TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. The agent is deployed in live.
Constraints: create one channel of type twilio_whatsapp, named CivicPulse
  WhatsApp, with the description "Residents reach CivicPulse on WhatsApp.",
  on civic_info_agent in the live environment, with the command
  line of the ADK, orchestrate channels create, run in the shell with .env
  loaded so that the two values are read from the environment variables. Do
  not use the channel operation of the Orchestrate server. The channel has two
  fields, the account SID and the auth token; no sender number is needed. No
  value is written in a file or shown in the chat. Change nothing in the
  agent. Add the command to the import script and the channel's deletion to
  the delete script.
Deliverable: the channel created on the instance, and the event URL that the
  platform returned, quoted in your answer.
Verify: list the channels of civic_info_agent in live and show that CivicPulse
  WhatsApp is there.
Stop: if the command returns an error, show me its exact text and wait.
```

Approve each request as it comes. Bob runs the command and reports the event URL: a long address on your instance that ends with `/channels/twilio_whatsapp/<an identifier>/events`. Copy it from Bob's answer; 10.6 needs it.

## 10.6 Tell Twilio where to send the messages

Back in Twilio's console, on the page of 10.3, open the second tab, **Sandbox settings**. In the field **When a message comes in**, replace the address that Twilio put there with the event URL from Bob's answer, leave the method on POST, and click **Save**. The setting is not applied until you click Save.

Screenshot: the Sandbox settings tab, with the event URL in the field and the Save button.

From this moment, every message that your phone sends to the test number reaches the Agent.

## 10.7 Try it

In WhatsApp on your phone, in the conversation with the test number, send:

```
Does a broken mirror go in the glass bin?
```

The answer arrives within a few seconds, from the Waste Sorting Rules: a broken mirror is not accepted as glass and goes wrapped in the grey bin, with the Waste and Recycling contact. Then try the questions of the earlier chapters: the collection day of a street, the status of a permit application, a pothole to report. Each one reaches the department that owns it, as in chapter 9, and comes back in WhatsApp.

WhatsApp shows the answers and nothing else. To see the reasoning, which Tool was called and which department answered, ask the same question through Bob, with `Ask civic_info_agent:` in front and the request for reasoning. Bob's chat operation reaches the Agent in Draft, whose definition is the one deployed in Live, so the steps are the same.

If no answer arrives: check that the event URL in Twilio is the one from Bob's answer and that you clicked Save; check that your phone is still joined, which lapses after three days, by sending the join code again; and ask Bob `List the channels of civic_info_agent in live.` to confirm that the Channel exists.

## 10.8 What Bob built

Open the import script. The Channel is one command at the end, with the type, the name, a description, and the two values as the names of the variables. A Channel has no file of its own in the project: its definition is that command, and the values are on the instance. The delete script has the matching command. When a Channel is exported from the instance, the Auth Token comes back empty.

Bob's MCP tab has nothing new, and the Agent definitions are unchanged: a Channel is attached to an Agent from the outside, in one environment, and the Agent does not know it is there.

The Channel belongs to the Live environment of the Agent. When a later chapter changes the Agent in Draft and deploys it again, the Channel stays where it is and residents on WhatsApp get the new version.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 10.9 Summary

CivicPulse answers on WhatsApp. The Agent is the one of chapter 9; what was added is one Channel on the Agent in Live, and an address in Twilio's settings. Every other Channel type is added the same way: an account on the outside service, one definition, one command, and one address to set.

- An Orchestrate Channel connects an Agent in one environment to an outside service: web chat, WhatsApp, SMS, Slack, Teams, Facebook Messenger, Genesys. One Channel of each type per environment.
- The platform gives each Channel an event URL; the outside service sends every message there and receives the answer.
- A Channel holds the credentials of the outside service. They reach the instance through `.env` and the command, as a Connection's do.
- Twilio's Sandbox is a shared test number for development; the city's own number comes with a WhatsApp business account, and the Channel does not change.

The prompt of 10.4 follows the practice of chapter 8 for any new asset, and the same six points apply to a Connection, a Toolkit or the next Channel you create:

1. Name the Orchestrate asset to create, and its type as the ADK lists it.
2. Name the Agent it belongs to and the environment.
3. Say where the credentials are and that the command reads them from the environment, never the values.
4. Say what is not needed, when Bob tends to ask for it.
5. Say what must not change.
6. End with the three questions: what Bob understood, what it needs, what exists.

Residents who prefer the website are next. In chapter 11, CivicPulse goes on the city's website through the web chat Channel, and the deployed definition is exported as the record of what is live.
