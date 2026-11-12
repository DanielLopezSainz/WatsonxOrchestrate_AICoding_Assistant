# Chapitre 2. Connecter Bob à watsonx Orchestrate

Niveau : débutant. Durée : environ 30 minutes. Prérequis : IBM Bob installé, et une instance watsonx Orchestrate à laquelle vous pouvez vous connecter.

## Vue d'ensemble

Avant que Bob puisse créer quoi que ce soit dans watsonx Orchestrate, il doit être connecté à votre instance. IBM fournit pour Bob une extension qui installe l'ADK qu'utilise Bob, connecte Bob à l'instance et prépare le dossier de projet.

À la fin du chapitre :

- Le dépôt du guide est ouvert dans Bob comme dossier de projet.
- Bob est connecté à votre instance watsonx Orchestrate et peut lister ce qui y existe.
- Bob lit l'instance sans demander, et demande votre approbation avant d'écrire un fichier, d'exécuter une commande ou de modifier l'instance.

Sautez ce chapitre si chaque ligne de la liste de contrôle de la section 2.7 est déjà vraie pour le dossier que vous avez ouvert dans Bob.

## 2.1 Avant de commencer

| Il vous faut | D'où cela vient |
|---|---|
| IBM Bob 2.1 ou ultérieur | Installé et ouvert |
| Git | Installé sur votre machine ; Bob l'utilise pour cloner. Vous ne taperez aucune commande git |
| Une instance Orchestrate | Un tenant SaaS sur IBM Cloud ou AWS, ou la Developer Edition exécutée sur votre machine |
| Pour un tenant : son URL et une clé d'API | Dans l'interface d'Orchestrate : votre icône d'utilisateur, Settings, API details. La clé n'est affichée qu'une fois ; l'étape 1 de 2.2 indique où la conserver |

Ne collez pas la clé d'API dans une conversation avec Bob, et ne l'écrivez dans aucun autre fichier.

## 2.2 L'installation, étape par étape

Après chaque étape, une ligne « Vous devriez voir » décrit le résultat attendu ; ne continuez que lorsque vous le voyez.

Étape 1. Cloner le dépôt.

1. Dans Bob, cliquez sur l'icône des fichiers en haut à gauche. Si aucun dossier n'est ouvert, le panneau affiche deux boutons : Open Folder et Clone Repository.
2. Cliquez sur Clone Repository et collez `https://github.com/DanielLopezSainz/WatsonxOrchestrate_AICoding_Assistant.git`.
3. Choisissez où l'enregistrer. Bob y crée un dossier nommé `WatsonxOrchestrate_AICoding_Assistant`.
4. Lorsque Bob propose d'ouvrir le dépôt cloné, cliquez sur Open. Si la conversation de Bob est au premier plan, cliquez sur l'icône des fichiers pour voir les fichiers : `README.md`, le dossier `guide` avec les chapitres, le dossier `walkthroughs` et un fichier nommé `.env.example`.
5. Créez votre fichier `.env` à la racine du dossier de projet, à côté de `README.md`, là où se trouve `.env.example` : faites un clic droit sur `.env.example`, choisissez Copy, collez-le au même endroit et renommez la copie en `.env`. Ouvrez-le et renseignez l'URL et la clé d'API de votre tenant (sur la Developer Edition, laissez-le tel quel).

Vous devriez voir : le nom du dossier en haut du panneau, et `.env` listé à côté de `.env.example`.

Le fichier `.env` est l'endroit où ce guide conserve les valeurs qui doivent rester sur votre machine : l'URL et la clé du tenant maintenant, une valeur de plus au chapitre 7 et deux au chapitre 10. Git l'ignore, il n'est donc pas validé et n'atteint pas votre dépôt ; vous ne collez jamais son contenu dans une conversation avec Bob. À l'étape 5, vous tapez la clé une fois dans l'extension ; `.env` est l'endroit où vous la retrouvez quand l'extension la redemande plus tard.

Étape 2. Installer l'extension.

1. Ouvrez la vue Extensions : `Cmd Shift X` sur Mac, `Ctrl Shift X` ailleurs.
2. Recherchez `watsonx Orchestrate ADK`, éditeur watson-devex, et cliquez sur Install.

![L'extension watsonx Orchestrate ADK dans la vue Extensions, avec son bouton Install](images/ch02-extension-install.png)

Vous devriez voir : une icône watsonx Orchestrate dans la barre de gauche. Si la barre est pleine, l'icône se trouve sous les trois points en bas de celle-ci.

Étape 3. Initialiser l'espace de travail.

1. Cliquez sur l'icône watsonx Orchestrate. Un panneau intitulé « Watsonx Orchestrate: Explorer » s'ouvre avec le message « No workspace found. Please initialise a workspace to begin building » et un bouton, Initialise Workspace.
2. Si le panneau indique plutôt que l'extension s'est chargée en mode restreint, cliquez sur son lien pour faire confiance au dossier, confirmez, et rechargez la fenêtre quand c'est demandé. Bob le demande une fois par dossier.
3. Cliquez sur Initialise Workspace. Une boîte de dialogue demande « Initialize watsonx Orchestrate workspace in the current folder? » et affiche le chemin du dossier. Cliquez sur Continue with Current Folder.
4. Si Bob demande l'autorisation d'installer `uv`, acceptez. L'extension a besoin de `uv` pour créer l'environnement Python. Si `uv` ne peut pas être installé, par exemple sur une machine où les installations sont restreintes, l'extension affiche l'adresse des instructions d'installation manuelle ; installez `uv` et cliquez de nouveau sur Initialise Workspace.
5. Patientez. Un message de progression égrène les étapes ; l'extension installe un environnement Python et l'ADK dans le dossier, ce qui prend une à deux minutes.

Vous devriez voir : le panneau comporte maintenant deux sections. Explorer liste Agents, Tools, Connections, Knowledge Bases et Toolkits ; Environment Manager affiche une liste déroulante Environment et un bouton Add.

Étape 4. Envoyer à Bob son message de démarrage.

À la fin de l'initialisation, l'extension place un message dans la zone de saisie de la conversation de Bob, sans l'envoyer. Aucune notification n'est affichée, et le message passe donc facilement inaperçu.

1. Trouvez le texte intitulé « SYSTEM PROMPT - IBM watsonx Orchestrate » dans la zone de saisie.
2. Appuyez sur Entrée pour l'envoyer tel quel.

![Le message de démarrage placé dans la zone de saisie par l'extension, avant l'envoi](images/ch02-starting-message.png)

Le message demande à Bob de passer en mode Agent, de charger les skills Orchestrate, et d'utiliser le serveur Orchestrate pour toutes les opérations sur les Agents, les Outils et les environnements, et le serveur de documentation comme référence. Si la zone est vide, par exemple parce que le texte a été effacé ou qu'une nouvelle conversation a été ouverte avant son envoi, collez le texte suivant et envoyez-le :

```
# SYSTEM PROMPT - IBM watsonx Orchestrate
## Instructions
1. Switch to **Agent mode** if not already active.
2. Use the `fetch_all_skills` tool on the `watsonx-orchestrate-adk` MCP server to load available skills.
3. Use the fetched skills and `watsonx-orchestrate-adk` MCP for all agent, tool, and environment operations. Consult `watsonx-orchestrate-adk-docs` MCP for API reference and documentation guidance.
```

Vous devriez voir : Bob répondre que les skills sont chargés, avec un tableau des skills, et qu'il est en mode Agent. Si Bob demande d'abord l'approbation pour exécuter `fetch_all_skills`, approuvez ; l'étape 7 règle les approbations pour le reste du guide. Le nombre de skills dépend de la version de l'ADK ; la version 2.18 en fournit huit. Les skills sont enregistrés dans `.bob/skills` dans le dossier de projet, et Bob les lit dans chaque chapitre à partir du chapitre 4.

Étape 5. Se connecter à votre instance.

Votre instance est le service watsonx Orchestrate où s'exécutent vos Agents : un tenant SaaS sur IBM Cloud ou AWS, ou la Developer Edition exécutée sur votre machine. L'ADK appelle une connexion à une instance un environnement ; c'est un autre usage du mot que les environnements Draft et Live du chapitre 1, qui sont deux parties d'une même instance. La section Environment Manager du panneau affiche les environnements existants, et sa liste déroulante indique celui qui est actif ; Bob travaille sur l'environnement actif.

- Developer Edition exécutée sur votre machine : rien à faire. La liste déroulante affiche déjà `local (active)`, et en dessous « Local server: Started ».
- Tenant SaaS : la liste déroulante est vide sur une machine où l'ADK n'a jamais été utilisé. Cliquez sur Add et répondez tour à tour à quatre questions : un nom pour l'environnement, par exemple `mytenant` ; l'URL de l'instance vue en 2.1 ; le réglage SSL, où vous sélectionnez la première option, Verify SSL (Recommended) ; et votre clé d'API, tapée dans un champ masqué. Lorsqu'on vous demande s'il faut activer l'environnement maintenant, confirmez.

Vous devriez voir : dans Environment Manager, la liste déroulante affichant le nom de votre environnement suivi de « (active) ». Dans Explorer, dépliez Agents : la liste est lue sur l'instance, elle affiche donc les Agents qui y existent. Un tenant que personne n'a encore utilisé en a un, `AskOrchestrate`. La Developer Edition en a deux, affichés comme « Try Document Processing Agent (DocProcessing) » et « AskOrchestrate ».

![L'Environment Manager avec l'environnement saas actif](images/ch02-environment-manager-active.png)

Étape 6. Vérifier que Bob atteint les deux serveurs.

L'étape 3 a enregistré deux serveurs MCP : `watsonx-orchestrate-adk`, que Bob utilise pour agir sur votre instance, et `watsonx-orchestrate-adk-docs`, qu'il utilise pour rechercher dans la documentation d'Orchestrate.

1. Ouvrez les réglages de Bob avec l'icône des réglages dans le panneau de Bob, puis l'onglet MCP.
2. Trouvez les deux entrées `watsonx-orchestrate-adk` et `watsonx-orchestrate-adk-docs`.

Vous devriez voir : les deux marquées comme connectées, et une soixantaine d'opérations listées sous la première lorsque vous la dépliez.

Étape 7. Régler les approbations.

Par défaut, Bob demande une approbation avant chaque action. Avec les réglages suivants, Bob lit les fichiers et interroge l'instance sans demander, et demande toujours avant d'écrire un fichier, d'exécuter une commande ou de modifier l'instance. La section 2.5 explique les deux réglages.

1. Cliquez sur le bouton Permissions, à côté de la liste déroulante des modes en bas de la zone de saisie. Une liste de neuf catégories s'ouvre : Read, Edit, Execute, MCP, Skill, Todo, Subtask, Subagent, Mode. Activez Read et MCP. Laissez Edit et Execute désactivés. La même liste se trouve dans les réglages de Bob, sous Auto-Approve.
2. Ouvrez les réglages de Bob, onglet MCP, dépliez `watsonx-orchestrate-adk`, et activez Always allow pour ces opérations uniquement : `check_version`, `list_agents`, `list_tools`, `list_toolkits`, `list_knowledge_bases`, `list_connections`, `list_models`, `export_agent`, `export_tool`, `export_toolkit`, `chat_with_agent`.

Vous devriez voir : aucun changement pour l'instant. L'effet est visible à l'étape suivante, où Bob liste les Agents sans demander d'approbation.

Étape 8. Tester l'accès à l'instance. Ouvrez une nouvelle conversation, sélectionnez le mode Ask dans la liste déroulante des modes, et envoyez :

```
Which agents exist on my instance? List their names and one line each.
```

Vous devriez voir : Bob appeler le serveur Orchestrate, ce qui s'affiche au-dessus de sa réponse, et les mêmes Agents que ceux que liste l'Explorer. Si Bob demande d'abord une approbation, les réglages de l'étape 7 ne sont pas en place. Si la réponse mentionne un répertoire de travail, un chemin interdit ou un problème d'authentification, voyez la section 2.8.

## 2.3 Les vues de Bob utilisées dans ce guide

Bob affiche différentes vues selon l'icône sélectionnée dans la barre de gauche. Les chapitres suivants désignent les cinq vues ci-dessous par ces noms.

### File Explorer

Ouvrez-le avec l'icône des fichiers en haut de la barre de gauche. Il affiche le dossier de projet sur votre disque : les dossiers `guide` et `walkthroughs` du dépôt, les dossiers créés par l'extension (`agents`, `tools`, `connections`, `knowledge-bases`, `toolkits`, `models`), et chaque fichier que Bob écrit. Cliquez sur un fichier pour l'ouvrir dans l'éditeur.

Dans le File Explorer, vous lisez une conception ou une définition d'Agent que Bob a écrite, et vous ouvrez les chapitres de ce guide.

![Le File Explorer avec le dossier de projet ouvert](images/ch02-file-explorer.png)

### Panneau watsonx Orchestrate

Ouvrez-le avec l'icône watsonx Orchestrate dans la barre de gauche. Il comporte deux sections.

- Explorer liste ce qui existe sur votre instance : Agents, Tools, Connections, Knowledge Bases et Toolkits. Les listes sont lues sur l'instance, pas dans les fichiers du dossier de projet.
- Environment Manager affiche les environnements dans une liste déroulante, l'environnement actif étant marqué « (active) », un bouton Add pour enregistrer une autre instance et, pour la Developer Edition, l'état du serveur local avec un bouton pour le démarrer ou l'arrêter.

Utilisez l'Explorer pour confirmer qu'une importation a eu lieu : un Agent qui apparaît sous Agents existe sur l'instance. Pour actualiser une liste, placez le pointeur sur sa ligne, par exemple Agents, et cliquez sur l'icône d'actualisation qui y apparaît.

Un élément de l'Explorer propose ces actions :

- Cliquer sur le nom d'un élément enregistre une copie de sa définition depuis l'instance dans le dossier de projet, pour un Agent sous la forme `agents/<name>.yaml`, et l'ouvre. Si un fichier de ce nom existe déjà, une boîte de dialogue demande s'il faut le remplacer. Choisissez Cancel pour conserver votre fichier. Utilisez cette action lorsque vous voulez la définition exactement telle que l'instance la détient.
- L'icône de conversation sur la ligne d'un Agent ouvre une conversation avec cet Agent.
- L'icône de corbeille supprime l'élément de l'instance, après confirmation.

L'Environment Manager, sous l'Explorer, est l'endroit où vous réactivez un environnement lorsque son jeton a expiré, ou passez à une autre instance.

![Le panneau watsonx Orchestrate après l'initialisation : Explorer et Environment Manager](images/ch02-orchestrate-panel.png)

### Source Control

Ouvrez-le avec l'icône de branche dans la barre de gauche ; il liste les fichiers modifiés depuis le dernier commit. Depuis cette vue, vous pouvez indexer des fichiers, taper un message de commit, valider et synchroniser avec le dépôt distant, d'un clic.

Utilisez Source Control pour voir ce que Bob a modifié dans le dossier de projet et pour conserver votre travail dans git. Le chapitre 3, section 3.6, décrit comment faire les mêmes opérations en le demandant à Bob.

### Panneau de conversation de Bob

L'icône de Bob ouvre le panneau où vous écrivez les prompts et lisez les réponses de Bob. Les commandes suivantes sont utilisées tout au long du guide.

| Commande | Emplacement | Rôle |
|---|---|---|
| Liste déroulante des modes | En bas de la zone de saisie | Détermine le mode qu'utilise Bob pour la conversation |
| Bouton Permissions | À côté de la liste déroulante des modes, en bas de la zone de saisie | Ouvre la liste des actions que Bob peut réaliser sans demander : Read, Edit, Execute, MCP et d'autres |
| Nouvelle conversation | Le signe plus en haut du panneau | Une conversation vierge, sans rien des précédentes |
| Mention @ | Tapée dans la zone de saisie | Désigne un fichier ou un dossier, pour que Bob le lise |
| Boutons d'approbation et de refus | Au-dessus de la zone de saisie, lorsque Bob demande une action | Autorisent ou refusent l'action que Bob propose |

![Le panneau de conversation de Bob avec la liste déroulante des modes et le bouton Permissions](images/ch02-chat-panel-modes.png)

### Réglages de Bob, onglet MCP

Ouvrez les réglages de Bob avec l'icône des réglages dans le panneau de conversation de Bob, puis sélectionnez l'onglet MCP. Il liste les serveurs auxquels Bob est connecté ; en déplier un affiche son état et ses opérations, chacune avec un interrupteur Always allow, et une commande pour redémarrer le serveur.

L'onglet MCP est aussi l'endroit où vous vérifiez que les deux serveurs Orchestrate sont connectés, réglez les interrupteurs Always allow et redémarrez un serveur lorsqu'une opération échoue sans raison apparente.

![L'onglet MCP avec les deux serveurs Orchestrate et les interrupteurs Always allow](images/ch02-mcp-tab.png)

### Comment les vues sont liées

Une définition d'Agent est un fichier dans le File Explorer jusqu'à ce que Bob l'importe. Après l'importation, l'Agent apparaît dans la section Explorer du panneau watsonx Orchestrate. Si les deux diffèrent, l'instance n'a pas reçu la dernière version du fichier, ou le fichier a été modifié après l'importation. Source Control montre quels fichiers ont changé depuis le dernier commit.

## 2.4 Ce qui a été installé

Les composants suivants apparaissent par leur nom dans les messages de Bob et dans l'onglet MCP.

| Composant | Ce qu'il fait |
|---|---|
| Le watsonx Orchestrate Agent Development Kit, l'ADK | Définit les Agents, les Outils et tout ce qui les entoure sous forme de fichiers, et envoie ces fichiers à une instance. Installé à l'étape 3 |
| Le serveur MCP watsonx Orchestrate, `watsonx-orchestrate-adk` dans l'onglet MCP | Permet à Bob d'utiliser l'ADK : lister, importer, tester et exporter des éléments sur votre instance. Bob le démarre au besoin. MCP est le protocole standard qu'utilisent les assistants de codage pour communiquer avec de tels programmes |
| Le serveur de documentation d'IBM, `watsonx-orchestrate-adk-docs` dans l'onglet MCP | S'exécute sur Internet et permet à Bob de rechercher dans la documentation d'Orchestrate, pour que Bob consulte la documentation au lieu de s'appuyer sur ses connaissances générales |

1. Le serveur Orchestrate lit et écrit uniquement dans le dossier qui était ouvert lorsque vous avez initialisé l'espace de travail. Ouvrez toujours ce dossier dans Bob.
2. Sur un tenant, la clé d'API donnée à l'étape 5 a produit un jeton qui expire au bout de deux heures. Ensuite, chaque opération échoue avec une erreur d'authentification jusqu'à ce que vous réactiviez l'environnement dans l'Environment Manager.
3. L'ADK conserve un seul environnement actif par machine, et Bob comme tout autre assistant de codage de la machine l'utilisent. Changer d'environnement dans l'Environment Manager le change pour tous. Aucun chapitre de ce guide ne change d'environnement.

## 2.5 Les approbations, expliquées

- Le bouton Permissions, à côté de la liste déroulante des modes en bas de la zone de saisie, ouvre un interrupteur par catégorie. Read permet à Bob de lire des fichiers sans demander. MCP lui permet d'exécuter des opérations Orchestrate sans demander, mais uniquement celles que vous marquez une à une. Edit et Execute couvrent l'écriture de fichiers et l'exécution de commandes. Laissez Edit et Execute désactivés, pour que Bob demande avant d'écrire des fichiers ou d'exécuter des commandes.
- L'interrupteur Always allow de chaque opération dans l'onglet MCP approuve cette opération de façon permanente ; l'étape 7 a approuvé les onze opérations qui ne font que lire l'instance ou envoyer un message de test. Toute autre opération, comme importer, créer, supprimer ou définir des identifiants, demande toujours une approbation.

## 2.6 Autres assistants de codage par IA

Le serveur Orchestrate est le même pour tous les assistants. Cursor et VS Code avec Copilot ont la même extension et les mêmes étapes ; Claude Code et Claude Desktop se connectent au moyen d'un fichier de réglages qui nomme le serveur et le dossier. L'installation pour chacun est décrite à l'adresse https://developer.watson-orchestrate.ibm.com/mcp_server/wxOmcp_installation. Si cette adresse a changé, recherchez l'installation du serveur MCP dans la documentation de l'ADK watsonx Orchestrate.

## 2.7 Liste de contrôle

1. Le dossier ouvert dans Bob est le dépôt cloné, et c'est celui que vous avez initialisé.
2. Le dossier `guide` est visible au premier niveau de ce dossier, à côté des dossiers créés par l'extension.
3. Le fichier `.env` est à la racine de ce dossier, et `.bob/skills` contient les skills Orchestrate chargés à l'étape 4.
4. L'onglet MCP affiche `watsonx-orchestrate-adk` et `watsonx-orchestrate-adk-docs`, tous deux connectés.
5. Sous le bouton Permissions, Read et MCP sont activés et Edit et Execute désactivés, et Always allow est activé pour les onze opérations de lecture.
6. L'Environment Manager affiche un environnement actif.
7. Le prompt de liste des Agents renvoie les Agents attendus, sans demande d'approbation.

## 2.8 Quand quelque chose ne va pas

| Bob signale | Cause | Solution |
|---|---|---|
| `Attempting to access resources outside the working directory is forbidden.` | Le dossier ouvert dans Bob n'est pas celui qui a été initialisé, ou Bob pointe vers un fichier ailleurs sur votre disque | Ouvrez le dossier initialisé. Si vous devez changer de dossier, exécutez Update MCP Servers depuis la palette de commandes avec le bon dossier ouvert |
| Chaque opération échoue avec une erreur d'authentification ou d'autorisation après avoir fonctionné | Le plus souvent, le jeton de deux heures de l'étape 5 a expiré | Réactivez l'environnement dans l'Environment Manager ; l'appel suivant fonctionne sans redémarrage |
| Un artefact a été importé, mais l'Explorer du panneau watsonx Orchestrate ne l'affiche pas | Certaines opérations annoncent un succès même lorsque la plateforme a enregistré une erreur. L'importation d'une Base de connaissances avec un type de document non pris en charge en fait partie | Fiez-vous à la liste, pas au message. Après une importation, demandez à Bob de lister les artefacts de ce type et vérifiez que le nouveau y figure |
| L'importation d'un Outil Python échoue avec `No module named '<tool>'` alors que le fichier existe | Bob a tenté d'importer depuis ce dossier avant qu'il existe, et le serveur garde l'échec en mémoire tant qu'il tourne | Redémarrez le serveur avec la commande de redémarrage de l'onglet MCP, puis importez de nouveau |
| La commande du serveur est introuvable, ou l'entrée ne démarre pas | Le plus souvent, l'environnement Python créé par l'extension est endommagé ou a été déplacé | Exécutez de nouveau Initialise Workspace ; il le répare |
| `watsonx-orchestrate-adk` apparaît déconnecté et ne redémarre pas depuis l'onglet MCP, alors que l'environnement est actif | L'entrée démarre à chaque fois la version la plus récente du paquet du serveur, et une nouvelle version peut échouer au démarrage | En mode Agent, demandez à Bob : `Run the command of the watsonx-orchestrate-adk entry of .bob/mcp.json in a terminal and show me its error.` Si l'erreur nomme le paquet, demandez à Bob de fixer dans cette entrée la version de votre ADK, par exemple `ibm-watsonx-orchestrate-mcp-server@2.18.0`, puis redémarrez le serveur depuis l'onglet MCP et ouvrez une nouvelle conversation |

Lorsque Bob teste un Agent qui n'a pas d'Outils, il indique que le raisonnement est vide.
