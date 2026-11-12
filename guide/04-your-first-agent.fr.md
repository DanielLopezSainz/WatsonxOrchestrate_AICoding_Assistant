# Chapitre 4. Votre premier Agent Orchestrate

Niveau : débutant. Durée : environ 60 minutes. Prérequis : chapitre 2 terminé, chapitre 3 lu ou sauté selon son tableau de lecture.

## Vue d'ensemble

Imaginez que le lampadaire devant chez vous est éteint depuis une semaine. Il est sept heures du soir et les bureaux de la ville sont fermés. Vous ouvrez le site web de la ville d'Utopia et tapez : « The street light on my street has been out for a week. Who do I tell? » Quelques secondes plus tard, vous avez la réponse : le service Roads and Infrastructure, l'adresse à laquelle écrire, et les heures auxquelles quelqu'un répond au téléphone.

Cette réponse vient de l'Agent que vous créez dans ce chapitre, le premier Agent de CivicPulse. Il connaît trois services municipaux, ce que chacun traite et comment les joindre, et il sait quoi dire lorsqu'un habitant l'interroge sur quelque chose qu'on ne lui a jamais appris.

Vous créez l'Agent en trois étapes, une dans chacun des modes de Bob. Bob vous demande ce qu'il a besoin de savoir, écrit une conception que vous approuvez, construit l'Agent et le teste. Ensuite, vous cherchez une lacune dans ses faits : vous lui demandez un détail que les faits ne contiennent pas, lisez ce qu'il répond, et ajoutez le détail.

L'Agent est volontairement simple. Il se compose de :

- Un Agent Orchestrate, `civic_info_agent`, défini dans un seul fichier.
- Le modèle par défaut de l'instance.
- Une vingtaine de lignes d'instructions : les faits sur trois services, le ton, et quoi répondre lorsqu'une question sort de ces faits.
- Un message de bienvenue et deux suggestions de questions (starter prompts), affichés avant que l'habitant ne tape.

Il n'a ni Base de connaissances Orchestrate, ni Outils Orchestrate, ni Connexion Orchestrate à un autre système : ses instructions sont donc sa seule source. Les autres composants sont ajoutés à partir du chapitre 5 ; la section 1.2 les décrit.

Sautez ce chapitre si vous avez déjà créé un Agent dans watsonx Orchestrate avec Bob. Pour continuer avec le chapitre 5 sans construire l'Agent, envoyez à Bob cette instruction en mode Agent : `Import walkthroughs/ch04/agents/civic_info_agent.yaml into my instance.`

## 4.1 Avant de commencer

Ce chapitre exige la mise en place du chapitre 2, effectuée en entier :

- Le dépôt du guide cloné et ouvert dans Bob (chapitre 2, étape 1).
- L'extension watsonx Orchestrate ADK installée et l'espace de travail initialisé dans ce dossier (étapes 2 et 3).
- Le message de démarrage de Bob envoyé, pour que les skills Orchestrate soient chargés (étape 4).
- Un environnement actif dans l'Environment Manager, connecté à votre Developer Edition ou à votre tenant (étape 5).
- Les approbations réglées comme à l'étape 7 : Read et MCP activés, Edit et Execute désactivés. Avec Edit et Execute activés, Bob écrit des fichiers et exécute des commandes sans les demandes d'approbation que ce chapitre mentionne.

Vérifiez que Bob atteint votre instance. Ouvrez une nouvelle conversation en mode Ask et envoyez :

```
Which agents exist on my instance?
```

Sur une Developer Edition neuve, Bob liste deux Agents, DocProcessing et AskOrchestrate. Sur un tenant neuf, il liste AskOrchestrate. Si la réponse mentionne un répertoire de travail, un chemin interdit ou un problème d'authentification, voyez la section 2.8.

Si la liste contient déjà `civic_info_agent`, quelqu'un a déjà suivi ce chapitre sur l'instance. Demandez à Bob de le supprimer et de lister de nouveau les Agents. Bob demande votre approbation avant de le supprimer.

## 4.2 Mode Ask : comprendre la demande

Mode : Ask, dans une nouvelle conversation.

Ce prompt présente le projet à Bob pour la première fois. Son but est de confirmer que Bob a compris ce que vous voulez et de le laisser dire ce qu'il lui manque encore avant qu'un seul fichier n'existe. Il est bien plus facile de corriger un malentendu maintenant qu'une fois l'Agent construit.

Utilisez le mode Ask pour cette conversation : Bob peut lire votre projet et votre instance, et ne peut rien modifier.

Le prompt est un prompt structuré rédigé sous forme de texte suivi (chapitre 3, type 3). Il décrit l'Agent en termes simples : pour qui il est, le genre de question auquel il répond, d'où viennent ses connaissances, et ce qu'il ne doit pas faire. Il se termine en demandant à Bob ce qu'il a compris, ce dont il a besoin de votre part et ce qui existe déjà sur votre instance.

```
I would like to build an information agent for the residents of the City of
Utopia with watsonx Orchestrate. It should answer questions like "the street
light on my street has been out for a week, who do I tell?", "how do I apply
for a building permit?" and "when is the waste office open?". It answers from
a fixed set of facts about three city departments: Permits and Planning, Roads
and Infrastructure, and Waste and Recycling. It does not look anything up in
other systems and it does not create requests.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Bob examine d'abord votre instance, ce qui prend quelques secondes, pour que sa réponse décrive ce qui s'y trouve. La réponse contient généralement :

1. Un résumé de ce que Bob a compris. Comparez-le à ce que vous vouliez dire. S'il est faux, corrigez-le maintenant.
2. Une liste de ce qui existe déjà sur l'instance : les Agents, Outils, Bases de connaissances et Connexions, et si le nom du nouvel Agent est libre. Bob la lit sur l'instance.
3. Les questions auxquelles Bob a besoin de réponses avant de pouvoir écrire une conception, par exemple les faits pour chaque service, le format des réponses, quoi dire lorsqu'une question sort des faits, et le nom de l'Agent.

![La réponse de Bob au premier prompt : ce qu'il a compris, ce qui existe sur l'instance, ses questions](images/ch04-ask-answer.png)

Les questions de Bob varient d'une exécution à l'autre, mais elles se ramènent aux mêmes points : les faits, le ton, les limites de l'Agent et son nom. La réponse suivante les donne toutes à Bob d'un coup, vous pouvez donc l'utiliser quelle que soit la formulation de ses questions. Envoyez-la dans la même conversation.

```
Use these facts as they are.

Permits and Planning: permits@utopia.example, 555 0110, Monday to Friday 09:00
to 17:00. Building permit applications are submitted online at
https://services.utopia.example/permits.
Roads and Infrastructure: roads@utopia.example, 555 0120. Potholes, street
lights and damaged signs. Urgent hazards on a public road, such as a burst
water main or a fallen tree: 555 0199 at any time.
Waste and Recycling: waste@utopia.example, 555 0130, Monday to Friday 08:00 to
16:00. Bulky item collection is booked online at
https://services.utopia.example/bulky.

Answers: two or three sentences, plain language, always with the contact.
English only.
If a question is outside the three departments, say so and name the department
most likely to help. Never invent an answer.
Name the agent civic_info_agent, with the display name "Utopia city information".
Keep the facts in the agent's instructions. Do not use a knowledge base.
```

Bob confirme les réponses et peut proposer de passer en mode Agent et de créer l'Agent tout de suite. Ne changez pas encore de mode ; rien n'a été créé. L'étape suivante, en mode Plan, écrit la conception dans un fichier que vous approuvez.

## 4.3 Mode Plan : écrire la conception

Mode : Plan, dans la même conversation.

En mode Plan, Bob écrit un document de conception qui définit l'Agent.

Restez dans la même conversation, pour que Bob garde tout ce que vous lui avez dit, et passez en mode Plan. Le prompt tient en une ligne, une instruction (chapitre 3, type 2).

```
Write the design for this agent into design/civic-info-design.md.
```

Bob écrit le fichier après que vous avez approuvé la demande, et affiche un résumé. Ouvrez le fichier et lisez-le comme la spécification de ce que vous allez recevoir. La mise en page est au choix de Bob et diffère d'une exécution à l'autre. Le tableau liste ce que le fichier doit contenir.

![La demande d'écriture de design/civic-info-design.md, avec le bouton Approve](images/ch04-approve-design-write.png)

| Contenu | Ce qu'il faut vérifier |
|---|---|
| Le rôle de l'Agent | Il correspond à votre demande |
| L'Agent | Son nom, son nom d'affichage, son modèle, et le fait qu'il n'a ni Outils, ni Base de connaissances, ni collaborateurs |
| Les faits | Les trois services, avec les contacts, horaires et adresses exactement tels que vous les avez donnés |
| Les instructions | Le texte complet que l'Agent lira : les faits et les règles de réponse |
| Les questions de test | Chacune avec ce que contient une réponse correcte |

Le modèle et la description sont définis de la même manière pour chaque Agent de ce guide :

- Vous n'avez pas nommé de modèle, la conception utilise donc le modèle par défaut de l'instance. L'identifiant du modèle par défaut dépend de l'instance et de sa version ; sur l'instance utilisée pour préparer ce guide, c'est `groq/openai/gpt-oss-120b`.
- La description dit à quoi sert l'Agent, et les autres Agents et l'interface d'Orchestrate la lisent pour décider quand utiliser cet Agent. Les instructions disent comment l'Agent se comporte, et l'Agent lui-même les lit dans chaque conversation.

## 4.4 Approuver la conception

Mode : Plan, même conversation.

La conception est une proposition, et c'est le moment de la modifier. Modifier la conception prend un prompt ; modifier l'Agent après la construction signifie l'importer et le tester de nouveau.

Lors de notre exécution, la conception ne disait rien de ce que voit un habitant avant de taper une question. Vérifiez la vôtre et, si cela manque, demandez-le :

```
Add a welcome message and two starter prompts to the design: the street light
question and the building permit question.
```

Bob révise le fichier et attend de nouveau, avec un résumé de ce qu'il a modifié. Ne vous fiez pas au résumé : ouvrez la conception dans le File Explorer et lisez les nouvelles lignes. Le message de bienvenue doit nommer les trois services, pour qu'un habitant sache ce que couvre l'Agent avant de taper, et les deux suggestions de questions doivent être les deux questions que vous avez demandées.

Lorsque la conception dit ce que vous voulez dire, elle est approuvée. Il n'y a rien à envoyer : l'approbation est la première ligne du prompt de 4.6.

Les faits donnent des horaires d'ouverture pour deux services et aucun pour Roads and Infrastructure. La conception ne dit pas ce que l'Agent doit faire à ce sujet.

## 4.5 Les environnements Draft et Live

Une instance a deux environnements. Draft est l'environnement des créateurs : un Agent en Draft peut être modifié, testé et importé de nouveau aussi souvent que nécessaire. Seuls les créateurs qui travaillent sur l'instance peuvent le joindre, depuis la page Manage Agents, où un panneau d'aperçu permet de converser avec lui. Live est l'environnement des habitants : l'Agent déployé en Live est celui que les habitants trouvent dans la conversation de la page d'accueil de l'instance, et plus tard sur le site web de la ville.

Lorsque Bob importe l'Agent, ou l'importe de nouveau après une correction, il modifie l'Agent en Draft. L'Agent en Live ne change pas tant que vous ne déployez pas : une opération qui prend l'Agent tel qu'il est en Draft et le déploie en Live. D'ici là, les habitants continuent de parler au déploiement précédent, si bien que personne ne tombe sur un Agent en cours de réparation. Si un déploiement s'avère incorrect, l'annuler ramène l'Agent en Live à son déploiement précédent.

Tout ce que fait Bob dans les sections suivantes se passe en Draft : la construction importe l'Agent en Draft, les tests s'exécutent sur lui, et la correction de 4.9 le remplace. Déployer l'Agent en Live est une instruction à Bob à la fin de 4.9.

La Developer Edition n'a que l'environnement Draft : sa conversation affiche les Agents en Draft, et il n'est pas possible d'y déployer. Si vous utilisez la Developer Edition, sautez le déploiement à la fin de ce chapitre et des chapitres suivants.

## 4.6 Mode Agent : construire et tester

Mode : Agent, dans une nouvelle conversation.

Dans cette étape, Bob construit l'Agent à partir de la conception approuvée.

Ouvrez une nouvelle conversation avec le signe plus en haut du panneau de conversation, puis sélectionnez Agent dans la liste déroulante des modes. Ne passez pas en mode Agent dans la conversation que vous utilisiez jusqu'ici.

Dans la conversation en cours, Bob dispose de votre demande, de sa première proposition, des faits, peut-être d'un Agent complet qu'il a présenté dans la conversation avant que vous ne demandiez une conception, de la conception et de votre révision. Vous n'en avez approuvé qu'une partie. Si Bob construit là, tout cela est sous ses yeux, et Bob peut reprendre un détail de son premier jet au lieu de la conception approuvée. Dans une nouvelle conversation, Bob ne lit que le fichier de conception et construit ce que vous avez approuvé.

Pour un Agent aussi petit, la différence se voit rarement. À partir du chapitre 9, une conception couvre quatre Agents et la discussion qui la précède est longue. La documentation de Bob décrit la même pratique pour passer d'un plan à sa mise en œuvre.

Le prompt fait deux phrases : la première approuve la conception et la seconde lance la construction. Bob tire tout le reste du fichier de conception, que la mention @ lui dit de lire.

```
The design in @design/civic-info-design.md is approved. Build it.
```

Approuvez chaque demande au fur et à mesure. La construction prend une minute ou deux à Bob. Lors de notre exécution, Bob :

1. A lu la conception, puis l'un des skills Orchestrate chargés par le message de démarrage du chapitre 2, celui qui sait comment les Agents se construisent et se testent. Tout ce qui suit vient de la conception et de ce skill.
2. A écrit le fichier d'Agent `agents/civic_info_agent.yaml`, c'est-à-dire la conception mise sous la forme qu'accepte watsonx Orchestrate : le nom, le modèle, les instructions avec les faits, et le message de bienvenue et les suggestions de questions dans la structure exacte qu'exige la plateforme.
3. L'a importé. L'Agent existe alors sur l'instance, en Draft, où seuls les créateurs peuvent l'utiliser.
4. A envoyé les questions de la conception, le lampadaire, l'arbre tombé, le permis de construire, l'encombrant, la taxe foncière, et une de son cru, une seconde question dans la même conversation pour vérifier que l'Agent se souvient de la première. Il a rendu compte de chaque réponse avec son verdict ; tous les tests ont réussi.
5. A présenté un tableau des fichiers qu'il a écrits, et une liste de façons d'essayer l'Agent vous-même.

![La commande d'importation affichée par Bob en mode Agent, en attente d'approbation](images/ch04-approve-import-command.png)

## 4.7 Lire la définition

L'Agent a été créé dans watsonx Orchestrate. Ce que vous voyez dans Bob est son fichier de définition, `agents/civic_info_agent.yaml`, que Bob a écrit et importé. Avant Bob, les créateurs écrivaient ce fichier à la main ; désormais Bob l'écrit, et vous le lisez. Ouvrez-le dans le File Explorer. Le tableau liste les champs auxquels ce guide fait référence.

| Champ | Rôle |
|---|---|
| Name | L'identifiant de l'Agent : en minuscules, avec des tirets bas. Tout le reste désigne l'Agent par ce nom |
| Display name | Le nom que voient les utilisateurs |
| Description | À quoi sert l'Agent. Les autres Agents et l'interface d'Orchestrate la lisent |
| Instructions | Comment l'Agent se comporte et, dans ce chapitre, les faits qu'il connaît |
| Model | Le modèle de langage sur lequel l'Agent s'exécute |
| Kind | Le type d'Agent. Il vaut `native` pour chaque Agent de ce guide |
| Style | La stratégie de raisonnement de l'Agent. Le guide utilise celle que Bob choisit par défaut. Elle apparaît sous deux noms, `react_core` dans le fichier et `react_intrinsic` sur l'instance, qui désignent le même style |
| Tools, collaborators, Knowledge Base | Vides dans ce chapitre. Les chapitres 5, 6 et 9 les remplissent |
| Welcome message et starter prompts | Ce que voit un utilisateur avant de taper |

Le fichier peut contenir d'autres champs.

Enregistrez votre travail maintenant, comme le décrit la section 3.6 : `Commit everything I changed with a short message saying what was built.` Désormais, toute modification de ce fichier peut être annulée.

Comparez le fichier à la conception. Les deux peuvent différer. Lors de notre exécution, la conception donnait le nom d'affichage Utopia city information et le fichier l'omettait, si bien que l'Agent apparaissait sous son nom interne. La correction de 4.9 en tient compte.

## 4.8 Faites connaissance avec votre Agent

Mode : Agent, même conversation.

Ouvrez le panneau watsonx Orchestrate. Dans la section Explorer, placez le pointeur sur la ligne Agents, cliquez sur l'icône d'actualisation qui y apparaît, et dépliez Agents. `civic_info_agent` y figure, à côté des Agents qui se trouvaient déjà sur l'instance.

![L'Agent dans la page Manage Agents de watsonx Orchestrate, avec le panneau d'aperçu et la réponse sur le lampadaire](images/ch04-preview-panel.png)

Ne cliquez pas sur le nom de l'Agent. Un clic enregistre une copie de l'Agent depuis l'instance dans le dossier de projet et propose de remplacer le fichier que Bob a écrit, dans un format plus long avec tous les champs que l'instance conserve. Si vous cliquez par erreur, choisissez Cancel dans la boîte de dialogue. Si le fichier est remplacé, il devient une copie de l'Agent tel que l'instance le détient : l'Agent lui-même est inchangé, mais toute modification apportée au fichier et pas encore importée est perdue, et le fichier lu en 4.7 change de forme. La demande de restauration de la section 3.6 rétablit le fichier.

Maintenant, parlez-lui. Bob l'a testé avec les questions de la conception ; cette fois, les questions sont les vôtres. Posez-les par l'intermédiaire de Bob, une question par message :

```
Ask civic_info_agent: "My recycling bin was not collected this morning. Who do I contact?"
```

Les habitants n'écriront pas leurs questions aussi proprement que la conception. Essayez celles-ci :

- La même question, tapée à la hâte : « bin not collected today who do i call ».
- Une question qui concerne deux services : « I want to build a garden shed and I also need to get rid of the old one. Who do I contact? »
- Une question en pleine nuit : « There is water flooding the street from a broken pipe. It is 2 am. What do I do? »
- Une question hors de son périmètre : « What time does the public swimming pool open? »
- Une relance dans la même conversation, après la question sur le recyclage : « And what if it happens again next week? »

Lisez chaque réponse en ayant sous les yeux les faits de 4.2. Pour les trois premières, le bon service et son contact doivent y figurer, et la rue inondée doit recevoir la ligne d'urgence ; la piscine doit recevoir un refus poli avec une orientation vers le service le plus susceptible d'aider. La relance doit être traitée comme une question sur la collecte des déchets, avec le contact de Waste and Recycling, sans que l'Agent demande à quoi « it » fait référence.

Notez toute réponse qui contient quelque chose qui ne figure pas dans les faits.

Jusqu'à la fin de la section suivante, l'Agent n'existe qu'en Draft, où vous pouvez l'utiliser et où les habitants ne le peuvent pas.

## 4.9 Corriger une mauvaise réponse

Mode : Agent, même conversation.

Demandez maintenant à l'Agent quelque chose que ses faits ne contiennent pas :

```
Ask civic_info_agent: "What are the opening hours of Roads and Infrastructure?"
```

Les faits ne donnent pas d'horaires pour ce service. Examinez la réponse. Lors de notre exécution, l'Agent a répondu du lundi au vendredi de 09:00 à 17:00, qui sont les horaires de Permits and Planning : un modèle de langage a tendance à combler une lacune avec le contenu le plus plausible, et la règle « never invent an answer » se trouve à côté de la règle sur les questions hors des trois services, si bien que le modèle peut la lire comme limitée à celles-ci. Si votre Agent dit plutôt qu'il n'a pas d'horaires pour Roads and Infrastructure, il a fait mieux que le nôtre ; appliquez tout de même la correction ci-dessous, pour que les horaires figurent dans les faits.

Dites à Bob ce qui n'allait pas et comment l'Agent doit se comporter. Bob sait où l'Agent est défini ; vous n'avez pas besoin de nommer le fichier.

```
civic_info_agent gave opening hours for Roads and Infrastructure that are not
in its facts. The hours of Roads and Infrastructure are Monday to Friday 07:00
to 19:00. When a question asks for a detail that is not in the facts, the agent
must say that it does not have that information. Also give the agent the
display name "Utopia city information", as in the design. Import the agent
again and ask it the same question.
```

Bob modifie le fichier de définition et l'importe de nouveau avant de poser la question. Bob peut aussi ajouter les nouveaux horaires à la conception, pour que la conception et l'Agent concordent. L'Agent répond désormais avec les horaires. Importer un fichier portant le nom d'un Agent existant remplace cet Agent au lieu d'en créer un second.

Posez encore une question que les faits ne couvrent pas, par exemple « Who is the head of the Permits department? ». L'Agent doit maintenant dire qu'il n'a pas cette information et donner le contact du service.

**Déployer l'Agent en Live**

L'Agent est corrigé et testé, mais il n'existe qu'en Draft, les habitants ne peuvent donc pas le voir. Pour le déployer en Live, envoyez une instruction :

```
Deploy civic_info_agent from draft to live.
```

Bob exécute le déploiement et indique que l'Agent a été déployé. Ouvrez votre instance watsonx Orchestrate dans le navigateur : l'Agent se trouve maintenant dans la conversation de la page d'accueil, avec son message de bienvenue et ses deux suggestions de questions, pour toute personne qui a accès à l'instance. Sur la Developer Edition, sautez cette étape ; le déploiement n'y est pas disponible.

![La conversation watsonx Orchestrate après le déploiement : le message de bienvenue et les deux suggestions de questions](images/ch04-live-chat-welcome.png)

Désormais, l'Agent existe dans les deux environnements. La prochaine fois que vous demanderez à Bob de modifier l'Agent, la modification ira en Draft, et l'Agent déployé en Live continuera de répondre comme avant jusqu'à ce que vous déployiez de nouveau. Il en va de même pour les questions : lorsque vous demandez à Bob d'envoyer une question à l'Agent, elle atteint l'Agent en Draft, car l'opération qu'utilise Bob pour converser avec un Agent, `chat_with_agent` sur le serveur Orchestrate, est conçue pour Draft et n'a pas d'option pour viser Live. Pour parler à l'Agent déployé en Live, celui auquel parlent les habitants, utilisez la conversation de watsonx Orchestrate.

## 4.10 Résumé

Un habitant d'Utopia peut maintenant demander à qui signaler un lampadaire éteint et obtenir le bon service, avec son contact et ses horaires, auprès d'un Agent qui n'existait pas il y a une heure. Vous avez décrit l'Agent, approuvé une conception et corrigé une réponse ; Bob a écrit tout le reste. Cinq points de ce chapitre s'appliquent à chaque Agent Orchestrate qui suit :

- Un projet d'Agent passe par les trois modes de Bob : le mode Ask pour comprendre la demande, le mode Plan pour écrire la conception, le mode Agent pour construire et tester.
- Vous approuvez la conception avant que Bob ne construise, et tout ce que vous voulez voir construit doit figurer dans la conception.
- Un seul fichier définit un Agent Orchestrate. Importer le fichier crée l'Agent en Draft ; l'importer de nouveau remplace l'Agent.
- Les instructions sont tout ce que l'Agent sait, c'est donc là qu'une mauvaise réponse se corrige.
- Tant que vous ne déployez pas, l'Agent n'existe qu'en Draft. Déployer place l'Agent tel qu'il est en Draft dans Live, l'environnement que voient les utilisateurs.

Vous avez construit le premier Agent, l'avez testé, avez trouvé une lacune dans ses faits, l'avez corrigée et, sur un tenant, l'avez déployé en Live, en une heure environ et sans écrire de code. Chaque Agent Orchestrate du reste du guide se fait de la même manière, et seuls les composants changent.

L'Agent connaît vingt lignes de faits, et une ville en compte bien davantage. Peut-on construire un abri sans permis, et dans quel bac va un miroir cassé ? Quel volume sonore une fête peut-elle atteindre après dix heures du soir ? Les réponses se trouvent dans les guides et la réglementation de la ville, et aucune instruction d'Agent ne peut contenir de telles pages. Au chapitre 5, Bob donne ces documents à l'Agent sous la forme d'une Base de connaissances Orchestrate, et l'Agent y puise ses réponses en citant le document.
