# Chapitre 3. Comment travailler avec Bob

Niveau : débutant. Durée : environ 20 minutes de lecture. Prérequis : aucun.

## Vue d'ensemble

Ce que Bob construit dépend du mode que vous utilisez à chaque étape, du moment où vous approuvez et de ce que vous écrivez dans un prompt. Tous les chapitres suivants suivent cette méthode de travail. L'exemple utilisé tout au long du chapitre est un Agent de la ville d'Utopia.

La méthode utilise un mode de Bob par étape :

- Le mode Ask, pour vous assurer que Bob a compris ce que vous voulez avant que quoi que ce soit ne soit écrit.
- Le mode Plan, pour obtenir une conception que vous lisez et approuvez.
- Le mode Agent, pour construire l'Agent à partir de la conception approuvée et le tester.

Ce qu'il faut lire, selon votre expérience :

| Si vous | Lisez | Sautez |
|---|---|---|
| N'avez jamais utilisé d'assistant d'IA pour travailler | Tout le chapitre | Rien |
| Utilisez ChatGPT, Claude ou un assistant similaire, mais pas Bob | 3.1, 3.2 et 3.5, propres à Bob et à watsonx Orchestrate | 3.3 et 3.4, sur l'écriture des prompts, et 3.6 si vous connaissez git |
| Utilisez déjà Bob dans ses trois modes | 3.2 et 3.5 | Les autres sections |

## 3.1 La méthode de travail recommandée

Vous décrivez le problème et prenez les décisions ; Bob écrit les fichiers, les importe et les teste, et rend compte du résultat, échecs compris. Lorsque vous travaillez avec Bob :

- Commencez les nouveaux projets et les fonctionnalités complexes en mode Plan, pour qu'un plan existe avant que quoi que ce soit ne soit construit.
- Ouvrez une nouvelle conversation pour chaque tâche, avec un objectif précis, et désignez les fichiers par des mentions @ au lieu de coller leur contenu. Avant de mettre en œuvre un plan, ouvrez une nouvelle conversation, pour que la discussion de planification ne consomme pas le contexte et que Bob ne mélange pas planification et mise en œuvre.
- Approuvez en fonction du risque. Trois stratégies sont possibles : l'approbation manuelle de chaque action, l'approbation automatique de certaines actions, et une approche hybride qui approuve automatiquement les actions à faible risque et exige une approbation pour les autres. Le chapitre 2 a configuré l'approche hybride.

Un mode détermine ce que Bob a le droit de faire dans une conversation.

### Mode Ask

Le mode Ask sert à poser des questions et à obtenir des explications. Dans ce mode, Bob peut lire des fichiers, utiliser les serveurs connectés, ce qui pour Orchestrate signifie interroger l'instance et rechercher dans la documentation, et charger des skills. Bob ne peut ni écrire de fichiers ni exécuter de commandes ; utilisez le mode Ask quand vous avez besoin d'informations sans rien modifier.

Dans ce guide, chaque projet d'Agent commence en mode Ask. Bob reformule la demande, liste ce qui existe déjà sur l'instance et pose les questions auxquelles il faut répondre avant de pouvoir écrire une conception. La méthode standard de Bob commence les nouveaux travaux en mode Plan, mais ce guide commence en mode Ask pour que la demande soit comprise avant que la conception ne soit écrite.

Dans l'exemple suivant, le même Agent est utilisé dans les trois modes : un Agent qui indique aux habitants de la ville d'Utopia quel service municipal traite leur question. En mode Ask, vous écrivez :

```
I would like to build an information agent for the residents of the City of
Utopia. It answers questions like "the street light on my street has been out
for a week, who do I tell?" from a fixed set of facts about three city departments. Tell me what
you understood, what you need to know from me, and what already exists on my
instance.
```

Bob interroge l'instance, puis répond en trois parties : ce qu'il a compris, un tableau des Agents, Outils et Connexions qui existent déjà, et une liste numérotée de questions, par exemple quels faits il doit connaître et que répondre lorsqu'une question sort des trois services. Rien n'est écrit ni créé, et vous répondez aux questions dans la même conversation.

### Mode Plan

Le mode Plan sert à planifier une tâche. Bob analyse les exigences, étudie le projet et conçoit les étapes de mise en œuvre. Il peut faire tout ce que permet le mode Ask, et il peut aussi écrire des fichiers ; il ne peut pas exécuter de commandes. Il pose des questions de clarification, demande votre approbation avant d'écrire les fichiers du plan, et les écrit dans le projet au format Markdown. Relisez le plan : le périmètre doit correspondre à votre demande, il doit nommer des fichiers concrets et éviter le flou, et rien ne doit manquer. Demandez des révisions dans la même conversation.

Bob écrit le plan sous forme de document de conception dans le dossier `design` ; vous l'approuvez avant que quoi que ce soit ne soit construit.

Dans la même conversation, vous passez en mode Plan et écrivez :

```
Write the design for this agent into design/civic-info-design.md.
```

Après que vous avez approuvé l'écriture du fichier, Bob l'écrit et affiche un résumé : ce qui a été demandé, ce qui existe sur l'instance, l'Agent proposé avec son nom et son modèle, les faits qu'il connaîtra, son comportement, l'ordre de construction, et les questions de test avec les réponses attendues. Vous lisez le fichier et, s'il manque quelque chose, demandez une modification dans la même conversation ; Bob révise le fichier et attend de nouveau.

### Mode Agent

Le mode Agent sert à mettre en œuvre une idée ou un plan. C'est le moins restreint : Bob lit et écrit des fichiers, exécute des commandes, utilise les serveurs, change de mode, et peut déléguer du travail à des sous-agents. Réservez-le à la construction : fonctionnalités, corrections de bogues, et tout ce qui modifie l'instance. Commencez le mode Agent dans une nouvelle conversation, avec un prompt qui désigne le plan par une mention @.

Dans ce guide, le mode Agent est celui où Bob écrit les fichiers de définition et d'Outils, les importe, teste l'Agent, lit le raisonnement de l'Agent, corrige ce qui a échoué et rend compte.

Vous ouvrez une nouvelle conversation, passez en mode Agent et écrivez :

```
The design in @design/civic-info-design.md is approved. Build it.
```

Bob écrit `agents/civic_info_agent.yaml`, demande l'approbation pour l'importer, l'importe, vérifie que l'Agent apparaît sur l'instance, envoie à l'Agent les questions de test de la conception et rend compte des réponses. Ensuite, l'Agent existe en Draft sur votre instance ; le chapitre 4 reprend chaque étape, avec le résultat complet.

### Changer de mode

Pour changer de mode :

- La liste déroulante des modes en bas de la zone de saisie, ou les commandes `/ask`, `/plan` et `/agent` tapées dans la conversation.
- Le raccourci `⌘ .` sur Mac ou `Ctrl .` sous Windows et Linux.
- Accepter un changement que Bob propose lorsqu'une demande exige un autre mode.
- Un changement que Bob effectue lui-même pendant une tâche, ce qui ne se produit sans demande que si Mode est activé sous le bouton Permissions.

| Mode | Sert à | Bob peut | Résultat |
|---|---|---|---|
| Ask | Comprendre la demande | Lire des fichiers, interroger l'instance, rechercher dans la documentation | Une reformulation de la demande, les questions ouvertes, un inventaire de l'instance |
| Plan | Écrire la conception | Tout ce qui précède, et écrire des fichiers | Un document de conception, en attente de votre approbation |
| Agent | Construire et tester | Tout | Les artefacts en Draft sur l'instance, une transcription des tests, un compte rendu |

## 3.2 Ce que vous approuvez, et quand

Vous approuvez deux fois dans chaque projet d'Agent : la conception, avant que Bob ne la construise, et le déploiement, avant qu'un Agent n'atteigne ses utilisateurs.

L'approbation de la conception a lieu entre le mode Plan et le mode Agent. Vous approuvez une liste : quels Agents existent et à quoi sert chacun, quels Outils a chaque Agent, quels systèmes externes ont besoin d'une Connexion, quels documents deviennent des connaissances, et l'ordre de construction. Si la liste n'est pas claire, renvoyez-la à Bob avec vos questions. Lorsque la conception est correcte, l'approbation tient en une ligne. Le mode Agent commence dans une nouvelle conversation, donc au chapitre 4 cette ligne, avec le fichier de conception désigné, constitue le prompt complet.

L'approbation du déploiement a lieu lorsque l'Agent est construit et testé. Chaque Agent que Bob importe est enregistré dans l'environnement Draft de l'instance ; les Outils et les Bases de connaissances appartiennent à l'instance et servent les deux environnements. Un Agent n'atteint ses utilisateurs que lorsqu'il est déployé ; le déploiement se fait avec une commande de l'ADK que Bob n'exécute jamais de sa propre initiative. Le chapitre 4 l'effectue une fois, avec une seule instruction, et les chapitres 5 à 9 la répètent. Si vous avez construit l'Agent dans la Developer Edition et le déployez sur un tenant SaaS, l'environnement actif doit être basculé sur le tenant avant le déploiement. Ce changement concerne Bob et tout autre assistant de codage de la machine.

Au chapitre 4, Bob écrit la conception de l'Agent d'information de la ville et attend votre approbation. Vous lisez le fichier et remarquez qu'il ne dit rien de ce que voit un habitant avant de taper une question. Vous écrivez, dans la même conversation en mode Plan :

```
Add a welcome message and two starter prompts to the design: the street light
question and the building permit question.
```

Bob révise le fichier et attend de nouveau. Lorsque la conception est complète, vous ouvrez une nouvelle conversation en mode Agent et écrivez :

```
The design in @design/civic-info-design.md is approved. Build it.
```

Bob construit et teste l'Agent, et l'Agent existe en Draft. Pour l'approbation du déploiement, à la fin des chapitres 4 à 9, vous demandez à Bob de déployer l'Agent ; Bob affiche la commande de déploiement et demande confirmation avant de l'exécuter. Tant que vous n'avez pas confirmé, l'Agent est en Draft, où seuls les créateurs de l'instance peuvent le joindre.

IMPORTANT : déployer, changer d'environnement, définir un identifiant et supprimer un artefact ne font pas partie des opérations pré-approuvées au chapitre 2, donc Bob demande une approbation avant chacune d'elles. Si Bob réalise l'une de ces actions sans demander, les réglages d'approbation diffèrent de ceux du chapitre 2. Reprenez la liste de contrôle de la section 2.7.

Entre ces deux approbations, Bob demande une approbation pour chaque fichier qu'il écrit et chaque commande qu'il exécute, comme l'a configuré le chapitre 2 ; approuvez chaque demande au fur et à mesure, et lisez le fichier que Bob propose d'importer. Après chaque importation, demandez à Bob de lister les artefacts de l'instance et vérifiez que le nouveau apparaît ; lors des tests, demandez le raisonnement et lisez-le.

## 3.3 Les types de prompts

Un prompt est le texte que vous tapez dans la conversation. Ce guide distingue trois types selon ce qu'ils demandent à Bob : une question demande une information, une instruction demande une action, et un prompt structuré décrit une tâche en plusieurs parties et indique comment vérifier le résultat. Ces noms sont propres à ce guide ; Bob ne les connaît pas.

Pour chaque prompt :

- Soyez précis, car Bob comble tout vide avec ses propres hypothèses.
- Montrez un exemple du résultat lorsque son format compte.
- Désignez les fichiers par des mentions @ au lieu de coller leur contenu.
- Planifiez avant de construire.

### Type 1 : la question

Une question demande une information à Bob, par exemple :

```
Which tools does civic_info_agent have, and what does each one do?
```

```
Why did civic_info_agent answer that permit PP-2026-0412 was unknown in the last test?
```

Utilisez une question pour comprendre le projet ou l'instance, pour savoir pourquoi quelque chose s'est produit, ou pour vérifier ce que Bob a compris avant de lui confier un travail. Les questions relèvent du mode Ask, où Bob ne peut rien modifier.

Nommez le fichier ou le test que Bob doit examiner ; sinon, Bob risque de répondre à partir de ses connaissances générales.

### Type 2 : l'instruction

Une instruction demande à Bob de réaliser une action, en une simple phrase à l'impératif.

Pour réaliser une action sur le projet ou l'instance :

```
Import agents/civic_info_agent.yaml into my instance.
```

```
Send the test questions from design/civic-info-design.md to civic_info_agent,
with reasoning, and show the answers next to the expected ones.
```

Pour demander un fichier, en listant ce que le fichier doit contenir :

```
Write the definition file for an agent named permits_agent that answers
questions about the status of building permit applications, with no tools yet.
Return only the file.
```

Pour corriger la réponse précédente de Bob, dans une conversation déjà en cours :

```
Use permit PP-2026-0398 as the example instead.
```

```
You changed the agent's name; put it back.
```

Utilisez une instruction pour une action unique dont le résultat attendu découle de l'action elle-même : une importation, une série de tests, une exportation, un fichier, une modification de la dernière réponse. Les instructions qui modifient l'instance relèvent du mode Agent, où Bob demande une approbation avant l'opération. Lorsque vous demandez un fichier, ajoutez « Return only the file », pour que Bob renvoie le fichier sans explication.

Pour une action en plusieurs étapes, ou dont le résultat doit être vérifié d'une manière particulière, utilisez un prompt structuré. Après de nombreuses corrections dans une même conversation, Bob perd de vue les contraintes antérieures ; dans ce cas, ouvrez une nouvelle conversation avec un prompt complet et des références aux fichiers actuels.

### Type 3 : le prompt structuré

Un prompt structuré est divisé en parties, chacune répondant à une question que Bob devrait sinon deviner. Les modèles ci-dessous sont des listes de contrôle pour celui qui écrit : le même contenu peut être envoyé sous forme de lignes étiquetées ou de texte suivi.

Le premier usage consiste à décrire ce que vous voulez au début d'un projet d'Agent, en mode Ask. Une question que le modèle laisse sans réponse revient de Bob sous forme de question, ou est tranchée par une hypothèse que Bob ne signale pas.

```
Users:        who will talk to the agent, and in which language
Purpose:      what the agent does, in one sentence, plus three example questions
Reached from: the Orchestrate chat, a web page, a messaging channel, the phone
Draws on:     the facts, documents or systems it needs, and which exist already
Out of scope: what it must not do, and what must not be built yet
Done when:    the questions it must answer correctly, and what a correct answer contains
```

Une forme plus courte, avec un titre, une description, des exemples de prompts et la valeur métier, suffit pour ouvrir la conversation :

```
I would like to develop an AI agent with watsonx Orchestrate. Here is my use case:

Title: Permit status agent
Description: Answers residents' questions about the status of their building permit applications.
Example prompts:
  "Where is my permit application PP-2026-0412?"
  "How long does a permit review take?"
Value: fewer calls to the Permits and Planning desk about applications in progress

Please propose the agent, tools, knowledge base and connections first
and wait for my approval before making changes.
```

Le premier prompt du chapitre 4 ne répond qu'à deux ou trois des six questions, et Bob demande le reste.

Le second usage consiste à spécifier une tâche en mode Agent, lorsque la tâche crée ou modifie quelque chose sur l'instance et que la vérification est propre à la tâche. Le modèle est :

```
Goal:        what must exist when the task is done, in one sentence
Context:     the files, folders and data to use, by name, with @ mentions
Constraints: names to keep, the model to use, what not to change
Deliverable: what Bob must return: a file, an import, a chat transcript, a report
Verify:      how Bob proves that the task worked, in a way that you can repeat
Stop:        the condition under which Bob must ask you instead of continuing
```

Le prompt suivant, pour l'Outil de permis du chapitre 6, est écrit comme si aucune conception n'existait :

```
Goal: the permit status tool exists on the instance and civic_info_agent can call it.
Context: @tools/get_permit_status.py and @agents/civic_info_agent.yaml.
Constraints: import the tool from that file. Keep the name get_permit_status.
  Add one paragraph to the agent's instructions saying when to call it; change
  nothing else.
Deliverable: the tool imported, the agent re-imported, and one chat asking
  "Where is my permit application PP-2026-0412?" with reasoning included.
Verify: the list of tools shows get_permit_status with permit_number in its input
  schema, and the chat reasoning shows one call to it returning "under review".
Stop: if the import returns an error, show me the exact text and wait.
```

Verify et Stop sont recommandés pour tout prompt qui modifie l'instance. Omettez une partie lorsqu'une conception approuvée l'énonce déjà ; au chapitre 4, le prompt en mode Agent est une simple instruction pour cette raison.

## 3.4 Prompts faibles et meilleurs

Un meilleur prompt désigne les fichiers par des mentions @, nomme l'Agent et les données, et indique ce que Bob doit renvoyer et, lorsque la modification compte, comment la vérifier. Sans cela, Bob comble les vides avec ses propres choix.

| Situation | Faible | Meilleur | Pourquoi |
|---|---|---|---|
| Commencer un projet d'Agent (prompt structuré) | « Build me a citizen services agent for the City of Utopia that can track permits, answer questions about regulations and take problem reports. », tapé en mode Agent | Le prompt structuré avec les six questions : trois exemples de phrases d'utilisateurs, les fichiers de données et l'Outil existant désignés par @, et « Tell me what you understood, what you need to know from me, and what already exists on my instance », en mode Ask | Le prompt faible laisse Bob supposer les données, inventer des Outils et importer avant que vous n'ayez vu un nom |
| Lancer un test (instruction) | « Test the agent. » | « Send the test questions from design/civic-info-design.md to civic_info_agent, with reasoning, and show the answers next to the expected ones. » | « Test the agent » laisse Bob choisir les questions et la manière de rendre compte. Le meilleur prompt nomme les questions, l'Agent et la forme de la réponse |
| Ajouter un Outil (prompt structuré) | « Add the permit status tool to the agent. » | Le prompt en six parties présenté en 3.3 | Le prompt faible ne nomme ni fichier ni Agent, et ne donne aucune preuve de réussite. Bob pourrait créer l'Outil de zéro, le renommer, ou annoncer un succès dès que l'importation répond |
| Analyser un échec (question) | « The agent does not work, fix it. » | « Why did civic_info_agent answer that permit PP-2026-0412 was unknown in the last test? Look at the reasoning of that test and tell me which tool was called and what it returned. » | « Fix it » pousse Bob à modifier la première chose qu'il trouve. La question demande d'abord la cause, et c'est dans le raisonnement qu'il faut la chercher |
| Demander un fichier (instruction) | « Write me an agent definition for permit tracking. » | La demande de fichier présentée en 3.3, avec le nom, le rôle et les Outils de l'Agent, terminée par « Return only the file » | Le nom, le rôle et les Outils sont énoncés. Le prompt faible produit un fichier plausible avec un nom inventé |
| Corriger une réponse précédente (instruction) | « That's not right, try again. » | « The table is right but the answer is too long. Keep the table, remove the introduction, and keep the whole answer under 80 words. » | « Try again » ne donne rien à modifier à Bob, qui devine donc ce qui n'allait pas |

Prompts à éviter :

| Prompt | Pourquoi il échoue | Quoi écrire à la place |
|---|---|---|
| « Build me a citizen services agent » | Bob invente les utilisateurs, les faits, les Outils et les noms | Le prompt structuré avec les six questions, en mode Ask |
| « Give it tools, a knowledge base and a few collaborators » | Chaque composant est une cause possible de mauvaise réponse. Lorsqu'on en ajoute plusieurs à la fois, trouver la cause prend beaucoup plus de temps | Un composant par itération, comme le font les walkthroughs |
| « It does not work, fix it » | Bob devine ce qui ne va pas et le modifie | Demandez d'abord le raisonnement du test qui échoue |
| « Make it production ready » | Le prompt ne nomme aucune vérification que Bob puisse faire, et ce que Bob construit reste en Draft jusqu'à ce que vous le déployiez | Construisez et testez en Draft ; déployez lorsque les tests passent |

## 3.5 Ce que Bob lit dans le dossier de projet

Deux éléments du dossier de projet, tous deux écrits par l'extension watsonx Orchestrate ADK au chapitre 2, sont à la disposition de Bob dans chaque conversation : le fichier de réglages `.bob/mcp.json`, à partir duquel Bob démarre le serveur Orchestrate et le serveur de documentation et qui fixe le dossier dans lequel Bob peut travailler, et les skills Orchestrate dans `.bob/skills`, que Bob active lorsqu'une tâche correspond à leur description. Vous ne les modifiez pas à la main ; les deux cas où une entrée de `.bob/mcp.json` change, aux chapitres 2 et 8, sont pris en charge par Bob.

Bob ne lit pas automatiquement les autres fichiers du projet. Désignez un fichier par une mention @ lorsque Bob doit le lire, par exemple le fichier de conception dans un prompt en mode Agent.

Utilisez une conversation par tâche. Les modes Ask et Plan partagent une conversation, car la conception a besoin de vos réponses ; le mode Agent utilise une conversation distincte avec le fichier de conception désigné, car au fil d'un long échange Bob perd de vue des contraintes qu'il avait acceptées plus tôt.

## 3.6 Bob et Git

Git conserve un historique des fichiers que Bob écrit dans le dossier de projet, les conceptions et les définitions, une version par commit. C'est Bob qui exécute les commandes git : vous décrivez l'opération en une phrase, en mode Agent, et Bob affiche la commande qu'il s'apprête à exécuter et demande votre approbation. Si vous ne précisez pas de message de commit, Bob en écrit un à partir des fichiers modifiés.

Le dossier de projet est déjà un dépôt git, puisque c'est un clone du dépôt du guide. Vos commits restent sur votre machine : les lecteurs ne peuvent pas pousser vers le dépôt du guide. Pour conserver vos commits ailleurs, ajoutez un dépôt distant à vous et demandez à Bob d'y pousser.

Chaque demande ci-dessous est une simple instruction, et Bob demande une approbation avant chaque commande qu'il exécute.

| Vous voulez | Envoyez |
|---|---|
| Enregistrer votre travail | `Commit everything I changed with a short message saying what was built.` |
| Enregistrer seulement certains fichiers | `Commit the files in the design folder with the message "City information agent design v2".` |
| Voir ce qui a changé depuis le dernier enregistrement | `Show me which files changed since the last commit and summarise the changes.` |
| Voir l'historique | `List the last ten commits with their dates and messages.` |
| Récupérer la dernière version du guide | `Pull the latest version of the guide from origin. Do not rebase.` |
| Annuler les modifications non validées d'un fichier | `Restore agents/civic_info_agent.yaml to the version in the last commit.` |
| Voir une version antérieure d'un fichier | `Show me what agents/civic_info_agent.yaml looked like three commits ago.` |
| Travailler sur une modification sans toucher à la version principale | `Create a branch named roads-hours and switch to it.` |
| Réintégrer une branche terminée | `Switch to the main branch and merge roads-hours into it.` |

Si une récupération (pull) produit des conflits, Bob s'arrête et les signale. Les mises à jour du guide modifient les dossiers `guide` et `walkthroughs` et le README ; un conflit ne survient que si vous avez modifié un fichier à ces endroits dans votre clone. Gardez vos notes et votre travail dans d'autres dossiers.

Les fichiers propres à votre machine, l'environnement Python, le dossier de réglages de Bob et `.env`, sont ignorés par git et ne sont pas validés. La vue Source Control, décrite à la section 2.3, offre les mêmes opérations d'un clic.
