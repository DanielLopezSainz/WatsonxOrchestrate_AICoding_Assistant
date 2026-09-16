# Design: Lumen Logistics employee helpdesk agent

## What was asked
An agent that answers employees' questions about how to reach IT, HR and Facilities at Lumen Logistics, using a short set of facts. It does not look anything up in other systems and it does not create tickets.

## What exists on the instance today
Two stock agents (DocProcessing and AskOrchestrate). No tools, no knowledge bases, no connections. Nothing to reuse; nothing conflicts with the proposed name.

## Proposed agent
- Name: lumen_helpdesk_agent
- Display name: Lumen Logistics helpdesk
- Model: groq/openai/gpt-oss-120b (the platform default)
- Tools: none. All the facts fit in the instructions.
- Collaborators: none.
- Knowledge base: none.

## Facts the agent will know (from the answers in the Discover phase)
- IT service desk: it-help@lumen-logistics.example, extension 4100, Monday to Friday 08:00 to 18:00. Password resets are self-service at https://it.lumen-logistics.example/reset.
- HR: hr@lumen-logistics.example, extension 4200, Monday to Friday 09:00 to 17:00. Payslips are in the HR portal, not by email.
- Facilities: facilities@lumen-logistics.example, extension 4300. Badge and door access problems go to Facilities. Urgent building problems (water, power, alarms) go to extension 4444, any time.

## Behaviour
- Answer in two or three sentences, always with the contact to use.
- If the question is outside these three teams, say so and point to the closest team; do not invent an answer.
- Friendly, plain, no jargon.

## Build order
1. Write agents/lumen_helpdesk_agent.yaml.
2. Import it into the instance (draft).
3. Test with three questions, reasoning included: a badge problem, a password reset, and a question outside scope.
4. Report.
