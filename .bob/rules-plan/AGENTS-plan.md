# Design phase (Plan mode)

Owner: Daniel Lopez Sainz, IBM. Last reviewed: 2026-09-17.

In this phase you write the design and nothing else. You may write files under `design/`. Do not import anything, do not create anything on the instance, do not run commands.

Write the design to `design/<name>-design.md` with these sections, in this order:

1. What was asked. Two or three sentences.
2. What exists on the instance today. From the inventory you made in the Discover phase; say what is reused.
3. Proposed agents. For each: name, display name, one-line purpose, model, tools, collaborators, knowledge base. Keep every agent at ten tools and collaborators or fewer.
4. Proposed tools, connections, knowledge bases and workflows. For each: name, what it does, what it needs (a connection, documents, a package).
5. Behaviour. The rules the agents follow: tone, length, what to do with unknowns.
6. Build order. Numbered steps in dependency order: connections, then tools and toolkits, then knowledge bases (wait until ready), then collaborator agents, then the top agent, then tests.
7. Tests. The questions that will be asked at the end and what a correct answer contains.

Show the design to the user and end with: "Waiting for your approval before the Build phase." Revise the file if they ask for changes; do not start building until they say yes.
