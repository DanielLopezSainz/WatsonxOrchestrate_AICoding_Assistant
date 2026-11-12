# Chapitre 5. Ajouter une Base de connaissances Orchestrate (RAG)

Niveau : débutant. Durée : environ 60 minutes. Prérequis : chapitre 4 terminé, ou son Agent importé depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre.

## Vue d'ensemble

Vous voulez construire un abri de jardin et devez savoir s'il faut un permis. Les bureaux de la ville sont fermés, alors vous interrogez CivicPulse. L'Agent du chapitre 4 peut seulement vous dire que Permits and Planning s'occupe des permis et quand le service est ouvert. Il connaît vingt lignes de faits, et la réponse à votre question se trouve dans le guide des permis de construire de la ville (Building Permit Guide), qu'il n'a jamais lu.

Dans ce chapitre, l'Agent reçoit les guides et la réglementation de la ville : le Building Permit Guide, les règles de tri des déchets (Waste Sorting Rules) et l'arrêté sur le bruit (Noise Ordinance). Bob écrit les trois documents pour la ville d'Utopia, les place dans une Base de connaissances et y connecte l'Agent. L'Agent répond alors à partir des documents : si un abri a besoin d'un permis, dans quel bac va un miroir cassé, quel volume sonore une fête peut atteindre après dix heures du soir, et il nomme le document d'où vient la réponse.

L'Agent du chapitre 4 et ses faits sont inchangés ; ses instructions gagnent un paragraphe.

Sautez ce chapitre si vous avez déjà connecté une Base de connaissances à un Agent avec Bob. Pour continuer avec le chapitre 6 sans la construire, envoyez à Bob ces instructions en mode Agent : `Import walkthroughs/ch05/knowledge-bases/city_regulations.yaml into my instance, wait until the knowledge base is ready, then import walkthroughs/ch05/agents/civic_info_agent.yaml.`

## 5.1 Avant de commencer

- La mise en place du chapitre 2, complète.
- L'Agent `civic_info_agent` du chapitre 4 sur votre instance, en Draft, avec la correction de la section 4.9. Si vous avez sauté le chapitre 4, importez-le comme le décrit la Vue d'ensemble de ce chapitre ; le fichier du dossier walkthrough contient déjà la correction.
- Une nouvelle conversation dans Bob pour ce chapitre.

Vérifiez que l'Agent est là : en mode Ask, demandez `Which agents exist on my instance?` et vérifiez que `civic_info_agent` figure dans la liste.

## 5.2 Ce qu'est une Base de connaissances Orchestrate

Les instructions d'un Agent peuvent contenir environ une page de faits. La réglementation d'une ville compte des centaines de pages et est révisée de temps à autre par des personnes qui n'ont aucune raison de savoir ce que disent les instructions de l'Agent ; pour de tels documents, l'Agent utilise une Base de connaissances Orchestrate.

Une Base de connaissances Orchestrate est un ensemble de documents que watsonx Orchestrate indexe, pour qu'un Agent puisse y faire des recherches. Lorsqu'un habitant pose une question, l'Agent cherche les passages des documents les plus proches de la question, les lit et répond à partir d'eux. Les documents ne sont pas copiés dans les instructions.

**Quand une Base de connaissances Orchestrate est le bon composant**

Le choix entre les deux dépend de l'endroit où se trouve l'information et de qui la tient à jour. Les instructions conviennent à un petit ensemble de faits stables qui appartiennent au créateur de l'Agent, comme les trois services du chapitre 4. Une Base de connaissances convient lorsque l'information :

- Est trop volumineuse pour des instructions, comme un guide des permis ou un manuel des employés.
- Existe déjà sous forme de documents, écrits et tenus à jour par d'autres personnes. Le service juridique met à jour la réglementation et l'équipe RH le manuel ; l'Agent doit suivre sans que personne ne touche à sa définition.
- Doit être donnée dans sa formulation officielle. Un habitant qui pose une question sur un tarif ou un délai veut ce que dit le document, et savoir de quel document il s'agit.

Bases de connaissances typiques dans des déploiements réels : les politiques et procédures d'une entreprise pour un assistant des employés ; la documentation produit et les guides de dépannage pour un Agent de support ; les contrats, conditions et tarifs pour un Agent de service client ; la réglementation et les formulaires pour un service public, comme la ville d'Utopia.

N'utilisez pas une Base de connaissances pour une information qui concerne une personne ou un dossier, comme l'état d'une demande de permis ou la dernière commande d'un client. Cette information se trouve dans un système et change d'une minute à l'autre ; un Outil va la chercher (chapitre 6).

**Ce qu'il faut savoir avant d'en construire une**

- Les documents sont des fichiers : texte, PDF, Word, PowerPoint, Excel, CSV ou HTML. Une Base de connaissances en contient jusqu'à 100, avec des limites de taille par type, par exemple 25 Mo pour un PDF et 5 Mo pour un fichier texte. Le texte brut est le format le plus simple, et celui qu'utilise ce chapitre.
- Après l'importation, la Base de connaissances n'est pas prête immédiatement : la plateforme traite les documents en arrière-plan et Bob vérifie l'état pendant la construction ; un Agent ne peut utiliser la Base de connaissances que lorsque son état est prêt.
- Une Base de connaissances appartient à toute l'instance. L'Agent en Draft et l'Agent déployé en Live interrogent la même Base de connaissances, donc une modification des documents atteint les habitants dès que la plateforme l'a indexée, sans déploiement.
- Mettre à jour une Base de connaissances, c'est l'importer de nouveau sous le même nom. Lorsqu'un règlement change, vous dites à Bob ce qui a changé ; Bob modifie le fichier texte et importe de nouveau la Base de connaissances, la plateforme la réindexe, et les Agents qui l'utilisent n'ont besoin d'aucune modification, car ils y font référence par son nom. Ajouter ou retirer un document fonctionne de la même manière. L'instance ne restitue pas les documents, conservez donc les fichiers texte dans le dossier de projet, dans git ; pour la ville d'Utopia, ils en sont la seule copie.
- watsonx Orchestrate propose aussi une fonction appelée chat with documents, qui permet à un utilisateur de joindre un fichier à une conversation. Ce n'est pas une Base de connaissances : le fichier n'est pas indexé pour les autres conversations, et ce guide ne l'utilise pas.

Un Agent utilise une Base de connaissances lorsque sa définition la nomme. Les instructions de l'Agent décident quand chercher : dans ce chapitre, pour toute question sur une règle ou une procédure, tandis que les contacts et les horaires restent dans les instructions.

**Les documents de ce chapitre**

La ville d'Utopia est fictive, donc dans ce chapitre vous donnez les règles dans les prompts et Bob écrit les documents ; avec de vrais documents, vous fournissez les fichiers, et le reste du chapitre est identique.

**Comment cela fonctionne, en quelques lignes**

Ce processus s'appelle la génération augmentée par la recherche (retrieval-augmented generation), RAG en abrégé : l'Agent récupère des passages de documents et le modèle de langage génère la réponse à partir d'eux. Dans watsonx Orchestrate :

- À l'importation, chaque document est découpé en passages, et chaque passage est converti en une liste de nombres qui en capture le sens, appelée embedding. Un modèle d'embedding effectue la conversion ; la Base de connaissances intégrée utilise un modèle IBM nommé `ibm/slate-125m-english-rtrvr-v2`, sauf si vous en choisissez un autre. Les passages et leurs embeddings sont stockés dans une base de données vectorielle fournie avec la plateforme, Milvus.
- Au moment de la question, la question de l'habitant est convertie de la même manière, et la base renvoie les passages dont les embeddings en sont les plus proches. Le modèle de langage rédige la réponse à partir de ces passages. L'Agent nomme le document dans ses réponses parce que ses instructions le demandent ; chaque passage porte le nom du document dont il provient.
- La base intégrée est une option parmi d'autres. Si votre organisation conserve déjà ses documents dans Milvus, Elasticsearch, OpenSearch ou Astra DB, une Base de connaissances peut pointer vers cet index au lieu d'importer des fichiers, et l'Agent l'utilise de la même manière.

## 5.3 Mode Ask : décrire les connaissances

Mode : Ask, dans une nouvelle conversation.

Les documents n'existent pas encore, le prompt indique donc à Bob ce que chacun doit contenir et à quelles questions les habitants doivent obtenir une réponse.

```
I want civic_info_agent to answer questions from the City of Utopia's guides
and regulations, not only from the facts in its instructions. Three documents
to start with: the building permit guide (when a permit is needed, how to
apply, fees and processing time), the waste sorting rules (which bin for which
waste, glass, bulky items, hazardous waste), and the noise ordinance (quiet
hours, construction work, private events, how to complain). The documents do
not exist yet; they are fictional and you will write them. Residents must get
answers to questions like "Do I need a permit for a garden shed?", "Which bin
does a broken mirror go in?" and "How loud can a party be after 10 pm?".

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob interroge l'instance et répond avec les trois parties du chapitre 4. Ses questions portent sur le format et le ton des documents, le type de Base de connaissances, les chiffres des règles, et la façon dont les instructions de l'Agent doivent changer. Bob peut terminer par une rangée de réponses suggérées sur lesquelles cliquer. Ce sont ses propres choix par défaut, et certains, comme le Markdown pour les documents, ne correspondent pas à ce chapitre ; ignorez-les et tapez la réponse ci-dessous.

Le second prompt répond aux questions de Bob et fixe les règles de ce chapitre : tout ce que l'Agent répond sur la réglementation doit en provenir.

```
These are my answers. The documents are plain text files with the .txt
extension, not Markdown, written as plain-language handouts for residents with
short sections. The knowledge base is the built-in one of the instance. Use the
following rules as they are.

Building permit guide. A permit is required for any new building, extension
or structure, except detached garden structures with a floor area under 10
square metres and a height under 2.5 metres, which need no permit. Applications
are submitted online at https://services.utopia.example/permits with a site
plan and drawings. The fee is 120 for structures under 50 square metres and 300
above. A decision is given within 30 days. Work must not start before the
decision.

Waste sorting rules. Four bins: green for food and garden waste, blue for paper
and cardboard, yellow for plastic and metal packaging, grey for everything
else. Glass bottles and jars go to the street containers, not to the bins.
Broken mirrors, window glass and drinking glasses are not accepted as glass:
wrap them and put them in the grey bin. Bulky items are collected on request,
booked online at https://services.utopia.example/bulky, up to three items per
booking, within ten working days. Paint, batteries and chemicals go to the
recycling centre at 14 Mill Road, open Saturdays 08:00 to 13:00.

Noise ordinance. Quiet hours are 22:00 to 07:00 from Sunday to Thursday and
23:00 to 08:00 on Friday and Saturday. During quiet hours, music must not be
audible outside the property. Construction work is allowed from 07:00 to
19:00 on weekdays and 08:00 to 13:00 on Saturdays, and never on Sundays.
A private event can get a one-night exemption, requested online at
https://services.utopia.example/noise at least five days in advance. Noise
complaints are reported at the same address.

The knowledge base is named city_regulations and is attached to the agent;
the chat with documents feature stays off. The agent keeps its current facts
and instructions, and searches the knowledge base for any question about a
rule, a procedure, a fee or a deadline. An answer taken from a document can be
longer than three sentences, up to a short paragraph, and still ends with the
contact of the department when one is involved. When a question is about a rule that
the documents do not cover, the agent says that it does not have that
information. In every answer taken from a document, the agent names the
document.
```

Bob confirme les réponses. Comme au chapitre 4, il peut esquisser les documents ou la conception dans la conversation.

## 5.4 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

```
Write the design for this change into design/city-regulations-design.md.
```

Bob demande l'approbation pour écrire le fichier, l'écrit et affiche un résumé. Ouvrez le fichier et comparez-le au tableau.

| Contenu | Ce qu'il faut vérifier |
|---|---|
| Les trois documents | Un nom et un plan pour chacun, couvrant chaque règle de votre réponse, sous forme de fichiers texte dans le dossier `knowledge-bases` |
| La Base de connaissances | Son nom, `city_regulations`, sa description et les trois documents |
| La modification de l'Agent | La Base de connaissances rattachée à `civic_info_agent`, et les instructions complétées : chercher les règles, dire quand une règle n'est pas couverte, nommer le document ; les faits du chapitre 4 inchangés |
| L'ordre de construction | Les documents d'abord, puis la Base de connaissances, puis l'attente qu'elle soit prête, puis l'Agent |
| Les tests | Au moins les trois questions de la Vue d'ensemble, chacune avec ce que contient une réponse correcte et le document dont elle provient |

Vérifiez que la conception prévoit une attente avant l'importation de l'Agent.

## 5.5 Approuver la conception

Mode : Plan, même conversation.

Lisez la conception. Si une règle manque ou qu'une question de test est fausse, demandez à Bob de la modifier. Lorsque la conception est correcte, elle est approuvée ; passez à 5.6.

## 5.6 Mode Agent : construire et tester

Mode : Agent, dans une nouvelle conversation.

```
The design in @design/city-regulations-design.md is approved. Build it.
```

La mention @ indique à Bob de lire le fichier de conception. Bob :

1. Écrit les trois documents, le Building Permit Guide, les Waste Sorting Rules et la Noise Ordinance, sous forme de fichiers texte dans le dossier `knowledge-bases`. Ouvrez-en un pendant que Bob continue.
2. Écrit la définition de la Base de connaissances, un fichier court qui nomme `city_regulations` et liste les trois documents.
3. Importe la Base de connaissances et attend. La plateforme indexe les documents en arrière-plan ; Bob vérifie l'état jusqu'à ce qu'elle soit prête, ce qui prend quelques minutes sur un tenant.
4. Met à jour l'Agent : la Base de connaissances est rattachée, les instructions sont complétées, et l'Agent est importé de nouveau, remplaçant l'Agent en Draft.
5. Teste l'Agent avec les questions de la conception et rend compte.

![Bob attendant la fin de l'indexation de la Base de connaissances](images/ch05-indexing-wait.png)

Approuvez chaque demande au fur et à mesure. Si une importation échoue, Bob lit l'erreur et corrige le fichier avant de continuer.

## 5.7 Ce que Bob a construit

Ouvrez le dossier `knowledge-bases` dans le File Explorer. Il contient quatre fichiers : les trois documents texte et la définition de la Base de connaissances, `city_regulations.yaml`.

Les trois fichiers texte sont le Building Permit Guide, les Waste Sorting Rules et la Noise Ordinance. Ouvrez le Building Permit Guide. Il se lit comme un dépliant de la mairie : un titre, quelques intertitres, et sous chacun la règle en phrases simples, avec les chiffres que vous avez donnés à Bob. Bob a pu ajouter ses propres exemples, comme un abri isolé de 8 mètres carrés et 2 mètres de haut qui n'a pas besoin de permis et un de 12 mètres carrés qui en a besoin. Lorsqu'un habitant pose une question sur un abri, l'Agent trouve le bon passage dans ce fichier et y puise sa réponse.

La définition de la Base de connaissances, `city_regulations.yaml`, est un fichier court qui ne contient aucune règle : il contient le nom de la Base de connaissances, une phrase qui dit ce que couvrent les documents, pour que l'Agent sache quand y chercher, et la liste des trois documents.

Le troisième fichier à ouvrir est `agents/civic_info_agent.yaml` ; cherchez-y deux modifications. Le nom `city_regulations` apparaît maintenant sous `knowledge_base` : l'Agent peut utiliser la Base de connaissances. Les instructions gagnent un nouveau paragraphe qui dit à l'Agent quoi en faire : chercher dans les documents pour toute question sur une règle, dire de quel document vient la réponse, et dire quand les documents ne couvrent pas une question. Tout ce qui vient du chapitre 4, les trois services et leurs contacts, est toujours là. Le fichier comporte aussi un long bloc nommé `chat_with_docs` avec `enabled: false` : c'est la fonction chat with documents de 5.2, désactivée comme le demandait votre réponse en 5.3.

Les éventuels scripts d'importation ou rapport de test ajoutés par Bob ne font pas partie de l'Agent sur l'instance.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 5.8 Les façons d'interagir avec les Agents Orchestrate

- Avec Bob, vous envoyez la question à l'Agent par l'intermédiaire de Bob : « Ask civic_info_agent: ... ». Bob vous montre la réponse et, comme il l'a vue, vous pouvez lui demander de corriger l'Agent dans votre message suivant. Les chapitres utilisent cette méthode pour tester chaque Agent.
- Dans watsonx Orchestrate, vous ouvrez votre instance dans le navigateur et tapez la question vous-même, dans la conversation qu'utilisent les habitants, qui parle à l'Agent déployé en Live, ou dans l'aperçu de la page Manage Agents, qui parle à l'Agent en Draft.

L'Agent existe dans deux environnements. Une question envoyée par l'intermédiaire de Bob atteint toujours l'Agent en Draft, celui que vous développez, et pour l'instant seul l'Agent en Draft cherche dans les documents, jusqu'à ce que vous déployiez en 5.9.

Bob a écrit les documents avec ses propres mots à partir de vos règles, les réponses aux questions ci-dessous doivent donc s'y trouver. Si une réponse diffère des règles, ouvrez le document : si la règle y figure, l'Agent l'a mal lue, et vous demandez à Bob de corriger l'Agent comme au chapitre 4 ; si elle manque, demandez à Bob de l'ajouter et d'importer de nouveau la Base de connaissances.

Avec Bob, posez les questions de la Vue d'ensemble, une par message :

```
Ask civic_info_agent: "Do I need a permit for a garden shed of 8 square metres?"
```

```
Ask civic_info_agent: "Which bin does a broken mirror go in?"
```

```
Ask civic_info_agent: "How loud can a party be after 10 pm on a Saturday?"
```

Lisez chaque réponse en ayant sous les yeux vos règles de 5.3. L'abri n'a pas besoin de permis, car il fait moins de 10 mètres carrés, à condition d'être isolé et de mesurer moins de 2,5 mètres de haut. Le miroir va, emballé, dans le bac gris. Un samedi, la musique ne doit pas être audible hors de la propriété après 23:00, et une dérogation pour une nuit peut être demandée cinq jours à l'avance. Vérifiez que chaque réponse nomme son document.

![Le panneau d'aperçu avec la réponse sur l'abri et le Building Permit Guide cité](images/ch05-preview-shed-answer.png)

Puis posez des questions comme le font les habitants :

- Pour tester un document et les faits ensemble, demandez « I want to build a 60 square metre extension. What does it cost, and who do I call? » Le tarif est de 300, et le contact est Permits and Planning.
- Pour une question qui contient un jour, demandez « Can the builders work on Sunday morning? » Jamais le dimanche.
- Pour une règle que les documents ne couvrent pas, demandez « Can I keep chickens in my garden? » L'Agent dit qu'il n'a pas cette information.

N'utilisez pas encore la conversation de la page d'accueil : elle répond avec les contacts et les horaires et sans documents, ou ne répond rien si vous n'avez jamais déployé. Ouvrez votre instance dans le navigateur, allez dans Manage Agents, sélectionnez Utopia city information, et tapez la question sur l'abri dans le panneau d'aperçu. La réponse doit correspondre à celle que Bob vous a montrée, avec son document cité.

## 5.9 Déployer la modification en Live

Mode : Agent, même conversation.

L'Agent qui cherche dans les documents existe en Draft. Si vous avez suivi le chapitre 4, l'Agent déployé en Live répond toujours à partir de ses vingt lignes de faits ; si vous avez importé l'Agent depuis le dossier walkthrough, rien n'est encore en Live. Dans les deux cas, déployez :

```
Deploy civic_info_agent from draft to live.
```

Bob indique que l'Agent est déployé et vous dit où les habitants peuvent le trouver : dans la conversation watsonx Orchestrate, sous son nom d'affichage, Utopia city information. Allez-y et posez la question sur l'abri ; la réponse est la même qu'en Draft. Sur la Developer Edition, sautez cette étape.

## 5.10 Résumé

L'Agent peut maintenant répondre à partir de la réglementation de la ville : une question sur un abri, un miroir ou une fête obtient la règle et le document dont elle provient. Les documents, la définition de la Base de connaissances et la modification de l'Agent sont des fichiers dans votre dossier de projet.

- Une Base de connaissances Orchestrate est un ensemble de documents que la plateforme indexe et dans lequel un Agent cherche. Elle est faite de fichiers, séparés des instructions de l'Agent. Un Agent qui répond de cette manière utilise la génération augmentée par la recherche, RAG.
- Après l'importation, la plateforme a besoin de quelques minutes pour indexer les documents. Un Agent ne peut utiliser la Base de connaissances que lorsque son état est prêt, l'Agent est donc importé après.
- Les instructions de l'Agent décident quand chercher et quoi dire lorsque les documents n'ont pas de réponse.
- Une Base de connaissances appartient à l'instance. Les modifications de ses documents prennent effet dès que la plateforme les a réindexés, pour l'Agent en Draft comme pour l'Agent en Live ; aucun déploiement n'est nécessaire.

L'Agent répond maintenant à partir de ce que la ville a mis par écrit, et toujours rien sur un habitant en particulier, comme l'approbation d'une demande de permis ou les jours de collecte d'une rue, car cette information se trouve dans les systèmes de la ville. Au chapitre 6, Bob donne à l'Agent ses premiers Outils Orchestrate, pour qu'une réponse puisse dépendre de la personne qui pose la question.
