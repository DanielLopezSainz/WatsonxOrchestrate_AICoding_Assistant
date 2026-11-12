# Chapitre 8. Une recherche d'adresse depuis un serveur MCP : les Boîtes à outils Orchestrate

Niveau : intermédiaire. Durée : environ 75 minutes. Prérequis : chapitre 7 terminé, ou son Outil, sa Connexion et son Agent importés depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre.

## Vue d'ensemble

Vous envoyez un message à CivicPulse : « The rubbish was not collected today at 18 elm st, which days do they collect it? ». L'Agent du chapitre 7 a un Outil qui connaît les jours de collecte d'Elm Street, mais l'Outil ne trouve pas la rue, car « 18 elm st » n'est pas l'orthographe qu'utilise la ville. Un registre des adresses (Address Registry) résout ce problème : il reçoit une adresse telle que l'habitant la tape et renvoie le nom officiel de la rue, le numéro, le quartier et le code postal. Dans ce chapitre, Bob écrit cet Address Registry sous forme de serveur MCP, avec les dix rues du calendrier de collecte (Collection Calendar), et l'Agent l'utilise.

MCP, le Model Context Protocol, est une manière standard pour un programme d'offrir des outils à des agents d'IA. Vous l'utilisez depuis le chapitre 2 : Bob atteint votre instance par un serveur MCP et la documentation d'Orchestrate par un autre. Maintenant, Bob construit son propre serveur MCP, grâce à sa capacité intégrée de création de serveurs MCP, et s'y connecte pour essayer ses outils. Ensuite, watsonx Orchestrate importe une copie du serveur MCP sous forme de Boîte à outils Orchestrate, et l'Agent reçoit ses outils.

Sautez ce chapitre si vous avez déjà importé un serveur MCP dans watsonx Orchestrate avec Bob. Pour continuer avec le chapitre 9 sans le construire, envoyez à Bob ces instructions en mode Agent : `Import the MCP server in walkthroughs/ch08/toolkits/address_registry into my instance as a toolkit named address_registry, with all its tools, then import walkthroughs/ch08/agents/civic_info_agent.yaml.` Ce raccourci donne à l'instance la Boîte à outils et l'Agent ; la connexion de Bob lui-même au serveur MCP, que met en place 8.6, n'est pas nécessaire aux chapitres suivants.

## 8.1 Avant de commencer

- La mise en place du chapitre 2, complète.
- L'Agent `civic_info_agent` du chapitre 7 sur votre instance, en Draft, avec ses quatre Outils et la Connexion `utopia_311`. Si vous avez sauté le chapitre 7, importez-les comme le décrit la Vue d'ensemble de ce chapitre.
- Dans les réglages de Bob, onglet MCP, le réglage Enable MCP Server Creation activé. Il l'est par défaut ; lorsqu'il est désactivé, Bob n'a pas d'instructions pour en écrire un.
- Une nouvelle conversation dans Bob pour ce chapitre.

Vérifiez que l'Agent est là : en mode Ask, demandez `Which tools does civic_info_agent have?` et vérifiez les quatre noms, `get_permit_status`, `get_request_status`, `get_collection_days` et `report_issue`.

La liste vient de l'Agent en Draft. Le serveur Orchestrate de Bob ne lit et ne modifie que l'environnement Draft de l'instance active ; ce qui atteint Live, les déploiements et l'identifiant Live du chapitre 7, passe par les commandes de l'ADK qu'exécute Bob. L'Agent déployé en Live au chapitre 7 n'est pas touché avant la section 8.9.

## 8.2 Ce qu'est un serveur MCP, et ce qu'est une Boîte à outils Orchestrate

Un serveur MCP est un programme qui offre des outils au moyen d'un protocole standard. Tout client qui parle ce protocole peut lister les outils, lire leurs descriptions et les appeler.

Les éditeurs publient des serveurs MCP pour leurs produits, pour qu'un Agent puisse chercher dans un système de tickets ou interroger une base de données par l'intermédiaire du serveur. Les équipes écrivent des serveurs MCP pour leurs propres systèmes, et le même registre d'adresses ou le même catalogue de produits sert alors tous les Agents de l'entreprise. La documentation de l'ADK liste des serveurs MCP des deux sortes que watsonx Orchestrate peut importer.

Une Boîte à outils Orchestrate est un groupe d'Outils que vous importez ensemble comme un seul asset. Pour l'Address Registry, le groupe est le serveur MCP : lorsque watsonx Orchestrate l'importe, la Boîte à outils est créée et chaque outil du serveur MCP devient un Outil de la Boîte à outils. À l'importation, vous choisissez tous les outils du serveur MCP ou certains d'entre eux ; l'Agent voit chacun sous le nom de la Boîte à outils, `address_registry:lookup_address`, et l'utilise comme n'importe quel autre Outil, à partir de sa description et de ses paramètres.

**Où s'exécute le serveur MCP**

Un serveur MCP peut s'exécuter dans watsonx Orchestrate ou en dehors. À l'intérieur, la plateforme reçoit le code du serveur MCP à l'importation, un dossier avec le programme et le fichier qui liste ses dépendances, en Python ou en Node.js, et le démarre lorsqu'un Agent appelle l'un de ses outils. À l'extérieur, le serveur MCP s'exécute sur votre propre infrastructure ou sur celle d'un éditeur, et la plateforme l'atteint par HTTP. Ce guide appelle le premier une Boîte à outils locale et le second une Boîte à outils distante. Dans ce chapitre, Bob écrit un serveur MCP pour watsonx Orchestrate.

**Ce qui change par rapport à un Outil**

| | Outil Orchestrate (chapitre 6) | Boîte à outils Orchestrate (ce chapitre) |
|---|---|---|
| Ce que vous importez | Une fonction | Un serveur MCP avec tous ses outils |
| Qui d'autre peut l'utiliser | watsonx Orchestrate | N'importe quel client MCP, Bob compris |
| Nom dans l'Agent | `get_collection_days` | `address_registry:lookup_address` |
| Le mettre à jour | Importer de nouveau l'Outil | Supprimer la Boîte à outils, l'importer de nouveau, puis importer de nouveau les Agents qui l'utilisent et déployer ceux qui sont en Live |
| Identifiants | Une Connexion nommée à l'importation | Une Connexion nommée à l'importation, dont les valeurs atteignent le serveur MCP sous forme de variables d'environnement |

L'Address Registry de ce chapitre n'a besoin d'aucune clé, la dernière ligne ne s'y applique donc pas.

**Le serveur MCP de ce chapitre : l'Address Registry**

Le serveur MCP qu'écrit Bob est un petit programme Python avec deux outils. `lookup_address` reçoit une adresse telle que l'habitant la tape et renvoie le nom officiel de la rue, le numéro, le quartier et le code postal. `list_streets` reçoit un quartier et renvoie ses rues. Les données derrière les deux sont une liste des dix rues du Collection Calendar du chapitre 6, chacune avec son quartier et son code postal.

**Pourquoi c'est l'un des chapitres les plus importants de ce guide**

Vous et votre équipe écrirez des serveurs MCP pour atteindre une base de données, une API interne ou un catalogue de produits, et par eux vos Agents atteignent des systèmes à l'intérieur et à l'extérieur de l'entreprise. Chaque Agent que vous construirez après ce guide et qui atteint un système de l'entreprise passe par un serveur MCP, les pratiques de ce chapitre sont donc celles que vous utiliserez le plus.

## 8.3 Mode Ask : décrire l'Address Registry

Mode : Ask, dans une nouvelle conversation.

Dans les chapitres précédents, les prompts ne nommaient pas l'asset Orchestrate à créer ; Bob le choisissait à partir de votre prompt. Cette fois, le prompt demande un serveur MCP par son nom. Les composants ont été présentés, le prompt énonce donc ce dont vous avez besoin et Bob n'a pas à deviner. Il nomme aussi Python au lieu de laisser le langage au choix de Bob, pour deux raisons : Bob peut écrire le serveur MCP en TypeScript, ce qui introduit Node.js et ses propres dépendances dans le projet ; et Python est le langage des Outils du chapitre 6, celui que connaissent la plupart des lecteurs, avec moins de dépendances. Le prompt dit aussi où s'exécute le serveur MCP et demande à Bob de l'essayer avant l'importation, deux décisions sur lesquelles Bob poserait sinon des questions.

```
The city of Utopia needs an address registry that resolves any address a
resident types, such as "18 elm st" or "7 Harbour Ln", into the official
street name, the house number, the district and the postcode. The address
registry will be an MCP server, running inside watsonx Orchestrate as a local
toolkit. I want civic_info_agent to use it so that, when a resident gives an
address, the Agent finds the official street before it looks up collection
days or reports a road problem. The city has no address registry yet: build
the MCP server in Python, with the data for the ten streets of the collection
calendar, and connect to it from Bob to try its tools before importing it
into watsonx Orchestrate.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Points à vérifier dans la réponse de Bob :

- Bob a compris un serveur MCP en Python avec pour données les dix rues du Collection Calendar, s'exécutant dans watsonx Orchestrate comme Boîte à outils locale, appelé par l'Agent avant tout Outil qui prend une rue, et essayé depuis Bob avant l'importation.
- Bob trouve sur l'instance l'Agent avec ses quatre Outils et sa Base de connaissances, le Collection Calendar avec les dix rues, les deux serveurs de la configuration MCP de Bob, et aucune Boîte à outils.
- Bob pose entre deux et cinq questions. Attendez-vous à une question sur les quartiers et les codes postaux ; les autres peuvent porter sur ce que renvoie l'outil pour une adresse inconnue, jusqu'où doit aller la correspondance d'une adresse tapée, quelle bibliothèque Python utiliser, s'il faut l'installer dans l'environnement du projet ou dans un environnement à part, quoi tester depuis Bob, et si l'Agent doit rechercher toutes les adresses ou seulement les adresses informelles. Chacune est une décision qui vous revient. Le second prompt choisit chaque fois l'option la plus simple, pour que votre Address Registry et celui de tous les autres lecteurs donnent les mêmes réponses. Bob peut terminer en vous demandant de passer en mode Agent ; restez en mode Ask.

Envoyez le prompt ci-dessous en entier, toujours en mode Ask et dans la même conversation ; il couvre ce que Bob a demandé et les points qu'il n'a pas soulevés. Si Bob a posé une question qu'il ne couvre pas, ajoutez à la fin une ligne avec votre réponse.

```
These are my answers.

1. The address registry covers the ten streets of tools/collection_calendar.csv
and nothing else. It has four districts: North, with Elm Street (UT1 1AA);
Harbour, with Harbour Lane (UT2 2AA); Old Town, with Mill Road (UT3 3AA); and
West. Put the other seven streets of the calendar into these four districts,
two or three per district, with postcodes that continue the pattern (UT1 1AB,
UT2 2AB, UT4 4AA and so on). The house number is whatever the resident typed;
the address registry returns it as given and does not check it.

2. Normalise only: lowercase, remove punctuation, expand the abbreviations st,
rd, ln, ave, dr, cl. No fuzzy matching and no extra library for it.

3. The official mcp Python SDK, one file, started with "python server.py", with
a requirements.txt next to it.

4. From Bob, call the two tools only: lookup_address with "18 elm st" and
list_streets with "Old Town". The chain through the Agent is tested after the
import.

5. The Agent always calls lookup_address before any tool that takes a street,
and uses the official street name for the collection calendar and for problem
reports, keeping the house number in the description of a report. When the
address registry does not know the address, the Agent asks the resident to
check it and calls no other tool.

Two tools: lookup_address, which receives an address as typed and returns the
official street name, the house number if there is one, the district and the
postcode; and list_streets, which receives a district and returns its streets.
When an address matches no street, lookup_address says so and returns nothing
else. Name the toolkit and its folder address_registry, and attach both tools
to the agent, listed under tools as toolkit:tool. The facts, the Knowledge
Base, the four tools and the Connection stay as they are.
```

Bob confirme les réponses et expose la construction dans la conversation : le fichier du serveur MCP et ses données, son entrée dans la configuration MCP de Bob, les deux appels de test, les modifications de l'Agent et, dans certaines exécutions, l'importation dans watsonx Orchestrate. Bob peut commencer comme s'il allait écrire les fichiers, et s'arrêter parce que le mode Ask ne le permet pas. Ne passez pas en mode Agent : la conception s'écrit d'abord, en mode Plan.

## 8.4 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

Une conception de serveur MCP décrit souvent uniquement des fichiers : le programme, l'entrée de configuration de Bob, un script avec la commande d'importation. À partir d'une telle conception, Bob écrit les fichiers et s'arrête ; rien n'est installé, testé ni importé. Le prompt ci-dessous l'empêche en demandant les étapes de construction sous forme de liste numérotée à la fin de la conception. Il nomme aussi deux détails sur lesquels Bob a tendance à se tromper : le Python qui démarre le serveur MCP, et l'importation depuis le dossier du serveur MCP. La section 8.10 explique les deux.

```
Write the design for this change into design/address-registry-design.md. End
it with the build steps in order: write the MCP server and its requirements
file, install the requirements into the project's Python environment, register
the MCP server in your MCP configuration, started with the Python of the
project's environment, with absolute paths, and call its two tools through
that connection, import the toolkit into watsonx Orchestrate from its folder
with all its tools, import the agent, run the test scenarios through the chat
operation of the Orchestrate server.
```

Lisez la réponse de Bob. Parfois, dans ses premières lignes, Bob dit qu'il ne peut pas écrire de fichiers et vous demande de passer en mode Agent. Si vous obtenez cette réponse et avez vérifié que vous êtes bien en mode Plan, envoyez le prompt suivant : `You are in Plan mode and can write files. Write the design to design/address-registry-design.md.` Approuvez l'écriture ; Bob écrit alors le fichier et le résume.

Ouvrez `design/address-registry-design.md` et comparez-le à ce tableau :

| Contenu | Ce qu'il faut vérifier |
|---|---|
| Le serveur MCP | Son dossier dans le projet, `toolkits/address_registry`, en Python, avec les deux outils, leurs descriptions et paramètres, les données des dix rues, et un fichier requirements |
| La connexion de Bob lui-même au serveur | Le serveur MCP enregistré dans la configuration MCP de Bob, démarré avec le Python de l'environnement du projet, pour que Bob puisse appeler les outils avant l'importation |
| La Boîte à outils | Son nom, `address_registry` ; l'importation depuis le dossier du serveur MCP avec la commande qui démarre le serveur MCP ; les deux outils importés |
| La modification de l'Agent | Les deux outils listés sous `tools` précédés du nom de la Boîte à outils, `address_registry:lookup_address` et `address_registry:list_streets` ; les instructions disent de rechercher d'abord chaque adresse et quoi faire lorsque l'Address Registry ne la connaît pas ; tout le reste inchangé |
| Les étapes de construction | Une liste numérotée à la fin, dans l'ordre du prompt. Sans elle, la construction s'arrête une fois les fichiers écrits |

## 8.5 Approuver la conception

Mode : Plan, même conversation.

Comparez le résumé de Bob et le fichier de conception au tableau de 8.4. Si quelque chose manque ou est faux, demandez la modification dans la même conversation ; Bob révise le fichier et attend de nouveau. Lorsque vous êtes d'accord avec la conception, passez à 8.6 : son premier prompt est l'approbation.

## 8.6 Mode Agent : construire, essayer, importer, tester

Mode : Agent, dans une nouvelle conversation.

Ouvrez une nouvelle conversation et passez en mode Agent pour exécuter le prompt :

```
The design in @design/address-registry-design.md is approved. Build it.
```

Bob suit les étapes de construction de la conception :

1. Écrit le serveur MCP, `toolkits/address_registry/server.py` avec les dix rues à l'intérieur, et `requirements.txt`.
2. Installe la bibliothèque dans l'environnement du projet et vérifie que le programme s'importe. La bibliothèque a pu changer de version depuis l'écriture de la conception et renommer sa classe de serveur ; Bob lit l'erreur et modifie une ligne.
3. Enregistre le serveur MCP dans sa configuration MCP et teste `lookup_address` et `list_streets`. La conception dit de les appeler par cette connexion ; Bob peut au lieu de cela exécuter les deux fonctions en Python et rendre compte de leurs résultats, ce qui ne teste pas la connexion. Le registre apparaît dans l'onglet MCP de Bob à côté des deux serveurs MCP du chapitre 2, et le test de 8.8 oblige Bob à utiliser la connexion.
4. Importe une copie du serveur MCP dans watsonx Orchestrate sous forme de Boîte à outils `address_registry`, depuis le dossier et avec la commande qui la démarre. La conception peut contenir une forme incorrecte de la commande ; Bob la corrige à partir de l'aide de la commande. La plateforme peut répondre à la première tentative par « We are configuring your tool in the background » ; Bob attend une minute et réessaie, et la seconde tentative réussit.
5. Met à jour l'Agent et l'importe de nouveau, remplaçant l'Agent en Draft. Bob peut d'abord placer la Boîte à outils sur la ligne `toolkits` : l'importation réussit et l'Agent ignore les outils, ce que Bob voit dans son premier test ; il les liste alors sous `tools` comme `address_registry:lookup_address` et `address_registry:list_streets`, et importe de nouveau l'Agent.
6. Envoie trois questions de test à l'Agent et rend compte : une adresse avec une abréviation, un signalement de nid-de-poule avec un numéro, et une adresse que le registre ne connaît pas.

![L'onglet MCP de Bob avec le serveur address_registry à côté des deux serveurs Orchestrate, ses deux outils listés](images/ch08-mcp-tab-registry.png)

Approuvez chaque demande au fur et à mesure. Bob corrige les échecs de ce type pendant la construction et ne rend compte que des résultats ; pour voir ce qu'il a corrigé, demandez dans la même conversation : `List every problem you met during the build and how you solved it.`

## 8.7 Ce que Bob a construit

Ouvrez le dossier du serveur MCP dans le File Explorer, `toolkits/address_registry`. Il contient deux fichiers : `server.py`, le programme avec ses données, et `requirements.txt`, qui nomme la bibliothèque MCP qu'utilise le programme. La bibliothèque ne fait pas partie de ce qu'a installé le chapitre 2. Bob l'a installée dans l'environnement du projet pendant la construction, pour son propre test, et watsonx Orchestrate l'installe sur l'instance à partir de ce fichier lorsque la Boîte à outils est importée. Bob peut ajouter un README ou un fichier de test.

Le programme est plus long qu'un Outil du chapitre 6, et l'essentiel reprend la même idée : chaque outil est une fonction avec une description et des paramètres typés, et une ligne au-dessus l'enregistre auprès du serveur MCP, un objet de la classe de serveur de la bibliothèque, `MCPServer` dans la version 2 de la bibliothèque et `FastMCP` dans la version 1. À la fin du fichier, le serveur MCP démarre et attend un client. Lorsque watsonx Orchestrate appelle un outil, il démarre ce programme, envoie l'appel par son entrée standard, lit la réponse sur sa sortie standard (le transport stdio, qu'utilise chaque Boîte à outils locale), et l'arrête.

L'onglet MCP de Bob (chapitre 2, section 2.3) liste l'Address Registry comme serveur MCP, connecté, avec ses deux outils, à côté de `watsonx-orchestrate-adk` et `watsonx-orchestrate-adk-docs`. La configuration de Bob pour ce serveur se trouve dans `.bob/mcp.json`, que git ignore : elle pointe vers le dossier sur votre machine, et le Bob de chaque lecteur écrit la sienne. Si l'entrée apparaît déconnectée, en rouge, la cause habituelle est un chemin relatif : Bob démarre ses serveurs MCP depuis un répertoire à lui, où `venv/bin/python` n'existe pas. Envoyez, en mode Agent : `The address_registry server in your MCP tab is disconnected. Fix its entry in .bob/mcp.json with absolute paths for the Python interpreter and the program, and restart it.`

Dans `agents/civic_info_agent.yaml`, la liste `tools` contient, après les quatre Outils du chapitre 7, les deux outils de la Boîte à outils précédés de son nom : `address_registry:lookup_address` et `address_registry:list_streets`. La ligne `toolkits` reste vide. Les instructions ont une nouvelle section : rechercher chaque adresse que donne un habitant, utiliser le nom officiel de la rue pour les autres Outils, et demander à l'habitant de vérifier une adresse que l'Address Registry ne connaît pas.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 8.8 Essayez

Posez la question à l'Agent, par l'intermédiaire de Bob avec `Ask civic_info_agent:` devant, ou dans le panneau d'aperçu de l'Agent dans le générateur de watsonx Orchestrate (Build, Agents, `civic_info_agent`). Sur un tenant, n'utilisez pas encore la conversation de la page d'accueil : elle parle à l'Agent déployé en Live, qui est encore la version du chapitre 7 et répond qu'il n'a pas de dossier pour « 18 elm st ». La conversation montre la modification après 8.9. Sur la Developer Edition, la conversation affiche l'Agent en Draft et répond déjà correctement.

```
The rubbish was not collected today at 18 elm st, which days do they collect it?
```

L'Agent résout l'adresse en Elm Street, consulte les jours de collecte et répond avec les jours des quatre bacs et le contact de Waste and Recycling. Essayez ensuite ceci :

- L'Address Registry seul, par l'intermédiaire de Bob, dans une nouvelle conversation en mode Ask : `Call lookup_address with "7 harbour ln" on the address_registry MCP server and show me the result.` Harbour Lane, numéro 7, quartier Harbour, UT2 2AA. Puis `Now call list_streets with "Old Town" on the same server.` : Mill Road et les autres rues de ce quartier. Le mode Ask ne laisse à Bob aucun moyen d'exécuter lui-même le programme, les appels passent donc par sa connexion MCP, et Bob affiche le serveur et l'outil au-dessus de sa réponse. C'est Bob qui appelle le serveur MCP sur votre machine ; l'Agent appelle la copie sur l'instance.
- Une adresse avec une autre abréviation : « Report a pothole at 7 harbour ln. » Le signalement part vers le remplaçant du centre d'appels 311 du chapitre 7, avec la rue Harbour Lane et la description « Pothole outside house number 7 », et l'Agent donne un numéro de demande.
- Une question sur les quartiers : « Which streets are in the Old Town district? » Mill Road et les autres rues que votre registre y place.
- Une adresse que l'Address Registry ne connaît pas : « Which day is the grey bin collected at 3 Castle Street? » L'Agent dit qu'il ne connaît pas cette adresse et vous demande de la vérifier. Avec le raisonnement, les étapes montrent la recherche et aucun appel à `get_collection_days`.

Posez de nouveau la première question avec le raisonnement. Les étapes montrent deux appels d'outils dans l'ordre : `lookup_address` avec l'adresse telle que tapée, qui renvoie Elm Street, numéro 18, North et UT1 1AA, puis `get_collection_days` avec Elm Street. Dans le raisonnement, l'outil apparaît comme `lookup_address` ; le nom de la Boîte à outils ne fait partie que de la définition de l'Agent.

![Le raisonnement : lookup_address, puis get_collection_days avec la rue corrigée](images/ch08-reasoning-two-calls.png)

## 8.9 Déployer la modification en Live

Mode : Agent, même conversation.

L'Agent a changé en Draft et doit être de nouveau déployé en Live. Sur la Developer Edition, sautez cette section.

```
Deploy civic_info_agent from draft to live.
```

Lorsque Bob annonce le déploiement, allez dans la conversation watsonx Orchestrate et posez la question de la Vue d'ensemble : un habitant qui écrit « 18 elm st » obtient les jours de collecte d'Elm Street.

## 8.10 Conseils pour construire des Boîtes à outils Orchestrate avec Bob

Chaque serveur MCP que vous construisez avec Bob pour watsonx Orchestrate passe par les étapes de ce chapitre : une description, une conception, une construction, une importation et un test. Chaque pratique ci-dessous dit quoi mettre dans vos prompts ou quoi vérifier dans la conception, et ce qui se passe sans elle.

1. Dites à Bob dans le premier prompt que vous voulez un serveur MCP. Si le prompt décrit seulement ce que l'Agent doit faire, Bob propose le composant le plus simple qui le fait, généralement un Outil Python, et aucun serveur MCP n'est construit.
2. Dites à Bob quel langage utiliser, Python dans ce guide. La documentation de Bob indique qu'il écrit généralement les serveurs MCP en TypeScript, ce qui ajoute Node.js et ses dépendances au projet. Python est le langage des Outils et de l'environnement qu'a installé le chapitre 2.
3. Dites à Bob où s'exécute le serveur MCP. « Running inside watsonx Orchestrate as a local toolkit » suffit, car une Boîte à outils locale utilise toujours stdio. Sans cela, Bob pose des questions sur les transports et peut affirmer à tort qu'une instance cloud a besoin de HTTP.
4. Demandez à Bob de tester lui-même le serveur MCP avant de l'importer, et vérifiez qu'il l'a fait par sa connexion MCP plutôt qu'en exécutant les fonctions Python. Bob propose rarement ce test de lui-même. Après l'importation, un échec n'apparaît que lorsque l'Agent appelle l'outil.
5. Donnez les données dans le prompt et gardez une correspondance simple. Sinon, Bob invente les données. Chaque bibliothèque qu'importe le serveur MCP doit être réinstallée sur l'instance, limitez donc le nombre de bibliothèques.
6. Nommez les outils, dites ce que chacun renvoie, et dites ce qui se passe quand rien ne correspond. Si le prompt les omet, Bob propose un outil là où il en faut deux et choisit leurs noms. Dites aussi ce que fait l'Agent d'un résultat introuvable ; pour l'Address Registry, il interroge l'habitant et n'appelle aucun autre Outil.
7. Utilisez un seul nom pour la Boîte à outils et son dossier, avec des tirets bas. Sinon, Bob peut écrire un dossier avec un trait d'union et donner un autre nom à la Boîte à outils, et l'Agent, la commande d'importation et vos notes ne concordent plus.
8. Dites à Bob que les outils vont dans la liste `tools` de l'Agent précédés du nom de la Boîte à outils, sous la forme `toolkit:tool`. Si Bob nomme plutôt la Boîte à outils sur la ligne `toolkits`, l'Agent s'importe sans erreur et ignore les outils ; seul un test le révèle.
9. Demandez à Bob de terminer la conception par les étapes de construction. Sans elles, « Build it » signifie « écris les fichiers » : Bob les écrit, vérifie leur syntaxe et s'arrête, sans rien installer, tester ni importer.
10. Demandez à Bob de démarrer le serveur MCP avec le Python de l'environnement du projet et avec des chemins absolus dans son entrée de `.bob/mcp.json`. Un simple `python` n'est généralement pas l'environnement où la bibliothèque est installée, et un chemin relatif n'est pas trouvé, car Bob démarre ses serveurs depuis un répertoire à lui. Dans les deux cas, l'entrée apparaît en rouge dans l'onglet MCP.
11. Pour une Boîte à outils locale, demandez à Bob de l'importer depuis son dossier, avec tous ses outils. La commande de l'ADK est `orchestrate toolkits add --kind mcp --name <name> --description "<text>" --package-root <folder> --command "python server.py" --tools "*"`. Sans le dossier, la plateforme ne reçoit aucun code, et le premier appel à un outil échoue.
12. Respectez les trois modes. Bob demande à passer en mode Agent après le premier prompt, après le second, et parfois au lieu d'écrire la conception en mode Plan. Répondez aux questions en mode Ask, écrivez la conception en mode Plan, et construisez dans une nouvelle conversation en mode Agent. Si Bob affiche la conception dans la conversation au lieu de l'écrire, dites-lui qu'il est en mode Plan et peut écrire le fichier.
13. En cas de doute, vérifiez ce que Bob dit de la plateforme dans la documentation de l'ADK. Bob peut énoncer une affirmation erronée avec une parfaite assurance. Bob peut lui-même interroger le serveur de documentation de la section 2.4 ; demandez-lui de confirmer une affirmation avant de construire dessus.
14. Précisez la version de la bibliothèque MCP dans `requirements.txt`, par exemple `mcp==2.3.0`. Une plage comme `mcp>=1.0.0` installe la version courante, quelle qu'elle soit, et une nouvelle version majeure peut renommer les classes qu'utilise le serveur. L'instance installe la bibliothèque à partir du même fichier, nommez donc la version que Bob a testée.
15. Dites à Bob comment tester l'Agent : dans les étapes de construction de la conception, avec les mots « run the test scenarios through the chat operation of the Orchestrate server », comme le fait le prompt de 8.4 ; pour un test à vous, avec `Ask civic_info_agent:` devant la question. Cette opération envoie un message à l'Agent en Draft et renvoie sa réponse, comme si vous parliez directement à l'Agent Orchestrate.
16. Demandez que les tests soient exécutés. Bob a terminé chaque conception de ce guide par une série de scénarios de test de sa propre initiative ; la phrase « run the test scenarios through the chat operation of the Orchestrate server » dans les étapes de construction lui fait les exécuter à la fin de la construction et rendre compte du résultat de chacun. Si une conception n'a pas de scénarios, demandez-les avant de l'approuver. Sans cette exécution, Bob annonce la construction comme terminée alors que l'Agent n'a répondu à aucune question.

## 8.11 Résumé

Vous avez construit un serveur MCP avec Bob, l'avez essayé depuis Bob, l'avez importé dans watsonx Orchestrate sous forme de Boîte à outils et avez donné ses outils à un Agent. Les mêmes étapes s'appliquent à chaque système que vos Agents atteindront par un serveur MCP : une base de données, une API interne, le produit d'un éditeur. Avant de construire le suivant, relisez la section 8.10.

- Un serveur MCP est un programme qui offre des outils au moyen d'un protocole standard à n'importe quel client, Bob et watsonx Orchestrate compris.
- Une Boîte à outils Orchestrate regroupe plusieurs outils en un seul asset ; le type MCP est un serveur MCP enregistré sur l'instance. L'Agent voit chaque outil sous la forme `toolkit:tool` et l'utilise comme n'importe quel autre Outil.
- Une Boîte à outils locale est un dossier que la plateforme exécute ; une Boîte à outils distante est un serveur MCP atteint par HTTP. Une Boîte à outils se met à jour en la supprimant et en l'important de nouveau ; les Agents qui l'utilisent sont alors importés de nouveau, et de nouveau déployés là où ils sont en Live.
- Bob crée lui-même des serveurs MCP, et les utilise comme client avant la plateforme.
