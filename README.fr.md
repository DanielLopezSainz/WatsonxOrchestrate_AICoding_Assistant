# Créer des agents watsonx Orchestrate avec IBM Bob

Utilisez IBM Bob pour créer des agents d'IA complexes sur IBM watsonx Orchestrate. Ce cours s'adresse aux utilisateurs expérimentés d'Orchestrate qui veulent accélérer leurs développements, et aux débutants qui veulent créer des agents complexes. Un minimum de connaissances théoriques sur watsonx Orchestrate est souhaitable, mais pas obligatoire.

*Ceci est la traduction française du [README](README.md). Les chapitres du guide sont en anglais.*

## Ce que vous allez construire

CivicPulse, le service aux habitants de la ville d'Utopia : un agent qui commence avec trois numéros de téléphone et finit en une équipe qui répond aux habitants sur WhatsApp. Chaque chapitre ajoute un composant de watsonx Orchestrate, et à la fin vous les avez tous construits :

- **Agent** : l'accueil de la ville, avec ses instructions, son message de bienvenue et ses suggestions de questions.
- **Base de connaissances** (Knowledge Base) : la réglementation de la ville, que l'agent recherche et cite.
- **Outils** (Tools) : des fonctions Python qui consultent une demande de permis, une réparation de voirie ou le jour de collecte d'une rue.
- **Connexion** (Connection) : la clé d'API du centre d'appels 311, tenue hors de la conversation et utilisée par un outil qui signale les nids-de-poule.
- **Boîte à outils** (Toolkit) : un serveur MCP écrit par Bob, pour que l'agent comprenne « 18 elm st ».
- **Agents collaborateurs** (Collaborator Agents) : un agent par service municipal derrière l'accueil, chacun avec ses propres outils et documents.
- **Canal** (Channel) : le numéro WhatsApp par lequel les habitants joignent toute l'équipe.

## Comment ça marche

Vous écrivez les prompts ; Bob écrit tout le reste. Chaque chapitre suit les trois mêmes étapes : en mode Ask, Bob dit ce qu'il a compris et ce qui existe déjà sur votre instance ; en mode Plan, il rédige une conception que vous lisez et approuvez ; en mode Agent, il construit, importe, teste et rend compte.

## À qui il s'adresse

À toute personne qui doit créer un agent sur watsonx Orchestrate : consultants, architectes, développeurs, analystes métier. Aucune ligne de code n'est écrite à la main, donc aucune expérience de la programmation n'est nécessaire ; si vous en avez, vous lirez ce que Bob écrit et apprendrez la plateforme plus vite. Le guide utilise Bob et l'extension watsonx Orchestrate ADK tels qu'ils sont livrés ; d'autres assistants qui se connectent au serveur MCP de l'ADK watsonx Orchestrate peuvent suivre les mêmes étapes, et le chapitre 2 indique où leur installation est décrite.

## Ce qu'il vous faut

- IBM Bob, version 2.1 ou ultérieure.
- Une instance watsonx Orchestrate, ou la Developer Edition sur votre machine (le chapitre 10 et les déploiements nécessitent une instance).
- Git, que Bob utilise pour vous.
- Un téléphone avec WhatsApp, pour le chapitre 10.
- Environ huit heures, un chapitre par séance.

## Par où commencer

1. Clonez ce dépôt et ouvrez-le dans Bob. Le dépôt est votre dossier de projet : Bob y écrit, et git conserve votre travail.
2. Faites le chapitre 2 : il installe l'ADK, connecte Bob à votre instance et prépare le dossier. Trente minutes.
3. Lisez le chapitre 3, puis créez votre premier agent au chapitre 4.

Vous pouvez aussi commencer à n'importe quel chapitre à partir du 5 : les fichiers des chapitres précédents sont dans `walkthroughs`, avec une instruction à donner à Bob pour les importer.

## Les chapitres

- [Introduction](guide/00-introduction.md) : à qui s'adresse le guide, ce qu'il vous faut, les conventions.
- [Chapitre 1. Ce que vous allez construire](guide/01-what-you-will-build.md)
- [Chapitre 2. Connecter Bob à watsonx Orchestrate](guide/02-connect-your-assistant.md)
- [Chapitre 3. Comment travailler avec Bob](guide/03-how-to-brief-your-assistant.md)
- [Chapitre 4. Votre premier agent Orchestrate](guide/04-your-first-agent.md)
- [Chapitre 5. Ajouter une base de connaissances Orchestrate (RAG)](guide/05-knowledge-base.md)
- [Chapitre 6. Ajouter des outils Orchestrate](guide/06-tools.md)
- [Chapitre 7. Signaler un problème : les connexions Orchestrate](guide/07-connections.md)
- [Chapitre 8. Une recherche d'adresse depuis un serveur MCP : les boîtes à outils Orchestrate](guide/08-mcp-toolkit.md)
- [Chapitre 9. Un agent par service : les agents collaborateurs](guide/09-collaborators.md)
- [Chapitre 10. CivicPulse sur WhatsApp : le canal Orchestrate](guide/10-whatsapp-channel.md)

## Contenu de ce dépôt

```
guide/            les chapitres, dans l'ordre de lecture
walkthroughs/     les fichiers produits par chaque chapitre (ch04 à ch10), pour commencer à n'importe quel chapitre
.env.example      le modèle de votre fichier .env local : l'URL de l'instance, la clé d'API, les clés de test des chapitres 7 et 10
.gitignore        tient .env, les réglages de Bob et l'environnement Python hors de git
```

Au fil des chapitres, Bob et l'extension ADK ajoutent leurs propres dossiers à côté de ceux-ci : `agents`, `tools`, `knowledge-bases`, `connections`, `toolkits`, `models`, `design`, `scripts`, `tests`, `exports`. Ils sont à vous ; validez-les dans git comme l'indiquent les chapitres.

## Versions

Rédigé et testé avec watsonx Orchestrate ADK 2.18.0 et IBM Bob 2.1, sur une instance IBM Cloud, en septembre et octobre 2026. La plateforme et Bob évoluent avec leurs versions ; si une étape se présente différemment chez vous, ouvrez une issue en indiquant le chapitre, la section, ce que vous avez envoyé et ce que vous avez obtenu.

IBM CSM Team, France
