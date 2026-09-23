# Agent mode

Owner: Daniel Lopez Sainz, IBM. Last reviewed: 2026-09-18.

Build what the approved design says and nothing more, in dependency order: connections, then tools and knowledge bases, then collaborator agents, then the agent that uses them.

- Write each file into its folder before importing it.
- After every import, look at the instance and confirm the artifact is there. If it is not, stop and report.
- Test each agent with the questions from the design, asking for the reasoning. Quote tool calls, results and errors exactly, and propose a fix before applying it.
- Fix by editing the file and importing again under the same name. Say first that this replaces the existing one.
- If an operation fails twice, ask the user to restart the Orchestrate MCP server before falling back to the `orchestrate` command.
- End with a short report: files written, what was imported and verified, the test answers, anything that failed.
