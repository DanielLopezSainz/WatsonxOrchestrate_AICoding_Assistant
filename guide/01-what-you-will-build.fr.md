# Chapitre 1. Ce que vous allez construire

Niveau : débutant. Durée : environ 5 minutes de lecture. Prérequis : aucun.

## Vue d'ensemble

Créer un Agent dans watsonx Orchestrate de manière traditionnelle, c'est écrire à la main des fichiers de définition, des fonctions Python et des commandes. Avec IBM Bob, vous décrivez en langage naturel ce que l'Agent doit faire. Bob réalise le développement à votre place, envoie le code à votre instance Orchestrate et teste le résultat pour confirmer que l'agent d'IA fonctionne comme prévu.

Dans ce guide, vous construisez l'application agentique CivicPulse pour la ville d'Utopia. Les habitants posent à CivicPulse des questions telles que :

- Quel service s'occupe d'un lampadaire éteint ?
- Ai-je besoin d'un permis pour un abri de jardin ?
- Quand le bac vert est-il collecté dans ma rue ?
- Où en est ma demande de permis ?

CivicPulse y répond, et lorsqu'un habitant a besoin qu'une action soit faite, comme signaler un problème ou ouvrir un dossier d'assistance, il la fait pour lui.

Vous construisez votre Agent de manière progressive, chaque amélioration s'appuyant sur la précédente. La première version de l'Agent, au chapitre 4, est simple : un Agent qui indique aux habitants lequel des trois services municipaux contacter, selon leur question. Sur cette base, vous ajoutez :

- Chapitre 5 : l'Agent a accès à la réglementation de la ville, pour répondre aux questions sur les permis, les déchets et le bruit à partir des documents officiels.
- Chapitre 6 : des Outils qui consultent les dossiers propres à un habitant : une demande de permis, une réparation de voirie, les jours de collecte d'une rue.
- Chapitre 7 : une Connexion au centre d'appels 311 de la ville, pour que les habitants puissent signaler des problèmes et obtenir un numéro de demande pour les suivre.
- Chapitre 8 : un registre des adresses, pour que « 18 elm st » soit compris comme Elm Street.
- Chapitre 9 : une équipe d'Agents spécialisés ajoutée à l'Agent principal, un par service, chacun travaillant sur les tâches de son service.
- Chapitre 10 : un numéro WhatsApp, pour que les habitants puissent utiliser leur messagerie préférée pour échanger avec CivicPulse.

À la fin, CivicPulse est une équipe de quatre Agents qui a accès à la réglementation de la ville (une Base de connaissances, interrogée par RAG), à des Outils (des programmes Python), à une Connexion (vers un système externe, le centre d'appels 311), à une Boîte à outils (un serveur MCP) et à un Canal (WhatsApp), tous écrits par Bob à partir de vos prompts.

Si vous connaissez déjà watsonx Orchestrate et Bob, allez à la section 1.3 pour le scénario et à la section 1.4 si vous voulez passer directement à un chapitre précis.

## 1.1 Les 2 personnages principaux

Ce guide utilise IBM Bob et IBM watsonx Orchestrate.

| Produit | Ce que c'est | Son rôle dans ce guide |
|---|---|---|
| IBM watsonx Orchestrate | Une plateforme qui exécute des agents d'IA. Un Agent Orchestrate répond à des questions et réalise des tâches pour ses utilisateurs, à l'aide d'instructions, de documents et de Connexions vers d'autres systèmes | Les Agents que vous créez s'exécutent ici. Votre exemplaire de la plateforme s'appelle une instance : un tenant SaaS, ou la Developer Edition sur votre propre machine |
| IBM Bob | Un assistant de codage par IA qui travaille dans un environnement de développement. Vous décrivez ce que vous voulez dans une conversation ; Bob écrit les fichiers, exécute les opérations et rend compte du résultat | C'est ici que vous créez les Agents. Vous n'écrivez pas à la main les fichiers d'Agent, d'Outil ou de Base de connaissances |

Le chapitre 2 installe l'extension watsonx Orchestrate ADK pour Bob. Cette extension relie les deux produits, pour que Bob puisse lister ce qui existe sur votre instance, y envoyer de nouveaux Agents et les tester.

## 1.2 De quoi se compose un Agent Orchestrate

Un Agent Orchestrate est construit à partir d'un petit ensemble de composants. Plusieurs d'entre eux sont des assets Orchestrate ayant leur propre type, écrits avec une majuscule dans ce guide.

| Composant | Ce que c'est |
|---|---|
| Instructions | Le texte qui définit l'Agent : son rôle, les faits qu'il connaît, sa manière de répondre et ce qu'il ne doit pas faire |
| Modèle | Le modèle de langage sur lequel l'Agent s'exécute. Le guide utilise le modèle par défaut de l'instance. Chaque Agent peut utiliser un modèle différent |
| Base de connaissances Orchestrate | Un ensemble de documents que l'Agent consulte lorsqu'une question demande plus d'informations que n'en contiennent ses instructions |
| Outils Orchestrate | Des fonctions que l'Agent appelle pour consulter des données ou réaliser une action |
| Connexions Orchestrate | Les adresses et identifiants des systèmes externes qu'utilisent les Outils |
| Boîtes à outils Orchestrate | Des groupes d'Outils fournis par un serveur externe et rattachés à l'Agent comme un ensemble |
| Agents collaborateurs | D'autres Agents Orchestrate auxquels un Agent délègue, pour que chaque Agent ait un rôle clair |
| Flux Orchestrate (Flows) | Des suites d'étapes définies à l'avance, avec des embranchements si nécessaire, au lieu d'être décidées par le modèle à chaque question |
| Canaux Orchestrate | Les interfaces par lesquelles les utilisateurs joignent un Agent, comme WhatsApp ou une fenêtre de conversation sur une page web |

Un Agent que vous créez reste dans l'environnement Draft de l'instance, où seuls les créateurs peuvent l'utiliser, jusqu'à ce que vous le déployiez en Live, où ses utilisateurs le joignent.

## 1.3 Le scénario

CivicPulse, la plateforme de services aux habitants de la ville d'Utopia, est le seul système que le guide construit du début à la fin. Chaque composant d'un Agent Orchestrate a un rôle dans ce scénario : une réglementation à consulter, l'état d'un permis à vérifier, un centre d'appels 311 auquel signaler, des services entre lesquels orienter les questions.

La ville, ses services, ses habitants et toutes ses données sont fictifs. Le guide utilise ces services :

| Service | Ce qu'il traite |
|---|---|
| Permits and Planning (Permis et urbanisme) | Permis de construire et demandes d'urbanisme |
| Roads and Infrastructure (Voirie et infrastructures) | Nids-de-poule, lampadaires, panneaux endommagés, dangers urgents sur la voie publique |
| Waste and Recycling (Déchets et recyclage) | Jours de collecte, collecte des encombrants, règles de recyclage |

## 1.4 Les chapitres

| Chapitre | Ce que vous faites | Composant Orchestrate | Capacité de Bob |
|---|---|---|---|
| 2 | Connecter Bob à votre instance watsonx Orchestrate | L'instance et ses environnements | L'extension, les vues, les approbations |
| 3 | Apprendre la méthode de travail | Aucun | Les modes Ask, Plan et Agent ; les prompts ; git |
| 4 | Créer un Agent Orchestrate qui indique aux habitants quel service contacter, et le déployer en Live | Instructions et modèle ; les environnements Draft et Live | Les trois modes à la suite |
| 5 | Donner à l'Agent les guides et la réglementation de la ville | Base de connaissances Orchestrate | Bob écrit les documents |
| 6 | Permettre à l'Agent de consulter l'état d'une demande ou d'un permis | Outils Orchestrate | Bob écrit les Outils ; lire le raisonnement de l'Agent |
| 7 | Permettre à l'Agent de signaler un nouveau problème au centre d'appels 311 de la ville | Connexions Orchestrate | Les identifiants tenus hors de la conversation |
| 8 | Ajouter une recherche d'adresse fournie par un serveur MCP | Boîte à outils Orchestrate | Bob construit le serveur MCP et le teste avant la plateforme |
| 9 | Répartir le travail entre un Agent d'accueil et un Agent par service | Agents collaborateurs | Le mode Plan pour une conception à plusieurs Agents |
| 10 | Donner un numéro WhatsApp à CivicPulse | Canal Orchestrate | Un prompt structuré pour une tâche en mode Agent, sans conception |

À partir du chapitre 4, chaque chapitre comporte une vue d'ensemble avec une note pour sauter les chapitres précédents, des prérequis, des étapes, des tests et un résumé, et les chapitres 4 à 9 se terminent par un déploiement. Les fichiers produits par chaque chapitre se trouvent dans le dossier `walkthroughs` du dépôt, pour que vous puissiez commencer à n'importe quel chapitre.
