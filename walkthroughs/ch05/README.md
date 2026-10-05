# Chapter 5 files

Files produced by chapter 5, as built with Bob on a watsonx Orchestrate tenant:

- `design/city-regulations-design.md`: the design that Bob wrote in Plan mode.
- `knowledge-bases/building_permit_guide.txt`, `waste_sorting_rules.txt`, `noise_ordinance.txt`: the three city documents that Bob wrote from the rules of section 5.3.
- `knowledge-bases/city_regulations.yaml`: the Knowledge Base definition.
- `agents/civic_info_agent.yaml`: the Agent with the Knowledge Base attached and the extended instructions.

To start the guide at chapter 6 without building this chapter, send Bob these instructions in Agent mode: `Import walkthroughs/ch05/knowledge-bases/city_regulations.yaml into my instance, wait until the knowledge base is ready, then import walkthroughs/ch05/agents/civic_info_agent.yaml.`
