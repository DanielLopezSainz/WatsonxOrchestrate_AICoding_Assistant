# Introduction

Créer des agents watsonx Orchestrate avec IBM Bob. IBM CSM Team, France. Rédigé et testé en septembre et octobre 2026 avec IBM Bob 2.1, l'ADK watsonx Orchestrate 2.18.0 et une instance watsonx Orchestrate sur IBM Cloud, sous macOS.

## À qui s'adresse ce guide

À toute personne qui souhaite créer des agents d'IA avec watsonx Orchestrate. Les développeurs expérimentés constateront que travailler avec Bob augmente leur productivité. Aux nouveaux utilisateurs, Bob offre la possibilité de développer des agents d'IA complets, aux fonctionnalités avancées, sans devoir être des développeurs experts.

## Prérequis

| | Pourquoi |
|---|---|
| IBM Bob 2.1 ou ultérieur, installé | L'assistant qui écrit et exécute tout |
| Une instance watsonx Orchestrate, ou la Developer Edition sur votre machine | Il vous faut une instance watsonx Orchestrate opérationnelle à laquelle connecter Bob |
| Git, installé | Bob l'utilise pour cloner le dépôt et enregistrer votre travail ; pas indispensable pour suivre le cours |
| Un téléphone avec WhatsApp | Uniquement si vous voulez utiliser Orchestrate depuis WhatsApp, chapitre 10 |
| Environ huit heures | Notre estimation du temps moyen nécessaire pour suivre tous les chapitres. Vous êtes libre d'aller directement au chapitre de votre choix |

## Comment le lire

Les chapitres s'appuient les uns sur les autres, dans l'ordre : le chapitre 2 connecte Bob à votre instance, le chapitre 3 présente la méthode de travail, et les chapitres 4 à 10 ajoutent chacun un composant au même Agent. À partir du chapitre 4, chaque chapitre s'ouvre sur une note pour sauter les chapitres précédents : les fichiers des chapitres précédents se trouvent dans le dossier `walkthroughs` du dépôt, avec une instruction à donner à Bob pour les importer, afin que vous puissiez commencer au chapitre dont vous avez besoin. Le chapitre 3 commence par un tableau qui aide les utilisateurs expérimentés à décider s'ils le lisent ou le sautent.

Chaque chapitre indique son niveau, sa durée et ses prérequis dans sa première ligne, et se termine par un résumé de ce qui a été construit et de ce qu'il faut retenir.

## Conventions

- Un prompt destiné à Bob figure dans un bloc de code. Envoyez-le en entier, tel quel ; le chapitre indique dans quel mode et s'il faut ouvrir une nouvelle conversation. Les prompts restent en anglais, tels qu'ils ont été testés.
- « Mode : Ask, dans une nouvelle conversation. » avant un prompt indique le mode et la conversation.
- « Points à vérifier dans la réponse de Bob : » liste ce que la réponse doit contenir ; « Vous devriez voir : » décrit l'écran après une étape.
- « Approuvez chaque demande au fur et à mesure. » signifie que Bob demande une approbation avant d'écrire un fichier ou d'exécuter une commande, et que vous approuvez chacune d'elles.
- « Enregistrez votre travail : » donne l'instruction qui valide (commit) les fichiers du chapitre.
- Un paragraphe qui commence par IMPORTANT énonce une règle valable pour le reste du guide.
- Les types d'assets Orchestrate portent une majuscule dans le texte (un Agent, un Outil, une Base de connaissances, une Connexion, une Boîte à outils, un Canal) ; dans les prompts et les fichiers, ils sont écrits comme Bob et la plateforme les écrivent, en anglais et en minuscules (agent, tool, knowledge base, connection, toolkit, channel).
- `Ask civic_info_agent:` devant une question l'envoie à l'Agent par l'intermédiaire de Bob.

## Le dépôt

Le guide, c'est ce dépôt : les chapitres dans `guide`, les fichiers de chaque chapitre dans `walkthroughs`, le README avec la liste des chapitres. C'est aussi le dossier de projet dans lequel vous travaillez avec Bob, comme l'explique le chapitre 2. Le fichier `.env.example` liste les valeurs qui restent sur votre machine, jamais dans le dépôt ni dans une conversation.

## Signaler un problème

La plateforme et Bob évoluent avec leurs versions, et une étape qui fonctionnait lors de la rédaction du guide peut se présenter différemment chez vous. Ouvrez une issue dans le dépôt en indiquant le chapitre, la section, ce que vous avez envoyé et ce que vous avez obtenu ; le guide est corrigé à partir de ces signalements.
