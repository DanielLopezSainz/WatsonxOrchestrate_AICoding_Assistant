# Chapter 9 files

Files produced by chapter 9, as built with Bob on a watsonx Orchestrate tenant:

- `design/collaborators-design.md`: the design that Bob wrote in Plan mode, with the sixteen test scenarios and the build steps at the end. Its sentences on hiding the department Agents were aligned with the prompt of 9.3, which keeps them visible.
- `agents/permits_agent.yaml`, `agents/roads_agent.yaml`, `agents/waste_agent.yaml`: the three department Agents, each with the Tools, the document and the facts of its department.
- `agents/civic_info_agent.yaml`: the front desk Agent, with no Tools, the three Collaborator Agents, the Knowledge Base for the Noise Ordinance, and the welcome message and starter prompts of chapter 4.

The department Agents are visible in the chat, as section 9.7 explains; a `hidden: true` line at the top level of each file would hide them.

To start the guide at chapter 10 without building this chapter, send Bob these instructions in Agent mode: `Import the four agents in walkthroughs/ch09/agents into my instance, the three department agents first and civic_info_agent last.`
