# Chapitre 9. Un Agent par service : les Agents collaborateurs

Niveau : intermédiaire. Durée : environ 60 minutes. Prérequis : chapitre 8 terminé, ou sa Boîte à outils et son Agent importés depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre.

## Vue d'ensemble

En rentrant chez vous en voiture, vous heurtez un nid-de-poule sur Harbour Lane. Le soir, vous ouvrez CivicPulse pour le signaler, et vous posez en même temps une question sur les bacs : « There is a pothole at 7 harbour ln, and which day is the green bin collected there? » L'Agent sur lequel nous travaillons peut répondre à toutes nos questions, car il contient des instructions qui couvrent tout : contacts, réglementation, quatre Outils, adresses. C'est justement le problème. Chaque question passe par une page de règles, et une modification pour un service peut casser les réponses des autres.

La ville d'Utopia a résolu ce problème il y a longtemps avec son centre d'appels 311 : les habitants appellent un seul numéro, et le centre d'appels transmet chaque appel au service concerné. Un Agent d'accueil parle aux habitants, et un Agent par service se tient derrière lui avec ses propres Outils et documents. L'Agent d'accueil garde le nom `civic_info_agent`, les habitants gardent donc le même point d'entrée.

Un Agent collaborateur est un Agent Orchestrate auquel un autre Agent transmet des questions.

Sautez ce chapitre si vous avez déjà construit avec Bob un Agent doté d'Agents collaborateurs. Pour continuer avec le chapitre 10 sans le construire, envoyez à Bob ces instructions en mode Agent : `Import the four agents in walkthroughs/ch09/agents into my instance, the three department agents first and civic_info_agent last.`

## 9.1 Avant de commencer

- La mise en place du chapitre 2, complète, avec votre environnement actif dans l'Environment Manager et le serveur Orchestrate connecté dans l'onglet MCP de Bob. Un environnement activé dure deux heures (section 2.4), et un serveur qui apparaît déconnecté se redémarre depuis l'onglet (section 2.8). Si l'environnement a expiré ou que le serveur est déconnecté, Bob ne peut pas atteindre l'instance et répond à partir des fichiers du projet.
- L'Agent `civic_info_agent` du chapitre 8 sur votre instance, en Draft, avec ses quatre Outils, les deux outils de la Boîte à outils `address_registry`, la Base de connaissances `city_regulations` et la Connexion `utopia_311`. Si vous avez sauté le chapitre 8, importez-les comme le décrit la Vue d'ensemble de ce chapitre.
- Une nouvelle conversation dans Bob pour ce chapitre.

Vérifiez que l'Agent est là : en mode Ask, demandez `Which tools does civic_info_agent have?` et vérifiez les six noms : `get_permit_status`, `get_request_status`, `get_collection_days`, `report_issue`, `address_registry:lookup_address` et `address_registry:list_streets`.

## 9.2 Ce qu'est un Agent collaborateur

Un Agent collaborateur est un Agent Orchestrate ordinaire qui travaille pour un autre Agent. L'Agent d'accueil contient une liste de ses Agents collaborateurs. Lorsqu'arrive une question à laquelle l'Agent d'accueil ne répond pas lui-même, il la transmet à l'Agent collaborateur concerné et rend la réponse à l'habitant. L'Agent collaborateur utilise ses propres Outils, documents et instructions, et l'habitant voit une seule conversation avec un seul Agent.

**Comment l'Agent d'accueil décide**

L'Agent d'accueil décide où envoyer chaque question à partir des descriptions de ses Agents collaborateurs. Le modèle lit ces descriptions à chaque question. Une question sur un nid-de-poule atteint `roads_agent` parce que sa description nomme les nids-de-poule, et une question envoyée au mauvais service se corrige en modifiant une description.

**Ce qui change par rapport à un seul Agent**

| | Un seul Agent (chapitres 4 à 8) | Accueil et services (ce chapitre) |
|---|---|---|
| Instructions | Tout sur la ville dans un seul texte | L'Agent d'accueil : accueil, contacts généraux, orientation, refus. Chaque service : son propre travail uniquement |
| Outils | Les six sur l'unique Agent | Chaque Outil sur l'Agent de son service |
| Base de connaissances | Un seul Agent y cherche | Les trois Agents qui y ont un document y cherchent ; les instructions de chacun nomment son document |
| Une modification pour un service | Modifie l'unique Agent qui sert les trois | Modifie un Agent de service ; les autres ne sont pas touchés |
| Raisonnement | Les appels d'Outils | L'appel à l'Agent collaborateur, puis ses appels d'Outils à l'intérieur |
| Déploiement | Un seul Agent | Chaque Agent est déployé séparément |

IMPORTANT : chaque Agent peut utiliser un modèle différent ; ce guide garde le modèle par défaut pour les quatre.

**La nouvelle équipe d'Agents**

- `civic_info_agent`, l'Agent d'accueil : le point d'entrée de CivicPulse, l'Agent auquel parlent les habitants. Toute question à laquelle il ne répond pas lui-même est transmise à l'Agent du service concerné, ou à deux lorsqu'une question en concerne deux.
- `permits_agent` : les permis de construire, les règles du Building Permit Guide et l'état d'une demande.
- `roads_agent` : les nouveaux signalements de problèmes de voirie, l'état d'un signalement existant, et le numéro pour les dangers urgents.
- `waste_agent` : les bacs et le recyclage, y compris les jours de collecte d'une rue et les Waste Sorting Rules.

IMPORTANT : ce chapitre n'écrit aucun code. Les Outils, la Boîte à outils, la Base de connaissances et la Connexion ne sont pas touchés ; les fichiers qui changent sont des définitions d'Agents, plus la conception et vos scripts d'importation. Vous pouvez diviser un Agent en plusieurs, ou les fusionner de nouveau, en modifiant ces définitions et en les important de nouveau.

## 9.3 Mode Ask : décrire l'équipe

Mode : Ask, dans une nouvelle conversation.

Le prompt demande à Bob de créer les Agents collaborateurs et décrit ce que font l'Agent d'accueil et chacun des trois services. Bob écrit les descriptions et les instructions des quatre Agents.

```
I want to split civic_info_agent into a front desk agent and three department
agents, Permits and Planning, Roads and Infrastructure, and Waste and
Recycling. The department agents are collaborators of the front desk. The front
desk keeps the name civic_info_agent, its welcome message and its starter
prompts; it answers general questions about the departments, their contacts
and hours, and questions about the noise ordinance, and passes every other
question to the department that owns it. Each department agent gets the tools
of its department, the facts of its department, and the documents of the
knowledge base that concern it. Nothing else changes: the tools, the toolkit,
the knowledge base and the connection stay as they are.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Points à vérifier dans la réponse de Bob :

- Bob a compris quatre Agents : l'Agent d'accueil avec trois Agents collaborateurs, et les Outils et documents répartis par service. Bob peut proposer sa propre répartition, par exemple l'Address Registry conservé aussi sur l'Agent d'accueil ; le second prompt la fixe.
- Bob trouve sur l'instance l'Agent avec ses six outils, la Base de connaissances, la Boîte à outils et la Connexion, et aucun autre Agent du projet. Des différences entre vos fichiers et l'instance peuvent aussi apparaître, comme le nom du style de l'Agent, que la plateforme rapporte sous un nom qui lui est propre. Le second prompt les règle.
- Bob pose des questions sur les noms des Agents de service, quel Outil va où, si la Base de connaissances est rattachée en entier ou divisée, ce que fait l'Agent d'accueil d'une question qui concerne deux services, quelles règles des chapitres précédents sont conservées, si les Agents de service sont cachés aux habitants, et le modèle. La dernière ligne du prompt suivant répond à deux autres questions que Bob peut poser : s'il faut mettre à jour vos scripts d'importation et s'il faut écrire une conception. Si Bob termine en vous demandant de passer en mode Agent, restez en mode Ask.

Envoyez le prompt ci-dessous en entier, toujours en mode Ask et dans la même conversation ; il couvre ce que Bob a demandé et les points qu'il n'a pas soulevés. Sa dernière ligne concerne un projet qui a des scripts d'importation, comme le vôtre si vous avez construit les chapitres précédents ; omettez-la sinon. Si Bob a posé une question qu'il ne couvre pas, ajoutez à la fin une ligne avec votre réponse.

```
These are my answers.

1. The department agents are permits_agent, roads_agent and waste_agent, with
the display names Permits and Planning, Roads and Infrastructure, and Waste and
Recycling.

2. permits_agent gets get_permit_status and the building permit guide.
roads_agent gets get_request_status, report_issue and
address_registry:lookup_address. waste_agent gets get_collection_days,
address_registry:lookup_address, address_registry:list_streets and the waste
sorting rules. civic_info_agent keeps no tool and keeps the noise ordinance.
The knowledge base city_regulations is attached to civic_info_agent,
permits_agent and waste_agent, and the instructions of each say which document
is theirs; roads_agent has no document and gets no knowledge base.

3. The description of each department agent is written for the front desk: it
says what the department answers and when to call it. The front desk calls one
department for a question about that department, and both departments for a
question that concerns two, and passes their answers on as they are. Residents
talk to the front desk only; the department agents stay visible in the chat
for now.

4. Every agent keeps the rules of the earlier chapters: the contact details at
the end of each answer, the exact wording of the not-found replies, the address
lookup before any tool that takes a street, and the refusal of questions
outside the three departments, which stays with the front desk and names the
office that might help without inventing any contact detail. A document is
named only for an answer taken from the knowledge base. The front desk also
keeps the number for urgent hazards, so that nobody waits for a handover.

5. All four agents use the same model and style as in
agents/civic_info_agent.yaml.

Update the import and delete scripts as well; the design and the tests come in
the next step.
```

Bob confirme les réponses et liste les quatre Agents dans la conversation : les Outils et les documents de chacun, les descriptions, l'ordre de construction, les modifications de vos scripts. Il peut aussi lister des limites qu'il ne peut pas garantir, comme la transmission mot pour mot de la réponse d'un service, qui dépend du modèle. Si Bob revient avec deux ou trois détails, répondez à chacun en une ligne. Parfois Bob commence comme s'il allait écrire les fichiers, et s'arrête parce que le mode Ask ne le permet pas. Ne passez pas en mode Agent : la conception s'écrit d'abord, en mode Plan.

## 9.4 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

Un Agent collaborateur doit être sur l'instance avant l'Agent qui le nomme, les trois services passent donc en premier et l'Agent d'accueil en dernier. Le prompt demande les étapes de construction dans cet ordre.

```
Write the design for this change into design/collaborators-design.md. End it
with the build steps in order: write the four agent definitions, import the
three department agents, import civic_info_agent, run the test scenarios
through the chat operation of the Orchestrate server.
```

Lisez la réponse de Bob. Parfois, dans ses premières lignes, Bob dit qu'il ne peut pas écrire de fichiers et vous demande de passer en mode Agent. Si vous obtenez cette réponse et avez vérifié que vous êtes bien en mode Plan, envoyez `You are in Plan mode and can write files. Write the design to design/collaborators-design.md.` et approuvez l'écriture ; Bob écrit alors le fichier et le résume.

Ouvrez `design/collaborators-design.md` et comparez-le à ce tableau :

| Contenu | Ce qu'il faut vérifier |
|---|---|
| Les quatre Agents | Leurs noms ; pour chacun, ses Outils, ses documents, ses faits, selon la répartition de 9.3 |
| Les descriptions | Une par Agent de service, qui dit ce qu'il traite et quand l'Agent d'accueil l'appelle ; la description de l'Agent d'accueil pour les habitants |
| L'Agent d'accueil | La liste `collaborators` avec les trois noms ; aucun Outil ; le message de bienvenue et les suggestions de questions conservés |
| Les instructions | L'Agent d'accueil : orientation, Noise Ordinance, refus ; chaque service : son propre travail, avec les règles des chapitres précédents |
| Les étapes de construction | Une liste numérotée à la fin : les quatre définitions, les trois services importés, puis l'Agent d'accueil, puis les scénarios de test |

## 9.5 Approuver la conception

Mode : Plan, même conversation.

Comparez le résumé de Bob et le fichier de conception au tableau de 9.4. Si quelque chose manque ou est faux, demandez la modification dans la même conversation ; Bob révise le fichier et attend de nouveau. Lorsque vous êtes d'accord avec la conception, passez à 9.6 : son premier prompt est l'approbation.

## 9.6 Mode Agent : construire et tester

Mode : Agent, dans une nouvelle conversation.

Ouvrez une nouvelle conversation et passez en mode Agent pour exécuter le prompt. Il nomme la dernière étape de la conception, les tests, car un prompt de construction qui dit seulement « build » a tendance à s'arrêter à la dernière importation :

```
The design in @design/collaborators-design.md is approved. Build it and run its test scenarios.
```

Bob suit les étapes de construction de la conception :

1. Écrit les quatre définitions dans le dossier `agents`, trois nouveaux fichiers et une nouvelle version de `agents/civic_info_agent.yaml`, et met à jour les scripts d'importation et de suppression, si votre projet en a.
2. Importe `permits_agent`, `roads_agent` et `waste_agent`. Un Agent qui nomme un Agent collaborateur pas encore présent sur l'instance est refusé à l'importation ; l'ordre de la conception l'évite.
3. Importe `civic_info_agent`, remplaçant l'Agent en Draft. Ses six outils sont maintenant sur les services.
4. Envoie les questions de test à `civic_info_agent` et rend compte des réponses.

IMPORTANT : regardez l'étape 4. Bob ne se contente pas de construire les Agents ; il les teste. Chaque conception que Bob a écrite dans ce guide se termine par une série de scénarios de test (ouvrez-la et lisez-les : une question, le service qu'elle doit atteindre, la réponse attendue), et la dernière étape de construction du prompt de conception, « run the test scenarios through the chat operation of the Orchestrate server », fait exécuter à Bob ces scénarios un par un à la fin de la construction et rendre compte du résultat de chacun. Conservez les deux dans chaque conception que vous écrirez désormais : les scénarios, que vous demandez si une conception n'en a pas, et l'étape de construction qui les exécute. Bob construit l'Agent et exécute les tests qui confirment qu'il fonctionne.

Approuvez chaque demande au fur et à mesure. Bob corrige les échecs pendant la construction et ne rend compte que des résultats ; pour voir ce qu'il a corrigé, demandez dans la même conversation : `List every problem you met during the build and how you solved it.`

## 9.7 Ce que Bob a construit

Ouvrez `agents/permits_agent.yaml` dans le File Explorer. C'est une définition comme celle du chapitre 4, mais plus courte. Sa `description` dit ce que traite le service et quand l'appeler. `tools` contient un nom et `knowledge_base` contient `city_regulations`. Les instructions ne couvrent que Permits and Planning : ses faits, la règle pour le Building Permit Guide et la règle pour `get_permit_status`. `agents/roads_agent.yaml` et `agents/waste_agent.yaml` ont la même forme avec leurs propres Outils ; `waste_agent` a les Waste Sorting Rules et `roads_agent` n'a pas de document.

Les trois services sont listés dans la conversation à côté de l'Agent d'accueil. Ouvrez-en un et posez-lui une question hors de son sujet. Il répond sur son propre sujet et refuse le reste. Il n'a pas de message de bienvenue, car il est fait pour servir un autre Agent. Les services restent visibles dans ce guide pour que vous puissiez les ouvrir et les tester ainsi. Dans un déploiement en production, envisagez le champ `hidden: true` au premier niveau de la définition de chaque service. La conversation ne liste alors que l'Agent d'accueil, et les habitants ne peuvent pas le contourner.

![La page Manage Agents avec l'Agent d'accueil et les trois Agents de service](images/ch09-four-agents.png)

Ouvrez `agents/civic_info_agent.yaml`. Sa liste `tools` est vide. Les trois noms sont dans `collaborators`, et `knowledge_base` conserve `city_regulations`. Les instructions sont bien plus courtes qu'au chapitre 8 : l'accueil, les contacts et horaires généraux, la règle pour la Noise Ordinance, la règle d'orientation, et le refus des questions hors des trois services. Le message de bienvenue et les suggestions de questions sont inchangés.

L'onglet MCP de Bob n'a rien de nouveau et le dossier de projet ne contient que des fichiers d'Agents, car un Agent collaborateur est déclaré dans la définition de l'Agent qui l'appelle.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 9.8 Essayez

Posez la question à l'Agent, par l'intermédiaire de Bob avec `Ask civic_info_agent:` devant, ou dans le panneau d'aperçu de l'Agent dans le générateur de watsonx Orchestrate :

```
There is a pothole at 7 harbour ln, and which day is the green bin collected there?
```

La réponse comporte les deux parties : un numéro de demande pour le nid-de-poule et le jour du bac vert de Harbour Lane, avec les contacts des deux services. Essayez ensuite ceci :

- Une question pour un seul service : « Where is my permit application PP-2026-0412? » L'état, venant de `permits_agent`.
- L'Agent d'accueil répond lui-même à certaines questions : « What are the quiet hours? » La Noise Ordinance, citée dans la réponse, sans appel à un service.
- Une question hors des trois services : « When does the swimming pool open? » L'Agent d'accueil refuse et nomme un bureau qui pourrait aider. Il ne donne aucune coordonnée pour ce bureau, car il n'en a pas. Le point 4 du second prompt interdit les coordonnées inventées parce que, sans cette règle, le modèle peut en fournir.
- Mauvaise adresse : « Which day is the grey bin collected at 3 Castle Street? » L'Agent des déchets vous demande de vérifier l'adresse ; l'Agent d'accueil transmet.

Posez de nouveau la première question avec le raisonnement. Un Agent collaborateur apparaît comme un outil de l'Agent d'accueil, nommé d'après son nom d'affichage : `chat_with_collaborator_roads_and_infrastructure`, avec une réponse qui commence par « Transferring to » et nomme le service. Les étapes qui suivent portent le nom du service, Roads and Infrastructure, et sont les appels d'Outils du chapitre 8 : `lookup_address`, puis `report_issue`. Puis la même chose pour Waste and Recycling, avec `lookup_address` et `get_collection_days`. Chaque service reçoit sa partie de la question dans les mots de l'Agent d'accueil, et la réponse présente les deux parties l'une après l'autre, chacune avec le contact de son service.

![Le raisonnement : Transferring to Roads and Infrastructure, puis les appels d'Outils du service](images/ch09-reasoning-transfer.png)

L'Agent des déchets peut attribuer le jour de collecte aux Waste Sorting Rules, un résultat d'Outil cité comme s'il venait du document. Ses instructions disent de nommer le document pour chaque réponse issue de la Base de connaissances, et il applique la règle trop largement.

Si l'Agent d'accueil envoie une question au mauvais service, regardez les descriptions des trois Agents collaborateurs. Dites à Bob quelle question est allée où, en une phrase, et demandez-lui de corriger la description, d'importer de nouveau l'Agent et de tester.

## 9.9 Déployer la modification en Live

Mode : Agent, même conversation.

Trois Agents ont été créés et un a changé en Draft, et chaque Agent est déployé séparément. Sur la Developer Edition, sautez cette section.

```
Deploy permits_agent, roads_agent, waste_agent and civic_info_agent from draft to live, in that order.
```

Une fois que Bob a annoncé les quatre déploiements, posez la question de la Vue d'ensemble dans la conversation watsonx Orchestrate, et vérifiez qu'une seule conversation renvoie un numéro de demande et un jour de collecte.

## 9.10 Résumé

Vous avez divisé un Agent en une équipe : un Agent d'accueil auquel parlent les habitants, et trois Agents de service auxquels il transmet les questions. Les réponses sont celles du chapitre 8 ; le raisonnement montre quel service a donné chacune. Lorsque les instructions d'un Agent ont dépassé un seul sujet, envisagez la même répartition : un Agent par sujet, et un devant.

- Un Agent collaborateur est un Agent Orchestrate nommé dans la liste `collaborators` d'un autre Agent. L'Agent appelant transmet la question et rend la réponse, si bien que l'habitant voit une seule conversation ; l'Agent collaborateur répond avec ses propres Outils et documents.
- L'Agent d'accueil oriente d'après les descriptions de ses Agents collaborateurs, la description d'un Agent de service est donc écrite pour l'Agent d'accueil : ce qu'il traite, et quand l'appeler.
- Un Agent collaborateur doit être sur l'instance avant que l'Agent qui le nomme ne soit importé, et chaque Agent est déployé séparément.
- Une modification pour un service modifie une seule définition d'Agent ; seules ses coordonnées figurent aussi dans les faits de l'Agent d'accueil.

L'équipe répond aux habitants dans la conversation de watsonx Orchestrate. Au chapitre 10, elle leur répond sur WhatsApp, par un Canal Orchestrate.
