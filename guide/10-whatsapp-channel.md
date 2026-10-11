# Chapter 10. CivicPulse on WhatsApp: the Orchestrate Channel

Level: intermediate. Time: about 45 minutes. Prerequisites: chapter 9 completed, or its four Agents imported from the walkthrough folder as that chapter's Overview describes, and deployed in Live.

## Overview

Saturday morning at the gym. A dumbbell slips out of your hand, and the mirror behind the rack comes down in pieces. The manager arrives with a broom, looks at the pieces, looks at you, and says the glass container outside is full of bottles and nobody ever told him where a mirror goes. He looks angry, and you had better have an answer. On your phone you have the WhatsApp contact of the City of Utopia. You send a WhatsApp message: "Does a broken mirror go in the glass bin?" After a few seconds, you get the answer. You did not need to call the 311 Call Center, or even log in to the city's website. An Orchestrate Channel saved your gym membership.

In this chapter, the front desk Agent of chapter 9 becomes reachable on WhatsApp. Bob creates an Orchestrate Channel for it, and Twilio, the telephony service that carries the messages, connects WhatsApp to the Agent.

To use the Orchestrate Agents you are not limited to a standard chatbot page: an Orchestrate Channel connects an Agent to different messaging services like WhatsApp, SMS, Slack, Teams...

This chapter needs an Orchestrate instance: on the Developer Edition, the ADK refuses to create a Channel, so read the chapter without running it. No later chapter depends on it.

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

When Bob creates a Channel, the platform gives it an event URL, an address on the instance that belongs to that Channel. The outside service, Twilio here, is told to send every incoming message to that address, and the platform runs the Agent and returns the answer to Twilio, which delivers it to the phone. A Channel holds the credentials of the outside service, in this case Twilio's two values, so that the platform can send answers through it.

**Draft and Live**

A Channel is attached to an Agent in one environment. A Channel on the Agent in Draft is for testing by builders; a Channel on the Agent in Live is for residents. The two are separate assets with separate event URLs. This chapter creates the Channel in Live because chapter 9 deployed the Agent there, and a test from your phone then follows the path that residents use.

**Twilio and its test number**

Twilio is a service that companies use to send and receive SMS and WhatsApp messages from their applications. A business number on WhatsApp requires a business account approved by Meta; for development, Twilio provides a shared test number, the Sandbox, that a phone joins by sending it a code. This chapter uses the Sandbox. Its limits: a phone stays joined for three days and must then send the code again; a trial account lasts 30 days and includes 100 WhatsApp messages; messages can only be exchanged with phones that joined. For the city's real number, the city applies for a WhatsApp business account through Twilio and the Channel stays the same.

**Where you will use it**

A Channel makes an Agent available outside watsonx Orchestrate. The Agents you build after this guide will answer employees in Slack or Teams and customers on WhatsApp, with the same definition that you test in the Orchestrate chat. For each new Channel, you set an account and an address on the outside service, and on the Orchestrate side you run one command.

IMPORTANT: a Channel holds credentials, like a Connection. The two Twilio values go into `.env` as in chapter 7 and reach the instance through the command that Bob runs, never through the chat; the only file that holds the Auth Token is `.env`, which git ignores.

## 10.3 Create the Twilio account and join the test number

The Orchestrate Agent that you created in the previous chapters will be reachable through WhatsApp. For the test, you use your own phone: a free Twilio account, created with your phone number, lets your WhatsApp talk to the Agent. Create the account as described below. You do this section by hand, in Twilio's console and on your phone, and Bob takes over in 10.4.

1. Create a free account at twilio.com. Twilio asks for an email address, then for your phone number, which it verifies by SMS. Twilio does not ask for a payment card. Answer the questions of the sign-up as you like.
2. In the console, from the Account Dashboard, open the **Develop** tab of the left panel, then **Messaging**, then **Try it out**, then **Send a WhatsApp message**. The page has two tabs. The first, **Sandbox**, shows Twilio's test number, `+1 415 523 8886`, your join code, `join` followed by two words, and a QR code.

Screenshot: the Sandbox tab, with the number, the join code and the QR code.

3. Scan the QR code with your phone, or open WhatsApp and send the join code to the test number. Use the phone whose number you gave at sign-up: a trial account exchanges messages only with verified numbers, and that one is verified. Twilio replies in WhatsApp that you are all set. Your number then appears under Sandbox Participants on the second tab of the page.

**The two values that the Channel needs**

The Channel sends Twilio two values: the **Account SID** and the **Auth Token**. You can get them on the Twilio home page, Console, under Account Info, and add them to `.env` in your project folder as you can see below:

```
WO_INSTANCE=<the URL of your instance>
WO_API_KEY=<the API key of your instance>
UTOPIA_311_API_KEY=<the value from chapter 7>
TWILIO_ACCOUNT_SID=<the Account SID, which starts with AC>
TWILIO_AUTH_TOKEN=<the Auth Token>
```

## 10.4 Ask mode: describe the Channel

Mode: Ask, in a new conversation.

Use a similar structure for any prompt that you use in the future to create a WhatsApp Channel. This prompt gives Bob the five requisites described below and mentions the ADK. You also need to add a "no number needed" instruction; otherwise Bob will try to get one. Last, name the ADK command, `orchestrate channels create`.

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

In the previous chapters, Bob wrote a design that you approved, and the build prompt was one line. A Channel is too small for that: one command creates it. So this chapter skips Plan mode. It goes from Ask mode to Agent mode in the same conversation, where Bob keeps what it found in 10.4, and it uses the structured prompt of chapter 3, the one with six parts. Each part answers a question that Bob would otherwise decide alone:

- Goal: what must exist when Bob is done.
- Context: the files and the environment Bob works with.
- Constraints: the command to use, the two fields, no sender number, nothing shown in the chat, the Agent untouched.
- Deliverable: what Bob must show you at the end, here the event URL.
- Verify: how Bob proves that the Channel exists, the part of the goal that Bob can check; Twilio's part is 10.7 and the test 10.8. Bob's answer then ends with that check.
- Stop: when Bob must ask you instead of continuing.

For another WhatsApp Channel, keep the Constraints part as it is here and have the Verify part ask for the list of the Agent's Channels.

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

Approve each request as it comes. Bob runs the command, reports the event URL, and ends with the list of the Agent's Channels in Live: one entry, CivicPulse WhatsApp, with its identifier and its creation time.

The event URL, the address of this Channel on your instance, names your tenant, the Agent, the environment, the type of Channel and the identifier of the Channel, and ends with `/events`. Twilio sends to this address every WhatsApp message that a joined phone sends to the test number, and the platform answers through it. The URL is the only link between Twilio and your Agent; section 10.7 pastes it into Twilio. Copy it from Bob's answer.

## 10.6 Look at the Channel with Bob

Mode: Ask, same conversation.

Before starting testing, run these three prompts with Bob to get some information about the Channel:

```
List the channels of civic_info_agent in live and in draft.
```

One Channel in Live, CivicPulse WhatsApp, with its identifier and its creation time; none in Draft.

```
Show me the details of the channel CivicPulse WhatsApp of civic_info_agent in live, including its event URL.
```

Bob shows the record that the platform keeps for the Channel: its type, its name and description, its own identifier, and the identifiers of the Agent and of the environment it belongs to. The Account SID is there, as an identifier. The Auth Token shows as redacted: the platform never returns a secret, and the export of the next prompt shows it as null. The record does not include the event URL, which the platform prints once, when the Channel is created, and does not store. Bob rebuilds it from the identifiers of the record, in the order given in 10.5. If you ever lose the URL, this question gives it back.

The third prompt exports the Channel to a file in the project. A Channel created with a command has no file of its own; the export gives it one. That file is useful when you need to:

- Recreate the Channel elsewhere: on a second instance, for example the city's production instance after a test instance, or on the Agent in Draft to test a change before residents see it. The file says what to recreate, the type, the name and the description; the command of the import script recreates it, with the token from the `.env` of that project.
- Keep a record of what is on the instance, in the project and under git, as the Agent definitions are. When someone changes the Channel in the interface, a new export shows the difference.
- See what the instance returns for a Channel that holds credentials.

```
Export the channel CivicPulse WhatsApp of civic_info_agent in live to exports/whatsapp-channel.yaml and show me the file.
```

A file with the type, the name, the description, the Account SID, a feedback setting (`enable_feedback: false`), and `twilio_authentication_token: null`. The instance returns the Account SID but not the secret. A YAML file cannot read `.env` and the token must never be typed into it, so the file is not imported as it is; the command of the import script recreates the Channel from the same values.

## 10.7 Tell Twilio where to send the messages

Configure Twilio to send the messages to the event URL discussed in 10.5.

1. In Twilio's console, from the Account Dashboard, open the **Develop** tab of the left panel, then **Messaging**, then **Try it out**, then **Send a WhatsApp message**, and click the second tab, **Sandbox settings**.
2. In the field **When a message comes in**, replace the address that Twilio put there (its own demo reply) with the event URL from Bob's answer. Leave the method on **POST**. Leave **Status callback URL** empty.
3. Click **Save**. The setting is not applied until you click Save.

Screenshot: the Sandbox settings tab, with the event URL in the field and the Save button.

## 10.8 Try it

In WhatsApp on your phone, in the conversation with the test number, send:

```
Does a broken mirror go in the glass bin?
```

The answer arrives within a few seconds, from the Waste Sorting Rules: a broken mirror does not go in the glass container, with the Waste and Recycling contact. Then keep the phone in hand: everything the Agents learned in the earlier chapters now answers on WhatsApp. Send these, in any order:

- `What are the quiet hours?` The front desk Agent answers itself, from the Noise Ordinance.
- `Which day is the green bin collected at 18 elm st?` The address as you would type it on a phone; the Address Registry of chapter 8 corrects it and the Waste and Recycling department gives the day.
- `Where is my permit application PP-2026-0412?` The Permits and Planning department reads the record of chapter 6: under review.
- `There is a pothole at 7 harbour ln.` A report to the 311 Call Center of chapter 7, and a request number in return.
- `Which streets are in the Old Town district?` The Address Registry again: Mill Road, High Street, Station Road.
- `Do I need a permit for a garden shed of 12 square metres?` The Building Permit Guide, through the Permits and Planning department: over 10 square metres, a permit is required. The answer may come in two messages, the second one, "How do we know?", naming the document; that is the platform's citation, which the chat shows as a footnote and WhatsApp as a message.
- `When does the swimming pool open?` The refusal of chapter 9: the question is outside the three departments, so the Agent names an office that might help and invents no contact.

WhatsApp shows only the answers. To see the reasoning, which Tool was called and which department answered, ask the same question through Bob, with `Ask civic_info_agent:` in front and the request for reasoning. Bob's chat operation reaches the Agent in Draft. Nothing changed in Draft since the deployment of chapter 9, so the reasoning through Bob shows which department and which Tool answer that question; the steps of a second run may differ in detail from the first.

If no answer arrives, Twilio's logs show where the message stopped. In the console, **Monitor**, then **Logs**, then **Messaging**. If your message is not listed, Twilio did not receive it. The usual reason is that your phone is no longer joined, which happens after three days, so send the join code again. If the message is listed with an error 11200, Twilio called the event URL and got no valid answer. One cause is a URL that no longer belongs to a Channel on the instance, for example after a Channel was deleted and created again. Reload the Sandbox settings page, paste the URL from Bob's answer, click Save, and reload the page to check that it holds. To confirm that the Channel exists, ask Bob `List the channels of civic_info_agent in live.`.

## 10.9 What Bob built

- The instance holds one Orchestrate Channel, CivicPulse WhatsApp, of type Twilio WhatsApp, attached to `civic_info_agent` in Live. It holds the two Twilio values. The Agent is unchanged.
- The project holds one command in the import script, the one that creates the Channel with the two values read from `.env`; one command in the delete script, placed before the removal of the Agent; and `exports/whatsapp-channel.yaml`, the export of 10.6, with the token empty.
- Bob's MCP tab and the Agent files are unchanged, because a Channel is attached to an Agent from the outside.

The Channel belongs to the Live environment of the Agent. When a later chapter changes the Agent in Draft and deploys it again, the Channel stays where it is and residents on WhatsApp get the new version.

Save your work: `Commit everything I changed with a short message saying what was built.`

## 10.10 Summary

The Utopia Agent is now reachable from WhatsApp. Take this chapter as your walkthrough guide when you perform similar implementations: the items that should be included in the prompts, the list of facts to verify and test, and the questions to ask Bob about the result.

- An Orchestrate Channel connects an Agent in one environment to an outside service: web chat, WhatsApp, SMS, Slack, Teams, Facebook Messenger, Genesys. One Channel of each type per environment.
- The platform gives each Channel an event URL; the outside service sends every message there and receives the answer.
- A Channel holds the credentials of the outside service. They reach the instance through `.env` and the command, as a Connection's do.
- Twilio's Sandbox is a shared test number for development; the city's own number comes with a WhatsApp business account, and the Channel does not change.

The prompt of 10.4 follows the practice of chapter 8 for any new asset, and the same six points apply to a Connection, a Toolkit or the next Channel you create:

1. Name the Orchestrate asset to create, and its type as the ADK lists it.
2. Name the Agent it belongs to and the environment.
3. Say where the credentials are and that the command reads them from the environment; never write a value in the prompt (here, the two Twilio values in `.env`).
4. Say what is not needed when Bob tends to ask for it (here, the sender number).
5. Say what must not change (here, the Agent).
6. End with the three questions: what Bob understood, what it needs, what exists.

In chapter 11, CivicPulse is added to the city's website with the web chat Channel.
