# Chapitre 10. CivicPulse sur WhatsApp : le Canal Orchestrate

Niveau : intermédiaire. Durée : environ 45 minutes. Prérequis : chapitre 9 terminé, ou ses quatre Agents importés depuis le dossier walkthrough comme l'indique la Vue d'ensemble de ce chapitre, et déployés en Live.

## Vue d'ensemble

Samedi matin à la salle de sport. Un haltère vous glisse des mains, et le miroir derrière le rack tombe en morceaux. Le gérant arrive avec un balai, regarde les morceaux, vous regarde, et dit que le conteneur à verre dehors est plein de bouteilles et que personne ne lui a jamais dit où va un miroir. Il a l'air en colère, et vous feriez bien d'avoir une réponse. Sur votre téléphone, vous avez le contact WhatsApp de la ville d'Utopia. Vous envoyez un message WhatsApp : « Does a broken mirror go in the glass bin? » Quelques secondes plus tard, vous avez la réponse. Vous n'avez pas eu besoin d'appeler le centre d'appels 311, ni même de vous connecter au site web de la ville. Un Canal Orchestrate a sauvé votre abonnement à la salle.

Dans ce chapitre, l'Agent d'accueil du chapitre 9 devient joignable sur WhatsApp. Bob crée pour lui un Canal Orchestrate, et Twilio, le service de téléphonie qui achemine les messages, relie WhatsApp à l'Agent.

Pour utiliser les Agents Orchestrate, vous n'êtes pas limité à une page de chatbot standard : un Canal Orchestrate relie un Agent à différents services de messagerie comme WhatsApp, SMS, Slack, Teams...

Ce chapitre exige une instance Orchestrate : sur la Developer Edition, l'ADK refuse de créer un Canal, lisez donc le chapitre sans l'exécuter. Aucun chapitre ultérieur n'en dépend.

## 10.1 Avant de commencer

- La mise en place du chapitre 2, complète, avec votre environnement actif dans l'Environment Manager et le serveur Orchestrate connecté dans l'onglet MCP de Bob. Un environnement activé dure deux heures (section 2.4), et un serveur qui apparaît déconnecté se redémarre depuis l'onglet (section 2.8).
- Les quatre Agents du chapitre 9 déployés en Live : `civic_info_agent`, `permits_agent`, `roads_agent` et `waste_agent`. Si vous les avez importés depuis le dossier walkthrough, déployez-les comme en section 9.9.
- Un téléphone avec WhatsApp.
- Un compte Twilio, créé en 10.3. L'essai gratuit suffit : il ne demande pas de carte de paiement et inclut le numéro de test qu'utilise ce chapitre.
- Une nouvelle conversation dans Bob pour ce chapitre.

Pour vérifier que l'Agent du chapitre 9 est en Live, demandez dans la conversation watsonx Orchestrate : `There is a pothole at 7 harbour ln, and which day is the green bin collected there?`. La réponse contient un numéro de demande et un jour de collecte.

## 10.2 Ce qu'est un Canal Orchestrate

Un Canal Orchestrate relie un Agent à un service de messagerie, à un site web ou à une plateforme de centre de contact. L'Agent que vous avez créé ne change pas ; le Canal reçoit chaque message du service, le transmet à l'Agent et renvoie la réponse par le même chemin.

Un Agent peut avoir plusieurs Canaux, un de chaque type : le même Agent peut répondre aux habitants sur WhatsApp, aux visiteurs du site web, et aux employés dans Slack ou Teams.

**Comment circule un message**

Lorsque Bob crée un Canal, la plateforme lui attribue une URL d'événements (event URL), une adresse sur l'instance qui appartient à ce Canal. Le service extérieur, ici Twilio, est configuré pour envoyer chaque message entrant à cette adresse, et la plateforme exécute l'Agent et renvoie la réponse à Twilio, qui la remet au téléphone. Un Canal détient les identifiants du service extérieur, ici les deux valeurs de Twilio, pour que la plateforme puisse envoyer les réponses par son intermédiaire.

**Draft et Live**

Un Canal est rattaché à un Agent dans un environnement. Un Canal sur l'Agent en Draft sert aux tests des créateurs ; un Canal sur l'Agent en Live sert aux habitants. Ce sont deux assets distincts avec des URL d'événements distinctes. Ce chapitre crée le Canal en Live parce que le chapitre 9 y a déployé l'Agent, et qu'un test depuis votre téléphone suit alors le chemin qu'empruntent les habitants.

**Twilio et son numéro de test**

Twilio est un service qu'utilisent les entreprises pour envoyer et recevoir des SMS et des messages WhatsApp depuis leurs applications. Un numéro professionnel sur WhatsApp exige un compte professionnel approuvé par Meta ; pour le développement, Twilio fournit un numéro de test partagé, le Sandbox, qu'un téléphone rejoint en lui envoyant un code. Ce chapitre utilise le Sandbox. Ses limites : un téléphone reste inscrit trois jours et doit ensuite renvoyer le code ; un compte d'essai dure 30 jours et inclut 100 messages WhatsApp ; les messages ne peuvent être échangés qu'avec des téléphones inscrits. Pour le vrai numéro de la ville, la ville demande un compte WhatsApp professionnel par l'intermédiaire de Twilio, et le Canal reste le même.

**Où vous l'utiliserez**

Un Canal rend un Agent disponible en dehors de watsonx Orchestrate. Les Agents que vous construirez après ce guide répondront aux employés dans Slack ou Teams et aux clients sur WhatsApp, avec la même définition que celle que vous testez dans la conversation Orchestrate. Pour chaque nouveau Canal, vous configurez un compte et une adresse sur le service extérieur et, côté Orchestrate, vous exécutez une commande.

IMPORTANT : un Canal détient des identifiants, comme une Connexion. Les deux valeurs de Twilio vont dans `.env` comme au chapitre 7 et atteignent l'instance par la commande qu'exécute Bob, jamais par la conversation ; le seul fichier qui contient l'Auth Token est `.env`, que git ignore.

## 10.3 Créer le compte Twilio et rejoindre le numéro de test

L'Agent Orchestrate que vous avez créé dans les chapitres précédents sera joignable par WhatsApp. Pour le test, vous utilisez votre propre téléphone : un compte Twilio gratuit, créé avec votre numéro de téléphone, permet à votre WhatsApp de parler à l'Agent. Créez le compte comme décrit ci-dessous. Vous faites cette section à la main, dans la console de Twilio et sur votre téléphone, et Bob prend le relais en 10.4.

1. Créez un compte gratuit sur twilio.com. Twilio demande une adresse e-mail, puis votre numéro de téléphone, qu'il vérifie par SMS. Twilio ne demande pas de carte de paiement. Répondez comme vous le souhaitez aux questions de l'inscription.
2. Dans la console, depuis l'Account Dashboard, ouvrez l'onglet **Develop** du panneau de gauche, puis **Messaging**, puis **Try it out**, puis **Send a WhatsApp message**. La page a deux onglets. Le premier, **Sandbox**, affiche le numéro de test de Twilio, `+1 415 523 8886`, votre code d'inscription, `join` suivi de deux mots, et un QR code.

![L'onglet Sandbox de Twilio : le numéro de test, le code d'inscription et le QR code](images/ch10-twilio-sandbox.png)

3. Scannez le QR code avec votre téléphone, ou ouvrez WhatsApp et envoyez le code d'inscription au numéro de test. Utilisez le téléphone dont vous avez donné le numéro à l'inscription : un compte d'essai n'échange de messages qu'avec des numéros vérifiés, et celui-ci l'est. Twilio répond dans WhatsApp que tout est prêt. Votre numéro apparaît alors sous Sandbox Participants dans le second onglet de la page.

**Les deux valeurs dont a besoin le Canal**

Le Canal envoie à Twilio deux valeurs : l'**Account SID** et l'**Auth Token**. Vous les trouvez sur la page d'accueil de Twilio, Console, sous Account Info, et les ajoutez à `.env` dans votre dossier de projet comme ci-dessous :

```
WO_INSTANCE=<the URL of your instance>
WO_API_KEY=<the API key of your instance>
UTOPIA_311_API_KEY=<the value from chapter 7>
TWILIO_ACCOUNT_SID=<the Account SID, which starts with AC>
TWILIO_AUTH_TOKEN=<the Auth Token>
```

## 10.4 Mode Ask : décrire le Canal

Mode : Ask, dans une nouvelle conversation.

Utilisez une structure similaire pour tout prompt que vous écrirez à l'avenir pour créer un Canal WhatsApp. Ce prompt donne à Bob les cinq éléments requis décrits ci-dessous et mentionne l'ADK. Il faut aussi ajouter une instruction « aucun numéro nécessaire » ; sinon Bob tentera d'en obtenir un. Enfin, nommez la commande de l'ADK, `orchestrate channels create`.

Un Canal Twilio WhatsApp a besoin de :

- L'asset Orchestrate nommé, comme au chapitre 8 : un Canal de type Twilio WhatsApp, le type tel que l'ADK le liste.
- L'Agent et l'environnement : `civic_info_agent` en Live.
- Un nom pour le Canal.
- Les deux valeurs de Twilio, l'Account SID et l'Auth Token, dans `.env`.
- Aucun numéro de téléphone : le numéro est celui de Twilio.

Un Canal se crée avec une seule commande de l'ADK qui prend les deux valeurs dans le fichier `.env`.

```
I want to add an Orchestrate channel of type Twilio WhatsApp to
civic_info_agent. The city uses Twilio; the account SID and the auth token are
in .env as TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. A Twilio WhatsApp channel
needs only these two values, no sender number. The channel is named CivicPulse
WhatsApp and is created on civic_info_agent in live with the command line of
the ADK, orchestrate channels create, run in the shell with .env loaded so
that the two values are read from the environment variables; do not use the
channel operation of the Orchestrate server, which would need the values in
the chat. The agent is deployed in live and must not change.

Tell me what you understood, what you need to know from me, and what already
exists on my instance.
```

Points à vérifier dans la réponse de Bob :

- Bob a compris un Canal de type Twilio WhatsApp sur `civic_info_agent` dans l'environnement Live, créé avec `orchestrate channels create` dans le shell et les deux valeurs de `.env`.
- Bob trouve sur l'instance les quatre Agents du chapitre 9 et aucun Canal sur aucun d'eux.
- Bob affiche la commande qu'il exécutera, avec `--field account_sid=$TWILIO_ACCOUNT_SID` et `--field twilio_authentication_token=$TWILIO_AUTH_TOKEN`, et demande si vous l'exécutez vous-même ou s'il l'exécute en mode Agent. La section 10.5 répond à cette question. Si Bob demande une description pour le Canal, il peut la choisir lui-même.

## 10.5 Mode Agent : créer le Canal

Mode : Agent, dans la même conversation qu'en 10.4. N'ouvrez pas de nouvelle conversation : la réponse de Bob en 10.4 est le contexte de cette étape.

Dans les chapitres précédents, Bob écrivait une conception que vous approuviez, et le prompt de construction tenait en une ligne. Un Canal est trop petit pour cela : une seule commande le crée. Ce chapitre saute donc le mode Plan. Il passe du mode Ask au mode Agent dans la même conversation, où Bob garde ce qu'il a trouvé en 10.4, et il utilise le prompt structuré du chapitre 3, celui en six parties. Chaque partie répond à une question que Bob trancherait sinon seul :

- Goal : ce qui doit exister lorsque Bob a terminé.
- Context : les fichiers et l'environnement avec lesquels Bob travaille.
- Constraints : la commande à utiliser, les deux champs, aucun numéro d'expéditeur, rien d'affiché dans la conversation, l'Agent inchangé.
- Deliverable : ce que Bob doit vous montrer à la fin, ici l'URL d'événements.
- Verify : comment Bob prouve que le Canal existe, la partie de l'objectif que Bob peut vérifier ; la partie de Twilio est en 10.7 et le test en 10.8. La réponse de Bob se termine alors par cette vérification.
- Stop : quand Bob doit vous demander au lieu de continuer.

Pour un autre Canal WhatsApp, gardez la partie Constraints telle quelle et demandez dans la partie Verify la liste des Canaux de l'Agent.

Restez dans la conversation de 10.4, passez en mode Agent et envoyez :

```
Goal: residents reach civic_info_agent on WhatsApp through Twilio.
Context: the Twilio account SID and auth token are in @.env as
  TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN. The agent is deployed in live.
Constraints: create one channel of type twilio_whatsapp, named CivicPulse
  WhatsApp, with the description "Residents reach CivicPulse on WhatsApp.",
  on civic_info_agent in the live environment, with the command
  line of the ADK, orchestrate channels create, run in the shell with .env
  loaded so that the two values are read from the environment variables. Do
  not use the channel operation of the Orchestrate server. The channel has two
  fields, the account SID and the auth token; no sender number is needed. No
  value is written in a file or shown in the chat. Change nothing in the
  agent. Add the command to the import script and the channel's deletion to
  the delete script.
Deliverable: the channel created on the instance, and the event URL that the
  platform returned, quoted in your answer.
Verify: list the channels of civic_info_agent in live and show that CivicPulse
  WhatsApp is there.
Stop: if the command returns an error, show me its exact text and wait.
```

Approuvez chaque demande au fur et à mesure. Bob exécute la commande, indique l'URL d'événements, et termine par la liste des Canaux de l'Agent en Live : une entrée, CivicPulse WhatsApp, avec son identifiant et sa date de création.

L'URL d'événements, l'adresse de ce Canal sur votre instance, nomme votre tenant, l'Agent, l'environnement, le type de Canal et l'identifiant du Canal, et se termine par `/events`. Twilio envoie à cette adresse chaque message WhatsApp qu'un téléphone inscrit envoie au numéro de test, et la plateforme répond par elle. L'URL est le seul lien entre Twilio et votre Agent ; la section 10.7 la colle dans Twilio. Copiez-la depuis la réponse de Bob.

## 10.6 Examiner le Canal avec Bob

Mode : Ask, même conversation.

Avant de commencer les tests, exécutez ces trois prompts avec Bob pour obtenir des informations sur le Canal :

```
List the channels of civic_info_agent in live and in draft.
```

Un Canal en Live, CivicPulse WhatsApp, avec son identifiant et sa date de création ; aucun en Draft.

```
Show me the details of the channel CivicPulse WhatsApp of civic_info_agent in live, including its event URL.
```

Bob affiche l'enregistrement que la plateforme conserve pour le Canal : son type, son nom et sa description, son propre identifiant, et les identifiants de l'Agent et de l'environnement auxquels il appartient. L'Account SID y figure, en tant qu'identifiant. L'Auth Token apparaît masqué : la plateforme ne renvoie jamais un secret, et l'exportation du prompt suivant l'affiche à null. L'enregistrement n'inclut pas l'URL d'événements, que la plateforme affiche une seule fois, à la création du Canal, et ne conserve pas. Bob la reconstitue à partir des identifiants de l'enregistrement, dans l'ordre donné en 10.5. Si vous perdez un jour l'URL, cette question vous la rend.

Le troisième prompt exporte le Canal dans un fichier du projet. Un Canal créé par une commande n'a pas de fichier à lui ; l'exportation lui en donne un. Ce fichier est utile lorsque vous devez :

- Recréer le Canal ailleurs : sur une seconde instance, par exemple l'instance de production de la ville après une instance de test, ou sur l'Agent en Draft pour tester une modification avant que les habitants ne la voient. Le fichier dit quoi recréer, le type, le nom et la description ; la commande du script d'importation le recrée, avec le jeton du `.env` de ce projet.
- Garder une trace de ce qui est sur l'instance, dans le projet et sous git, comme les définitions d'Agents. Lorsque quelqu'un modifie le Canal dans l'interface, une nouvelle exportation montre la différence.
- Voir ce que l'instance renvoie pour un Canal qui détient des identifiants.

```
Export the channel CivicPulse WhatsApp of civic_info_agent in live to exports/whatsapp-channel.yaml and show me the file.
```

Un fichier avec le type, le nom, la description, l'Account SID, un réglage de retour d'expérience (`enable_feedback: false`), et `twilio_authentication_token: null`. L'instance renvoie l'Account SID mais pas le secret. Un fichier YAML ne peut pas lire `.env` et le jeton ne doit jamais y être tapé, le fichier n'est donc pas importé tel quel ; la commande du script d'importation recrée le Canal à partir des mêmes valeurs.

## 10.7 Indiquer à Twilio où envoyer les messages

Configurez Twilio pour qu'il envoie les messages à l'URL d'événements vue en 10.5.

1. Dans la console de Twilio, depuis l'Account Dashboard, ouvrez l'onglet **Develop** du panneau de gauche, puis **Messaging**, puis **Try it out**, puis **Send a WhatsApp message**, et cliquez sur le second onglet, **Sandbox settings**.
2. Dans le champ **When a message comes in**, remplacez l'adresse qu'y a mise Twilio (sa propre réponse de démonstration) par l'URL d'événements de la réponse de Bob. Laissez la méthode sur **POST**. Laissez **Status callback URL** vide.
3. Cliquez sur **Save**. Le réglage n'est pas appliqué tant que vous n'avez pas cliqué sur Save.

![L'onglet Sandbox settings avec l'URL d'événements dans le champ et le bouton Save](images/ch10-twilio-sandbox-settings.png)

## 10.8 Essayez

Dans WhatsApp sur votre téléphone, dans la conversation avec le numéro de test, envoyez :

```
Does a broken mirror go in the glass bin?
```

La réponse arrive en quelques secondes, d'après les Waste Sorting Rules : un miroir cassé ne va pas dans le conteneur à verre, avec le contact de Waste and Recycling. Gardez ensuite le téléphone en main : tout ce que les Agents ont appris dans les chapitres précédents répond maintenant sur WhatsApp. Envoyez ces messages, dans n'importe quel ordre :

![La conversation WhatsApp sur le téléphone : la question et la réponse de CivicPulse](images/ch10-whatsapp-conversation.png)

- `What are the quiet hours?` L'Agent d'accueil répond lui-même, d'après la Noise Ordinance.
- `Which day is the green bin collected at 18 elm st?` L'adresse telle que vous la taperiez sur un téléphone ; l'Address Registry du chapitre 8 la corrige et le service Waste and Recycling donne le jour.
- `Where is my permit application PP-2026-0412?` Le service Permits and Planning lit le dossier du chapitre 6 : en cours d'examen.
- `There is a pothole at 7 harbour ln.` Un signalement au centre d'appels 311 du chapitre 7, et un numéro de demande en retour.
- `Which streets are in the Old Town district?` De nouveau l'Address Registry : Mill Road, High Street, Station Road.
- `Do I need a permit for a garden shed of 12 square metres?` Le Building Permit Guide, par l'intermédiaire du service Permits and Planning : au-delà de 10 mètres carrés, un permis est requis. La réponse peut arriver en deux messages, le second, « How do we know? », nommant le document ; c'est la citation de la plateforme, que la conversation affiche en note de bas de page et WhatsApp sous forme de message.
- `When does the swimming pool open?` Le refus du chapitre 9 : la question sort des trois services, l'Agent nomme donc un bureau qui pourrait aider et n'invente aucun contact.

WhatsApp n'affiche que les réponses. Pour voir le raisonnement, quel Outil a été appelé et quel service a répondu, posez la même question par l'intermédiaire de Bob, avec `Ask civic_info_agent:` devant et la demande de raisonnement. L'opération de conversation de Bob atteint l'Agent en Draft. Rien n'a changé en Draft depuis le déploiement du chapitre 9, le raisonnement obtenu par Bob montre donc quel service et quel Outil répondent à cette question ; les étapes d'une seconde exécution peuvent différer en détail de la première.

Si aucune réponse n'arrive, les journaux de Twilio montrent où le message s'est arrêté. Dans la console, **Monitor**, puis **Logs**, puis **Messaging**. Si votre message n'est pas listé, Twilio ne l'a pas reçu. La raison habituelle est que votre téléphone n'est plus inscrit, ce qui arrive au bout de trois jours ; renvoyez alors le code d'inscription. Si le message est listé avec une erreur 11200, Twilio a appelé l'URL d'événements et n'a pas obtenu de réponse valide. Une cause possible est une URL qui n'appartient plus à un Canal de l'instance, par exemple après qu'un Canal a été supprimé et recréé. Rechargez la page Sandbox settings, collez l'URL de la réponse de Bob, cliquez sur Save, et rechargez la page pour vérifier qu'elle est conservée. Pour confirmer que le Canal existe, demandez à Bob `List the channels of civic_info_agent in live.`.

## 10.9 Ce que Bob a construit

- L'instance contient un Canal Orchestrate, CivicPulse WhatsApp, de type Twilio WhatsApp, rattaché à `civic_info_agent` en Live. Il détient les deux valeurs de Twilio. L'Agent est inchangé.
- Le projet contient une commande dans le script d'importation, celle qui crée le Canal avec les deux valeurs lues dans `.env` ; une commande dans le script de suppression, placée avant la suppression de l'Agent ; et `exports/whatsapp-channel.yaml`, l'exportation de 10.6, avec le jeton vide.
- L'onglet MCP de Bob et les fichiers d'Agents sont inchangés, car un Canal est rattaché à un Agent de l'extérieur.

Le Canal appartient à l'environnement Live de l'Agent. Lorsqu'un chapitre ultérieur modifie l'Agent en Draft et le déploie de nouveau, le Canal reste en place et les habitants sur WhatsApp obtiennent la nouvelle version.

Enregistrez votre travail : `Commit everything I changed with a short message saying what was built.`

## 10.10 Résumé

L'Agent d'Utopia est maintenant joignable depuis WhatsApp. Prenez ce chapitre comme guide pas à pas lorsque vous réaliserez des mises en œuvre similaires : les éléments à inclure dans les prompts, la liste des faits à vérifier et à tester, et les questions à poser à Bob sur le résultat.

- Un Canal Orchestrate relie un Agent, dans un environnement, à un service extérieur : web chat, WhatsApp, SMS, Slack, Teams, Facebook Messenger, Genesys. Un Canal de chaque type par environnement.
- La plateforme attribue à chaque Canal une URL d'événements ; le service extérieur y envoie chaque message et en reçoit la réponse.
- Un Canal détient les identifiants du service extérieur. Ils atteignent l'instance par `.env` et la commande, comme ceux d'une Connexion.
- Le Sandbox de Twilio est un numéro de test partagé pour le développement ; le numéro propre de la ville s'obtient avec un compte WhatsApp professionnel, et le Canal ne change pas.

Le prompt de 10.4 suit la pratique du chapitre 8 pour tout nouvel asset, et les six mêmes points s'appliquent à une Connexion, une Boîte à outils ou au prochain Canal que vous créerez :

1. Nommez l'asset Orchestrate à créer, et son type tel que l'ADK le liste.
2. Nommez l'Agent auquel il appartient et l'environnement.
3. Dites où se trouvent les identifiants et que la commande les lit depuis l'environnement ; n'écrivez jamais de valeur dans le prompt (ici, les deux valeurs de Twilio dans `.env`).
4. Dites ce qui n'est pas nécessaire lorsque Bob a tendance à le demander (ici, le numéro d'expéditeur).
5. Dites ce qui ne doit pas changer (ici, l'Agent).
6. Terminez par les trois questions : ce que Bob a compris, ce dont il a besoin, ce qui existe.

C'est le dernier chapitre. CivicPulse répond aux habitants dans la conversation de watsonx Orchestrate et sur WhatsApp : un Agent d'accueil et trois services, les documents de la ville, des Outils, une Connexion, une Boîte à outils et un Canal, écrits par Bob à partir de vos prompts et testés par vous.
