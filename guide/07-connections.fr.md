# Chapitre 7. Signaler un problème : les Connexions Orchestrate

Niveau : débutant. Durée : environ 60 minutes. Prérequis : chapitre 6 terminé, ou ses Outils et son Agent importés depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre.

## Vue d'ensemble

Un nid-de-poule devant le 18 Elm Street est là depuis un mois, et c'est vous, l'habitant, qui roulez dedans chaque matin. Vous demandez à CivicPulse : « There is a pothole outside 18 Elm Street. Can you report it? » L'Agent du chapitre 6 peut vous donner l'état d'un signalement existant, mais il ne peut pas en créer un.

Dans ce chapitre, Bob crée un Outil Orchestrate qui envoie le signalement au centre d'appels 311 de la ville. Un centre d'appels 311 est le service qui traite les demandes non urgentes dans les villes nord-américaines, du nom du numéro que composent les habitants ; chaque signalement devient une demande de service avec un numéro. Pour l'Agent, le centre d'appels 311 est un système externe, comme une base de données ou une application, et l'Agent l'atteint comme il atteignait les dossiers du chapitre 6 : par un Outil Orchestrate. Le système externe exige des identifiants. watsonx Orchestrate les conserve dans un asset distinct, la Connexion Orchestrate, et les donne à l'Outil lorsque l'Agent l'appelle.

Bob crée aussi la Connexion Orchestrate. Avec la Connexion et l'Outil, l'Agent peut mettre à jour un système externe, et plus seulement le consulter.

Sautez ce chapitre si vous avez déjà fourni un identifiant à un Outil par une Connexion avec Bob. Pour continuer avec le chapitre 8 sans le construire, ajoutez à votre fichier `.env` la ligne que décrit la section 7.6, puis envoyez à Bob ces instructions en mode Agent : `Create the connection utopia_311 on my instance, kind API key sent in the header x-api-key, type team, for the Draft environment, and set its Draft credential from the variable UTOPIA_311_API_KEY in my .env file without displaying its value. Then import the tool walkthroughs/ch07/tools/report_issue.py with that connection, and import walkthroughs/ch07/agents/civic_info_agent.yaml.`

## 7.1 Avant de commencer

- La mise en place du chapitre 2, complète.
- L'Agent `civic_info_agent` du chapitre 6 sur votre instance, en Draft, avec ses trois Outils. Si vous avez sauté le chapitre 6, importez-les comme le décrit la Vue d'ensemble de ce chapitre.
- Une nouvelle conversation dans Bob pour ce chapitre.

Vérifiez que les Outils sont là : en mode Ask, demandez `Which tools exist on my instance?` et vérifiez que `get_permit_status`, `get_request_status` et `get_collection_days` figurent dans la liste.

## 7.2 Ce qu'est une Connexion Orchestrate

Presque tous les Agents d'un vrai projet dialoguent avec des systèmes appartenant à d'autres équipes : une base de données, un système de tickets, une application de paie, un modèle hébergé par un fournisseur, un serveur MCP, un index de documents. Chacun a une adresse et un moyen de prouver qui appelle : un utilisateur et un mot de passe, une clé d'API, un jeton, ou une connexion que l'utilisateur effectue lui-même. Dans watsonx Orchestrate, tout cela réside dans un seul type d'asset, la Connexion Orchestrate, et les Outils, Boîtes à outils, Modèles et Bases de connaissances qui ont besoin d'un système font référence à sa Connexion par son nom.

Lorsqu'un projet passe d'un Outil à vingt, une équipe d'exploitation voit dans la liste des Connexions quels systèmes atteignent les Agents et avec quels identifiants, par environnement. L'Agent du chapitre 4, qui ne lit que ses instructions, n'a pas de Connexion.

Le tableau liste où une Connexion est utilisée dans un projet.

| Où une Connexion est utilisée | Exemple | Dans ce guide |
|---|---|---|
| Un Outil Python qui appelle une API ou interroge une base de données | Le centre d'appels 311, un CRM, un service de paiement, une base SQL | Ce chapitre |
| Un Outil OpenAPI, construit à partir de la description d'une API REST existante | L'ERP de votre entreprise, un système de tickets, une application RH | Non construit ; même Connexion |
| Une Boîte à outils MCP dont le serveur exige un identifiant | Un serveur MCP tiers avec une clé d'API | Chapitre 8 |
| Un Modèle hébergé par un autre fournisseur | Un modèle watsonx.ai ou OpenAI utilisé par un Agent | Non construit |
| Une Base de connaissances conservée dans un magasin externe | Des documents indexés dans Elasticsearch ou Milvus | Non construit |
| Une connexion que chaque utilisateur effectue | Un système où l'Agent agit au nom de la personne, par OAuth | Non construit |

Un Outil qui appelle un service a besoin de l'adresse du service et, pour la plupart des services, d'un identifiant que le service accepte. L'adresse peut être écrite dans l'Outil ; une clé ne le peut pas, car le code va dans git, dans chaque copie du projet et dans chaque conversation qui affiche le fichier.

Une Connexion Orchestrate est l'endroit où watsonx Orchestrate conserve l'identifiant à la place. Elle a un nom, le type d'identifiant (une clé d'API, un utilisateur et un mot de passe, un jeton, une connexion OAuth), l'identifiant lui-même, et l'adresse du service lorsque l'Outil ne la porte pas. Un Outil nomme la Connexion dont il a besoin, et la plateforme transmet l'identifiant à l'Outil lorsque l'Agent l'appelle.

**La définition et l'identifiant**

Une Connexion Orchestrate est définie sans son secret : un nom, le type d'identifiant, le type de partage. Bob écrit cette définition soit sous forme de fichier dans le dossier `connections`, comme un Agent ou un Outil, soit sous forme de deux commandes dans son script d'importation, l'une qui crée la Connexion et l'autre qui la configure. Dans les deux cas, elle est écrite par le développeur et va dans git. L'identifiant est défini séparément, sur l'instance, par la personne qui le détient. Dans une entreprise, c'est l'équipe propriétaire du service ou l'équipe d'exploitation, et le développeur n'a pas besoin de voir la clé de production. Dans ce guide, vous jouez les deux rôles : Bob importe la Connexion, et la clé vient de votre fichier `.env` (chapitre 2).

**Un identifiant par environnement**

Chaque environnement conserve son propre identifiant : Draft contient une clé de test et Live la clé de production. Vous testez en Draft ; l'exploitation définit la clé Live lorsque l'Agent est déployé. Déployer l'Agent ne copie pas l'identifiant. Dans ce chapitre, la Connexion est d'abord définie pour Draft ; la section 7.10 ajoute l'environnement Live et sa clé avant le déploiement.

**Partagée ou personnelle**

Une Connexion est soit partagée par tous, `team`, avec un identifiant unique que définit un administrateur, soit personnelle, `member`, auquel cas chaque utilisateur est invité à fournir son propre identifiant dans la conversation la première fois. Le compte du centre d'appels 311 de la ville est partagé, la Connexion de ce chapitre est donc une Connexion team.

**Le centre d'appels 311 de ce chapitre**

Le centre d'appels 311 n'a pas encore donné accès à son système aux créateurs de la ville, ce chapitre utilise donc à sa place un service de test public, Postman Echo, qui répond à chaque requête en renvoyant ce qu'il a reçu, en-têtes compris. Le mécanisme est le même qu'avec un vrai système 311 : l'Outil envoie le signalement avec la clé dans un en-tête, et il ne considère le signalement comme accepté que si le service renvoie cet en-tête. La clé peut être n'importe quelle valeur que vous inventez, car le service de test accepte tout. Un vrai système 311 renverrait aussi un numéro de demande ; le service de test n'en renvoie pas, l'Outil en crée donc un au format du chapitre 6.

## 7.3 Mode Ask : décrire le signalement

Mode : Ask, dans une nouvelle conversation.

Le prompt décrit ce dont ont besoin les habitants et quel système est concerné, et ne dit rien de la manière dont ce système est atteint ou sécurisé. Bob doit comprendre la demande avant que quoi que ce soit ne soit écrit, et c'est à Bob de soulever la question des identifiants.

```
I want civic_info_agent to report a road problem to the 311 Call Center
when a resident asks it to, for example "There is a pothole outside 18 Elm
Street. Can you report it?". The 311 Call Center is an external system, and the
city has not given us access yet, so for now the public test service at
https://postman-echo.com/post, which returns what it receives, stands in for
it.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Points à vérifier dans la réponse de Bob :

- Bob soulève la question des identifiants, que personne n'a mentionnée. Le service de test n'en a pas besoin, mais le vrai système 311 exigera une adresse et une clé d'API, Bob demande donc s'il faut créer une Connexion dès maintenant, pour que l'Outil soit correctement câblé lorsque la ville donnera l'accès. Si votre Bob ne la soulève pas, la réponse ci-dessous le fait.
- Sur l'instance, Bob trouve l'Agent, la Base de connaissances, les trois Outils et les Connexions intégrées de la plateforme, pour des produits comme Salesforce ou ServiceNow, dont aucune n'appartient au projet. Dans le projet, le dossier `connections` est vide. Bob trouve aussi la ligne des instructions de l'Agent, venue du chapitre 4, qui interdit de créer des demandes, et dit qu'elle doit changer.
- Les questions varient d'une exécution à l'autre : ce que contient le signalement, en texte libre ou à partir d'une liste fixe de types de problèmes, et si les habitants s'identifient ; ce que l'Agent répond, et quel numéro de référence il donne, puisque le service de test n'en renvoie pas ; si l'Agent confirme les détails avant l'envoi ; s'il faut écrire un Outil Python ou un Outil OpenAPI ; et comment s'authentifie le vrai système 311.

Un ingénieur d'intégration pose les mêmes questions avant de connecter n'importe quel système externe. Le prompt ne mentionnait pas les identifiants ; dans la plupart des exécutions Bob les soulève, et le second prompt y répond, en nommant la Connexion et l'en-tête pour que le chapitre et les fichiers walkthrough concordent.

```
These are my answers. Create the connection now: the real 311 system will
require an API key with every request, and the tool must send it from the
start, so that only the address and the key change when the city gives
access. The connection is named utopia_311, shared by the whole team,
with the key sent in the header x-api-key. For now the key is a test value
that I invent, since the test service accepts anything, but it is stored and
used exactly as the real key will be. The key must never appear in the chat,
in the project files or in the tool's code. It is in my .env file, as the
variable UTOPIA_311_API_KEY, and the credential is set from that variable
with the orchestrate command in a shell that reads my .env file, so that the
value never appears in the chat, in a tool call or in a file.

One Python tool, report_issue, which receives the street and a free-text description
of the problem, with no category and no resident details, since reports are
anonymous. It sends them to the 311 Call Center with the key from the connection
and returns a request number in the format RQ-2026-NNNN that the tool
generates, since the test service returns none. The tool treats a report as
accepted only if the service echoes the key header back; otherwise it reports
a failure, and the agent says that the report could not be sent and gives the
contact of Roads and Infrastructure.

The agent uses the tool when a resident asks to report a road problem. It
sends the report as soon as it has the street and a description, without a
confirmation step, and asks for whatever is missing. After a successful
report, the agent gives the resident the request number and says that the
status can be checked with it. The line that forbids creating requests is
replaced by this tool. The facts, the knowledge base and the three lookup
tools stay as they are.
```

Bob confirme les réponses et expose la mise en œuvre dans la conversation, comme au chapitre 6, en code complet dans certaines exécutions et sous forme d'esquisse dans d'autres. Vérifiez-y ces points :

- La Connexion ne porte aucune clé : un nom, le type d'identifiant, le type `team`, l'adresse du service.
- L'Outil obtient la clé de la Connexion lorsqu'il s'exécute, et ne l'envoie que dans l'en-tête de la requête.
- Bob définit la clé à partir de la variable de `.env`, avec une commande qui n'affiche pas la valeur, et ne vous demande jamais de la coller dans la conversation.

Ne passez pas encore en mode Agent. Bob termine souvent une réponse en mode Ask par cette invitation. Passez d'abord en mode Plan, comme le recommande la documentation de Bob elle-même : le fichier de conception est l'endroit où vous vérifiez les décisions avant que quoi que ce soit n'existe sur l'instance, et il reste dans le projet, sous git, comme trace de ce qui a été décidé.

## 7.4 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

```
Write the design for this change into design/report-issue-design.md.
```

Bob écrit le fichier après votre approbation et le résume. Ouvrez `design/report-issue-design.md` et comparez-le à ce tableau :

| Contenu | Ce qu'il faut vérifier |
|---|---|
| La Connexion | Son nom, `utopia_311` ; le type, une clé d'API envoyée dans l'en-tête `x-api-key` ; l'adresse du service ; partagée par l'équipe ; définie pour Draft. Live est ajouté en 7.10 |
| L'identifiant | La conception dit que l'identifiant est défini à partir de la variable `UTOPIA_311_API_KEY` de `.env`, avec la commande orchestrate dans un shell, après l'importation, et qu'aucun autre fichier ni aucun prompt ne contient la valeur |
| L'Outil | `report_issue`, ses deux paramètres, la Connexion qu'il utilise, la vérification de l'en-tête renvoyé, le numéro de demande qu'il renvoie |
| La modification de l'Agent | L'Outil rattaché ; les instructions disent quand l'utiliser, quoi demander d'abord, quoi répondre en cas de succès et d'échec ; tout le reste inchangé |
| L'ordre de construction | La Connexion et son identifiant depuis `.env`, l'Outil, l'Agent, puis le test |

## 7.5 Approuver la conception

Mode : Plan, même conversation.

N'envoyez de prompt dans cette section que si la conception doit être modifiée. Comparez la conception au tableau de 7.4. Elle ne doit contenir aucune valeur de clé, pas même une valeur d'exemple. Si c'est le cas, envoyez `Remove every credential value from the design. The credential is set on the instance, not in a file.` S'il manque autre chose, demandez à Bob de l'ajouter. Bob peut aussi vous interroger sur des détails que la conception ne fixe pas, comme l'emplacement d'un fichier requirements ; répondez `Decide these yourself and proceed.` Lorsque la conception est correcte, ajoutez la clé à `.env` comme le décrit 7.6, puis passez à 7.7 : son premier prompt est l'approbation.

## 7.6 D'où vient la clé

La Connexion que Bob importe a un nom et un type mais pas de clé. C'est à vous de fournir la clé, et elle ne doit pas transiter par la conversation. Le guide la conserve là où le chapitre 2 conserve l'autre secret du projet : le fichier `.env` de votre dossier de projet, que git ignore. Ouvrez `.env` et ajoutez une ligne, avec une valeur que vous inventez. Après la modification, le fichier ressemble à ceci, avec vos propres valeurs à la place des marqueurs :

```
WO_INSTANCE=<the URL of your instance>
WO_API_KEY=<the API key of your instance>
UTOPIA_311_API_KEY=<a word and a number>
```

Sur la Developer Edition, les deux premières lignes sont vides et seule la troisième compte.

![Le fichier .env dans l'éditeur avec ses trois variables, les valeurs floutées](images/ch07-env-file.png)

Cette variable est le moyen par lequel la clé atteint l'instance sans transiter par la conversation : la commande de l'ADK qu'exécute Bob la lit depuis le shell, la clé n'apparaît donc dans aucune conversation ni dans aucun fichier du projet autre que `.env`. Dans une entreprise, la valeur vient d'un coffre-fort de secrets plutôt que d'un fichier `.env`, et la commande est la même que celle qu'exécute un pipeline de déploiement.

## 7.7 Mode Agent : construire et tester

Mode : Agent, dans une nouvelle conversation.

La construction commence dans une nouvelle conversation pour la raison donnée au chapitre 4 : la conversation de planification contient la première proposition de Bob et vos corrections, et Bob pourrait construire à partir d'elles au lieu de la conception que vous avez approuvée.

```
The design in @design/report-issue-design.md is approved. Build it. Set the
Draft credential of the connection from the variable UTOPIA_311_API_KEY in
my .env file, without displaying its value, then test the agent with the
pothole report of the Overview.
```

La troisième phrase est nouvelle : elle dit à Bob où se trouve la clé et que la valeur ne doit pas être affichée. Bob :

1. Définit la Connexion, sous forme de fichier dans le dossier `connections` ou avec des commandes, l'importe, et définit son identifiant Draft à partir de `.env`.
2. Écrit l'Outil dans le dossier `tools` et l'importe, avec la Connexion nommée.
3. Met à jour l'Agent, qui reçoit l'Outil et des instructions plus longues, et l'importe de nouveau, remplaçant l'Agent en Draft.
4. Teste l'Agent avec le signalement du nid-de-poule.

Approuvez chaque demande au fur et à mesure. Lisez la commande qui définit l'identifiant lorsque Bob demande l'approbation : elle nomme la variable et n'affiche aucune valeur. Si Bob propose de définir l'identifiant par l'une de ses opérations Orchestrate plutôt que par une commande, dites-lui d'utiliser la commande avec la variable ; une valeur transmise à une opération passe par la conversation.

Si le test échoue, Bob lit l'erreur et la corrige. Une erreur d'authentification signifie généralement que l'identifiant est allé vers un autre environnement ou une autre Connexion ; une erreur de lecture de la Connexion signifie généralement que le code de l'Outil nomme une Connexion que l'instance n'a pas.

## 7.8 Ce que Bob a construit

La Connexion est définie à l'un de deux endroits, selon l'exécution : un fichier `utopia_311.yaml` dans le dossier `connections`, ou deux commandes dans le script d'importation de Bob, l'une qui crée la Connexion et l'autre qui la configure. Dans les deux cas, la définition tient en quelques lignes : le nom, le type d'identifiant, une clé d'API, le type, `team`, et l'environnement Draft. Elle ne contient aucune clé, elle peut donc être partagée et validée. Un dossier `connections` vide signifie que Bob a utilisé les commandes. Dans ce cas, vérifiez que la Connexion existe sur l'instance : en mode Ask, `Which connections of this project exist on my instance, and is a credential set for them?` Bob liste `utopia_311` avec un identifiant défini pour Draft et aucun encore pour Live, ce que complète la section 7.10.

Ouvrez `tools/report_issue.py`. La ligne `@tool` nomme la Connexion qu'attend l'Outil, `utopia_311`. Vers le début de la fonction, une ligne obtient la clé auprès de la plateforme, depuis une variable que la plateforme définit lorsque l'Outil s'exécute ou par la bibliothèque des Connexions ; votre variable de `.env` ne sert qu'à placer la clé sur l'instance. La fonction n'utilise la clé que dans l'en-tête de la requête. La fonction envoie ensuite le signalement, vérifie que l'écho contient l'en-tête, construit le numéro de demande et le renvoie.

Ouvrez `agents/civic_info_agent.yaml`. Sous `tools`, un quatrième nom apparaît, `report_issue`. Les instructions ont un nouveau paragraphe : lorsqu'un habitant demande à signaler un problème de voirie, obtenir la rue et la description, appeler l'Outil, et répondre avec le numéro de demande, ou avec le contact de Roads and Infrastructure si le signalement n'a pas pu être envoyé.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 7.9 Essayez

Posez la question à l'Agent, par l'intermédiaire de Bob avec `Ask civic_info_agent:` devant, ou dans le panneau d'aperçu de watsonx Orchestrate :

```
There is a pothole outside 18 Elm Street. Can you report it?
```

L'Agent effectue le signalement et répond avec un numéro de demande au format RQ-2026, dit que l'état peut être vérifié avec ce numéro, et donne le contact de Roads and Infrastructure. Essayez ensuite ces questions :

- Omettez la rue : « I want to report a broken street light. » L'Agent demande où.
- Mettez tout dans une phrase : « Report a damaged road sign at the corner of Mill Road and Station Road, it has been down since Monday. » L'Agent fait un seul signalement et renvoie un seul numéro.
- Vérifiez le numéro qu'on vous a donné : « Has my report RQ-2026-NNNN been scheduled? », avec le numéro de la première réponse. L'Agent le consulte avec l'Outil du chapitre 6, répond qu'il n'a pas de dossier sous ce numéro et donne le contact : cet Outil lit son propre fichier de dossiers, que ce chapitre n'a pas modifié, et le service de test ne conserve rien. Avec un vrai système 311, les deux Outils liraient les mêmes dossiers.

Posez de nouveau la première question avec le raisonnement. Les étapes montrent l'appel à `report_issue` avec la rue et la description, et le résultat de l'Outil avec le numéro de demande. Les étapes ne montrent pas la clé, que l'Outil a reçue de la Connexion.

## 7.10 Déployer la modification en Live

Mode : Agent, même conversation.

L'Agent qui signale les problèmes existe en Draft, et la Connexion n'existe que pour Draft : déployé tel quel, l'Agent échouerait au premier signalement. Sur la Developer Edition, sautez cette section. Faites les deux étapes dans cet ordre. Dans une entreprise, la première est faite par l'exploitation, avec la clé de production ; ici, c'est Bob avec votre clé de test.

D'abord, la Connexion reçoit son environnement Live et sa clé Live :

```
Configure the connection utopia_311 for the Live environment with the same
kind and type as in Draft, and set its Live credential from the variable
UTOPIA_311_API_KEY in my .env file, without displaying its value.
```

Ensuite, déployez :

```
Deploy civic_info_agent from draft to live.
```

Lorsque Bob annonce le déploiement, allez dans la conversation watsonx Orchestrate et signalez le nid-de-poule : l'habitant de la Vue d'ensemble obtient un numéro de demande.

![La page Connections de watsonx Orchestrate avec utopia_311 et ses environnements Draft et Live](images/ch07-connections-page.png)

## 7.11 Résumé

L'Agent peut maintenant agir pour le compte d'un habitant : il signale un nid-de-poule au centre d'appels 311 et donne à l'habitant un numéro de demande. La clé a été conservée à deux endroits, votre fichier `.env` et l'instance, et envoyée au service dans un en-tête de requête ; la conversation, git et le code ne l'ont jamais contenue.

- Une Connexion Orchestrate est l'endroit où watsonx Orchestrate conserve un identifiant pour un service. Un Outil nomme la Connexion dont il a besoin et reçoit l'identifiant à l'exécution ; la clé n'apparaît dans aucun fichier sous git ni dans aucune conversation.
- La Connexion est définie par le développeur et importée avec le projet. L'identifiant est défini séparément sur l'instance, une fois par environnement, Draft et Live, depuis un endroit que git ne voit pas.
- Les Connexions team partagent un identifiant unique entre tous les utilisateurs ; les Connexions member demandent à chaque utilisateur le sien, dans la conversation.
- Construire un Outil Orchestrate qui agit demande les mêmes parties qu'un Outil qui consulte, une fonction, une description, des paramètres et un résultat, et l'Agent décide quand l'appeler de la même manière.

L'Agent consulte maintenant des dossiers et envoie de nouveaux signalements, avec quatre Outils Python que Bob a écrits et que la ville maintient. Beaucoup de services sont livrés avec leurs Outils prêts à l'emploi, sous forme de serveur MCP que n'importe quel Agent peut utiliser ; watsonx Orchestrate importe tout l'ensemble en une étape, sous forme de Boîte à outils Orchestrate. Au chapitre 8, Bob en construit une, et l'Agent en tire une recherche d'adresse.
