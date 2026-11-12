# Chapitre 6. Ajouter des Outils Orchestrate

Niveau : débutant. Durée : environ 60 minutes. Prérequis : chapitre 5 terminé, ou son Agent et sa Base de connaissances importés depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre.

## Vue d'ensemble

Il y a trois semaines, vous avez déposé une demande de permis de construire. L'e-mail de confirmation indique un numéro, PP-2026-0412, et rien n'est arrivé depuis. Vous demandez à CivicPulse : « Where is my permit application PP-2026-0412? » L'Agent du chapitre 5 a la réglementation de la ville dans sa Base de connaissances. Il peut vous dire qu'une décision est rendue sous 30 jours, et rien de plus, car il n'a jamais vu votre demande. Votre dossier se trouve dans le système des permis de la ville, pas dans un document.

Chaque question à laquelle l'Agent du chapitre 5 pouvait répondre avait la même réponse pour tous les habitants : les horaires d'un service, la règle pour un abri. Les questions de ce chapitre demandent des réponses qui dépendent du dossier concerné : l'état d'une demande, la date d'une réparation, le jour de collecte d'une rue. Pour répondre, l'Agent consulte ce dossier dans le système de la ville au moment où la question est posée.

Un Outil Orchestrate est le moyen par lequel un Agent va le chercher. Dans ce chapitre, Bob écrit trois Outils Orchestrate pour la ville d'Utopia : un qui consulte une demande de permis par son numéro, un qui consulte un signalement de problème par son numéro, et un qui donne les jours de collecte d'une rue. Utopia n'a pas de système des permis, Bob écrit donc aussi les dossiers que lisent les Outils, quelques lignes dans un fichier pour chacun. Ensuite, Bob connecte les Outils à l'Agent, et l'Agent décide, question par question, quand en utiliser un.

L'Agent et sa Base de connaissances restent tels qu'au chapitre 5 ; les instructions gagnent un paragraphe.

Sautez ce chapitre si vous avez déjà donné un Outil Python à un Agent avec Bob. Pour continuer avec le chapitre 7 sans le construire, vérifiez d'abord que la Base de connaissances du chapitre 5 existe sur votre instance, puis envoyez à Bob ces instructions en mode Agent : `Import the three Python tools in walkthroughs/ch06/tools into my instance, each one packaged with its record file, then import walkthroughs/ch06/agents/civic_info_agent.yaml.`

## 6.1 Avant de commencer

- La mise en place du chapitre 2, complète.
- L'Agent `civic_info_agent` du chapitre 5 sur votre instance, en Draft, avec la Base de connaissances `city_regulations` rattachée. Si vous avez sauté le chapitre 5, importez les deux comme le décrit la Vue d'ensemble de ce chapitre.
- Une nouvelle conversation dans Bob pour ce chapitre.

Vérifiez que les deux sont là : en mode Ask, demandez `Which agents and knowledge bases exist on my instance?` et vérifiez que `civic_info_agent` et `city_regulations` figurent dans la liste.

## 6.2 Ce qu'est un Outil Orchestrate

Les instructions contiennent ce que l'Agent sait ; la Base de connaissances, ce que la ville a mis par écrit. Ni l'une ni l'autre ne contient l'état d'une demande de permis : cette information se trouve dans le système des permis, et elle appartient à un habitant. Un Outil Orchestrate est une fonction que l'Agent appelle pendant qu'il répond, pour obtenir une information ou agir.

L'Agent utilise tour à tour les parties suivantes d'un Outil Orchestrate.

| Partie | Ce que c'est | Ce qu'en fait l'Agent |
|---|---|---|
| La description | Une phrase qui dit ce que fait l'Outil et quand l'utiliser | La lit, avec la question, pour décider s'il appelle l'Outil |
| Les paramètres | Les valeurs dont l'Outil a besoin, chacune avec un nom et une description, par exemple un numéro de permis | Les trouve dans la question, ou les demande à l'habitant |
| Le résultat | Ce que renvoie l'Outil, par exemple le dossier d'une demande | Rédige la réponse à partir de lui |

Aucun prompt ne dit à l'Agent d'appeler un Outil pour une question donnée, pas plus qu'aucun ne lui dit de chercher dans la Base de connaissances : les instructions disent quand les Outils s'appliquent, et le modèle décide de chaque cas à partir de la question et des descriptions de ses Outils. « Where is my permit application PP-2026-0412? » correspond à la description de l'Outil des permis et contient un numéro de permis, l'Agent l'appelle donc avec ce numéro. « Where is my permit application? » correspond à la description mais ne contient pas de numéro, l'Agent le demande donc. Outre les instructions, la description et les noms des paramètres sont tout ce dont dispose l'Agent pour cette décision.

**Les types d'Outils Orchestrate**

| Type | Ce que c'est | Dans ce guide |
|---|---|---|
| Outil Python | Une fonction Python dans un fichier, envoyée sur l'instance et exécutée là | Ce chapitre |
| Outil OpenAPI | Une API REST existante, décrite par son fichier OpenAPI ; aucun code à écrire | L'alternative à un Outil Python lorsque l'API existe déjà |
| Boîte à outils Orchestrate | Un ensemble d'Outils servis par un serveur MCP, comme celui qu'utilise Bob pour parler à votre instance | Chapitre 8 |
| Flux Orchestrate | Une suite d'étapes comprenant des Outils et des Agents, que l'Agent appelle comme un seul Outil | Non construit dans ce guide |

Un Outil Python se compose d'une fonction, d'une description, de paramètres et d'un résultat, dans un seul fichier, que décrit la section 6.7.

**Les données de ce chapitre**

Dans une vraie ville, l'Outil des permis interrogerait le système des permis, par son API, avec un identifiant. La ville d'Utopia n'a pas de système des permis. Dans ce chapitre, chaque Outil lit ses dossiers dans un petit fichier que Bob écrit et envoie avec l'Outil : dix demandes, dix signalements, les jours de collecte de dix rues. L'Agent appelle chaque Outil comme il en appellerait un connecté à un vrai système.

**Lire le raisonnement de l'Agent**

Un Agent doté d'Outils fait des choix, et watsonx Orchestrate vous permet de les voir. Avec chaque réponse, l'Agent peut montrer les étapes qu'il a suivies : l'Outil qu'il a appelé, les valeurs qu'il a transmises, ce que l'Outil a renvoyé. Dans la conversation watsonx Orchestrate, les étapes se trouvent derrière un lien Show Reasoning à côté de la réponse ; par l'intermédiaire de Bob, vous les demandez avec les mots « with reasoning ». La définition de l'Agent a un réglage pour cela, `hide_reasoning`, qui vaut `false` pour `civic_info_agent` ; la section 6.8 montre comment lire les étapes.

## 6.3 Mode Ask : décrire les consultations

Mode : Ask, dans une nouvelle conversation.

Le prompt n'utilise pas le mot Tool : il décrit ce que demandent les habitants et où se trouvent les réponses, dit que la ville n'a pas de système à interroger, et laisse à Bob le choix du composant, qui doit être un Outil Python, comme le décrit 6.2.

```
I want civic_info_agent to answer questions about one resident's own record,
not only questions about rules and contacts. Residents ask things like "Where
is my permit application PP-2026-0412?", "Has my pothole report RQ-2026-1187
been scheduled?" and "Which day is the grey bin collected on Elm Street?". The
city keeps three kinds of records for this: building permit applications,
problem reports about roads, and the collection calendar by street, each one
found by its number or by the street name. The City of Utopia has no systems
to query: the records are fictional, and you will write them.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Dans la réponse de Bob, cherchez les points suivants :

- Dans ce qu'il a compris, Bob propose des fichiers de dossiers et des Outils Python qui les lisent, un par type de dossier. Bob a choisi le mot Tool sans qu'on le lui dise ; 6.2 explique pourquoi.
- Ce qu'il a trouvé sur l'instance : l'Agent, la Base de connaissances, et aucun Outil du projet.
- La ligne du chapitre 4 qui dit que l'Agent ne consulte rien dans d'autres systèmes. Bob peut signaler que cette ligne doit changer ; la construction de 6.6 la modifie.
- Ses questions : combien de dossiers, quels mots d'état, quels bacs, quoi dire lorsqu'un numéro est inconnu. Elles reçoivent une réponse ci-dessous.

Le second prompt crée les dossiers en toutes lettres : trois demandes, trois signalements et trois rues, avec des numéros et des dates fixes, pour que votre Agent donne les mêmes réponses que l'Agent de tous les autres lecteurs. Le reste du prompt tranche les décisions que Bob a demandées. Rien n'est encore créé.

```
These are my answers. Three Python tools: get_permit_status, which receives a
permit number and returns the application's address, type of work, status,
submission date and the date by which a decision is due; get_request_status,
which receives a request number and returns the report's street, type of
problem, status and scheduled date when there is one; and get_collection_days,
which receives a street name and returns the collection day of each bin, the
same every week. Each tool reads its records from a CSV file kept with the
tool, so that the file is uploaded with it.

Use these records as they are, and add seven more of your own to each file,
using only the status words that appear in these records. The bins are the four
of the waste sorting rules: grey, green, blue and yellow.

Permit applications. PP-2026-0412, 18 Elm Street, garden shed of 12 square
metres, status Under review, submitted 2026-09-12, decision due 2026-10-12.
PP-2026-0398, 7 Harbour Lane, two-storey extension, status Approved, submitted
2026-08-20, decided 2026-09-30. PP-2026-0433, 42 Mill Road, garage, status
Additional documents requested, submitted 2026-09-25, site plan missing.

Problem reports. RQ-2026-1187, Elm Street, pothole, status Scheduled, repair on
2026-10-09. RQ-2026-1203, Harbour Lane, street light out, status Closed, fixed
on 2026-10-01. RQ-2026-1210, Station Road, damaged sign, status Received.

Collection days. Elm Street: grey bin Monday, green bin Thursday, blue and
yellow bins Wednesday. Harbour Lane: grey Tuesday, green Friday, blue and
yellow Wednesday. Mill Road: grey Monday, green Thursday, blue and yellow
Friday.

The agent uses a tool for any question about one resident's application,
report or street. Any resident who gives a number sees the record; the agent
does not check who is asking. When a question gives no number or street, the
agent asks for it. When a number or street is unknown, the agent says that it has no
record under that number and gives the contact of the department. The agent
keeps its facts and its knowledge base; a question can need both a tool and a
document. The rule from chapter 4 that the agent does not look anything up in
other systems is replaced by these tools. Answers from a tool stay within
three sentences and end with the contact of the department, as before.
```

Vérifiez dans la réponse de Bob les points suivants :

- Les dossiers sous forme de tableaux, le code des trois Outils, le nouveau paragraphe des instructions. Bob peut même commencer comme s'il allait écrire les fichiers, et s'arrêter parce que le mode Ask ne le permet pas.
- Au-dessus de chaque Outil, Bob écrit une phrase qui le décrit. « Look up the status of a building permit application by its permit number » est ce que l'Agent lira au moment de décider.
- Bob vous invite à passer en mode Agent. Ne changez pas encore de mode ; rien n'a été créé. La conception que vous lisez et approuvez vient en 6.4.

## 6.4 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

La conception couvre trois Outils, trois fichiers de dossiers, une modification de l'Agent et une importation pour chaque Outil. Demandez à Bob de la mettre par écrit.

```
Write the design for this change into design/city-services-tools-design.md.
```

Bob demande l'approbation, écrit le fichier et le résume. Vérifiez que le fichier contient les éléments suivants :

| Contenu | Ce qu'il faut vérifier |
|---|---|
| Les trois Outils | Nom, paramètre, résultat, et la phrase qui le décrit à l'Agent. La phrase dit ce que l'Outil consulte et à partir de quoi : « by its permit number » plutôt que seulement « a permit » |
| Les dossiers | Trois fichiers CSV avec vos dossiers, à côté de l'Outil qui lit chacun d'eux |
| L'importation de chaque Outil | La conception dit que chaque Outil est envoyé sur l'instance avec son fichier de dossiers. Sans le fichier, l'Outil échoue sur l'instance |
| La modification de l'Agent | Les trois Outils rattachés ; les instructions disent quand utiliser un Outil, demander un numéro manquant, quoi dire lorsqu'un dossier est inconnu ; les faits et la Base de connaissances inchangés |
| L'ordre de construction | Les dossiers et les Outils d'abord, chaque Outil importé, puis l'Agent |
| Les tests | Au moins les trois questions du premier prompt de 6.3, chacune avec son dossier attendu |

## 6.5 Approuver la conception

Mode : Plan, même conversation.

Comparez la conception au tableau de 6.4. Si un Outil, un dossier ou un test manque, demandez à Bob de le modifier dans la même conversation.

La conception doit dire que chaque Outil est envoyé avec son fichier de dossiers. Si ce n'est pas le cas, envoyez :

```
Each tool must be uploaded to the instance together with its record file.
Change the design so that it says how.
```

Bob ajoute le mécanisme à la conception et l'explique : la commande d'importation désigne le dossier `tools` comme racine du paquet, et tout le dossier part sur l'instance avec l'Outil. Lorsque la conception dit ce que vous voulez dire, passez à 6.6.

## 6.6 Mode Agent : construire et tester

Mode : Agent, dans une nouvelle conversation.

```
The design in @design/city-services-tools-design.md is approved. Build it.
```

Cette construction comporte du code. Bob :

1. Écrit les trois fichiers de dossiers, un CSV par type de dossier.
2. Écrit les trois Outils, un fichier Python chacun, dans le dossier `tools`.
3. Importe les Outils. Chacun est empaqueté avec son fichier de dossiers et envoyé ; l'instance vérifie le code et la description, et Bob corrige un fichier si l'instance le refuse.
4. Met à jour l'Agent : rattache les trois Outils, complète les instructions et importe de nouveau l'Agent, remplaçant l'Agent en Draft.
5. Teste l'Agent avec les questions de la conception et rend compte.

Approuvez chaque demande au fur et à mesure. Le compte rendu de Bob peut dire que l'Agent est déployé. Il n'est importé qu'en Draft ; la section 6.9 le déploie en Live.

## 6.7 Ce que Bob a construit

Ouvrez le dossier `tools` dans le File Explorer. Il contient six fichiers : trois fichiers Python, un par Outil, `get_permit_status.py`, `get_request_status.py` et `get_collection_days.py`, et trois fichiers CSV avec les dossiers, `permits.csv`, `requests.csv` et `collection_calendar.csv`.

Ouvrez `get_permit_status.py` et trouvez la fonction `get_permit_status`, lors de notre exécution vers le bas du fichier. Autour de la fonction se trouvent les éléments suivants :

![tools/get_permit_status.py dans l'éditeur : la ligne @tool, la description et le paramètre](images/ch06-tool-file.png)

- La ligne `@tool` au-dessus de la fonction. Elle indique à watsonx Orchestrate que cette fonction est un Outil.
- Juste sous le nom de la fonction, le texte entre triples guillemets. C'est la description : une phrase sur ce que fait l'Outil, une ligne sur le paramètre, une ligne sur le résultat. Ce sont les mots que lit l'Agent lorsqu'il décide d'appeler ou non l'Outil.
- `permit_number`, le paramètre. L'Agent doit en trouver la valeur dans la question de l'habitant avant de pouvoir appeler l'Outil.

Le reste du fichier ouvre `permits.csv`, trouve la ligne qui porte ce numéro et la renvoie.

`permits.csv` contient une ligne par demande. Trouvez la ligne de PP-2026-0412, la demande de la Vue d'ensemble : 18 Elm Street, abri de jardin, en cours d'examen, décision attendue le 2026-10-12.

Ouvrez `agents/civic_info_agent.yaml`. Vers le bas, sous `tools`, figurent les noms des trois Outils. Dans les instructions, une nouvelle section dit quand appeler chaque Outil, quoi demander lorsque le numéro manque, et quoi dire lorsqu'il n'y a pas de dossier. La ligne du chapitre 4 qui interdisait toute consultation autorise désormais les trois Outils. Les faits et la Base de connaissances sont inchangés. Bob a pu ajouter des suggestions de questions pour les nouvelles questions.

Le dossier peut aussi contenir un fichier requirements, qui nomme les bibliothèques Python dont ont besoin les Outils et qui est envoyé avec eux, et un rapport de test, que Bob a écrit pour lui-même. Ni l'un ni l'autre ne fait partie de l'Agent.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 6.8 Essayez, et lisez le raisonnement

Posez à l'Agent les trois questions du premier prompt de 6.3, par l'intermédiaire de Bob ou dans le panneau d'aperçu de watsonx Orchestrate. Par l'intermédiaire de Bob, commencez chaque message par `Ask civic_info_agent:`.

```
Where is my permit application PP-2026-0412?
```

```
Has my pothole report RQ-2026-1187 been scheduled?
```

```
Which day is the grey bin collected on Elm Street?
```

Les réponses sont, dans l'ordre : en cours d'examen avec une décision attendue le 12 octobre, une réparation prévue le 9 octobre, et lundi. Chaque réponse se termine par le contact du service, parce que les instructions le demandent.

Essayez ensuite des questions qui testent les limites des Outils :

- Omettez le numéro, dans une nouvelle conversation pour que l'Agent ne réutilise pas celui ci-dessus : « Where is my permit application? » L'Agent le demande.
- Utilisez un numéro qui n'existe pas : « Where is my permit application PP-2026-9999? » L'Agent dit qu'il n'a pas de dossier sous ce numéro et donne le contact de Permits and Planning.
- Demandez un Outil et un document : « My application PP-2026-0412 is for a shed. Can I start building while I wait? » La réponse dit que les travaux ne doivent pas commencer avant la décision, d'après le Building Permit Guide. Gardez cette question pour la partie suivante.
- Nommez une rue sans qu'une consultation soit nécessaire : « The grey bin on Elm Street was not collected today. Who do I call? » L'Agent répond avec le contact de Waste and Recycling et n'appelle pas l'Outil du calendrier, car la question n'a pas besoin d'un jour de collecte.

Pour lire comment l'Agent y est parvenu, posez de nouveau la première question par l'intermédiaire de Bob, avec deux mots de plus :

```
Ask civic_info_agent, with reasoning: "Where is my permit application PP-2026-0412?"
```

Bob affiche maintenant les étapes avec la réponse : l'Agent a appelé `get_permit_status` avec le numéro de permis `PP-2026-0412`, l'Outil a renvoyé le dossier de `permits.csv`, et l'Agent a rédigé la réponse à partir de lui. Dans le panneau d'aperçu de watsonx Orchestrate, chaque réponse a à côté d'elle un lien Show Reasoning, qui ouvre les mêmes étapes : l'Outil, son entrée, sa sortie.

Ensuite, posez la question sur l'abri avec le raisonnement. La Base de connaissances apparaît dans les étapes comme un Outil nommé `city_regulations`, avec la requête que l'Agent lui a envoyée et les passages qu'il a reçus en retour. L'Agent peut répondre à cette question par deux chemins, le dossier et le guide, et les étapes montrent lequel il a pris : lors des essais, il a utilisé les deux sources dans une exécution et le guide seul dans une autre, et les deux réponses étaient correctes.

Lorsqu'un Agent doté d'Outils répond mal, ouvrez ses étapes de raisonnement. Elles montrent quel Outil a été appelé et avec quelles valeurs, ce qui réduit la recherche : un mauvais Outil met en cause les descriptions des Outils, une mauvaise valeur les descriptions des paramètres, et l'absence d'appel les instructions. Dites à Bob ce que vous avez trouvé, en une phrase, comme en 4.9.

![Le raisonnement d'une réponse dans le panneau d'aperçu : l'appel à get_permit_status avec son entrée et sa sortie](images/ch06-reasoning-tool-call.png)

## 6.9 Déployer la modification en Live

Mode : Agent, même conversation.

Sur la Developer Edition, sautez cette section. Tant que vous ne déployez pas, l'Agent en Live répond toujours qu'une décision est rendue sous 30 jours, ou n'existe pas si vous avez importé le chapitre 5 depuis le dossier walkthrough, car seul l'Agent en Draft a les Outils. Envoyez de nouveau l'instruction de déploiement :

```
Deploy civic_info_agent from draft to live.
```

Bob confirme le déploiement. Allez dans la conversation watsonx Orchestrate et posez la question sur PP-2026-0412 : l'habitant de la Vue d'ensemble obtient maintenant l'état de sa demande.

## 6.10 Résumé

L'Agent donne maintenant des réponses qui dépendent du dossier concerné : l'état d'une demande, la date d'une réparation, le jour de collecte d'une rue. Vous avez approuvé la conception et fourni les dossiers ; les Outils, les dossiers et les nouvelles instructions sont des fichiers dans votre dossier de projet, et vous avez lu le raisonnement de l'Agent.

- Un Outil Orchestrate est une fonction que l'Agent appelle pendant qu'il répond. L'Agent décide quand l'appeler, à partir de la description de l'Outil et de la question.
- La description et les descriptions des paramètres sont écrites pour l'Agent. L'Agent décide à partir d'elles, c'est donc le premier endroit où regarder lorsqu'il décide mal.
- Une réponse peut combiner les sources : un Outil pour le dossier de l'habitant, la Base de connaissances pour la règle, les instructions pour le contact.
- Le raisonnement de l'Agent montre les étapes entre la question et la réponse, appels d'Outils compris. Demandez-le à Bob avec les mots « with reasoning », ou ouvrez Show Reasoning à côté d'une réponse dans watsonx Orchestrate.

Aucun des trois Outils ne crée ni ne modifie de dossier. Le chapitre 7 ajoute un Outil qui crée un signalement de problème par l'API du centre d'appels 311 de la ville, et présente la Connexion Orchestrate, l'asset où sont conservés les identifiants d'un Outil pour qu'ils n'apparaissent jamais dans le code ni dans git.
