# DataMind — Modèle de données

## 1. Objectif

Le modèle de données de DataMind permet de gérer :

- les utilisateurs ;
- les datasets importés ;
- le profilage des datasets ;
- les analyses réalisées ;
- les visualisations ;
- les conversations avec l'AI Analyst ;
- les messages échangés.

La base de données utilisée pour le MVP est PostgreSQL.

---

# 2. Architecture générale

```text
User
│
├──< Dataset
│     │
│     ├── DatasetProfile
│     │      └──< ColumnProfile
│     │
│     └──< Analysis
│            └──< Visualization
│
└──< Conversation
       │
       ├── Dataset (optionnel)
       │
       └──< Message



3. Entités principales
3.1 User

Représente un utilisateur de DataMind.

Principaux attributs
Attribut	Type	Contraintes
id	Integer	PK
name	String(100)	NOT NULL
first_name	String(100)	NOT NULL
email	String(255)	NOT NULL, UNIQUE, INDEX
profession	String(150)	NULLABLE
password_hash	String(255)	NOT NULL
created_at	DateTime	NOT NULL
updated_at	DateTime	NOT NULL
Relations

Un utilisateur peut posséder plusieurs :

datasets ;
analyses ;
conversations.
4. Dataset

Représente un fichier de données importé par un utilisateur.

Principaux attributs
Attribut	Type	Contraintes
id	Integer	PK
user_id	Integer	FK → users.id, NOT NULL
name	String(255)	NOT NULL
source_type	String(50)	NOT NULL
file_name	String(255)	NOT NULL
file_size	Integer	NULLABLE
storage_key	String(500)	NOT NULL
created_at	DateTime	NOT NULL
updated_at	DateTime	NOT NULL
Relations
User 1 ─── N Dataset

Un dataset appartient à un seul utilisateur.

Suppression

Si un utilisateur est supprimé :

User
 ↓ CASCADE
Dataset

Ses datasets sont supprimés.

5. DatasetProfile

Contient le résultat du profilage global d'un dataset.

Principaux attributs
Attribut	Type
id	Integer
dataset_id	Integer
row_count	Integer
column_count	Integer
missing_value_count	Integer
duplicate_row_count	Integer
quality_score	Float
details	JSONB
created_at	DateTime
updated_at	DateTime
Relation
Dataset 1 ─── 1 DatasetProfile

dataset_id est UNIQUE.

Un dataset possède donc un seul profil global.

6. ColumnProfile

Contient les informations de profilage d'une colonne.

Principaux attributs
Attribut	Type
id	Integer
dataset_profile_id	Integer
column_name	String(255)
data_type	String(100)
total_count	Integer
missing_count	Integer
missing_percentage	Float
distinct_count	Integer
distinct_percentage	Float
is_identifier_candidate	Boolean
statistics	JSONB
Relation
DatasetProfile 1 ─── N ColumnProfile
Suppression
DatasetProfile
      ↓ CASCADE
ColumnProfile
7. Analysis

Représente une analyse effectuée sur un dataset.

Principaux attributs
Attribut	Type	Contraintes
id	Integer	PK
user_id	Integer	FK, NOT NULL
dataset_id	Integer	FK, NOT NULL
analysis_type	String	NOT NULL
question	Text	NOT NULL
filters	JSONB	NULLABLE
result	JSONB	NULLABLE
created_at	DateTime	NOT NULL
updated_at	DateTime	NOT NULL
Pourquoi JSONB ?

Les analyses peuvent produire des résultats de formes différentes.

Exemple :

{
  "mean": 125000,
  "median": 118000,
  "count": 100
}

Une autre analyse pourrait produire :

{
  "correlation": 0.87,
  "variables": ["age", "salary"]
}

Il est donc préférable de conserver les résultats flexibles dans JSONB.

8. Filtres

Les filtres appliqués à une analyse sont stockés dans :

Analysis.filters

Exemple :

{
  "date": {
    "column": "date",
    "from": "2025-01-01",
    "to": "2025-12-31"
  },
  "region": {
    "column": "region",
    "values": ["Abidjan", "Bouaké"]
  }
}

Les filtres ne sont pas stockés comme des colonnes fixes dans Dataset.

Ils sont appliqués dynamiquement par le Data Engine.

9. Visualization

Représente une visualisation produite à partir d'une analyse.

Principaux attributs
Attribut	Type
id	Integer
analysis_id	Integer
chart_type	String
title	String
config	JSONB
created_at	DateTime
updated_at	DateTime
Relation
Analysis 1 ─── N Visualization

Une analyse peut donc générer plusieurs graphiques.

Suppression
Analysis
   ↓ CASCADE
Visualization
10. Conversation

Représente une conversation avec l'AI Analyst.

Principaux attributs
Attribut	Type	Contraintes
id	Integer	PK
user_id	Integer	FK, NOT NULL
dataset_id	Integer	FK, NULLABLE
title	String(255)	NOT NULL
created_at	DateTime	NOT NULL
updated_at	DateTime	NOT NULL
Pourquoi dataset_id est nullable ?

Une conversation peut commencer sans dataset.

Exemple :

Comment fonctionne une corrélation ?

Le dataset peut ensuite être associé à la conversation.

Suppression

Si un dataset est supprimé :

Dataset
   ↓ SET NULL
Conversation

La conversation est conservée mais :

dataset_id = NULL

Cela permet de préserver l'historique de l'utilisateur.

11. Message

Représente un message appartenant à une conversation.

Principaux attributs
Attribut	Type
id	Integer
conversation_id	Integer
role	String
content	Text
message_metadata	JSONB
created_at	DateTime
updated_at	DateTime
Relation
Conversation 1 ─── N Message
Roles prévus

Les valeurs sont actuellement validées au niveau applicatif :

user
assistant
system
tool
message_metadata

Permet de conserver des informations techniques liées au message.

Exemple :

{
  "analysis_id": 42,
  "tools_used": [
    "filter_data",
    "aggregate_data"
  ],
  "visualization_id": 15
}
12. Règles de suppression
Relation	Comportement
User → Dataset	CASCADE
User → Conversation	CASCADE
User → Analysis	CASCADE
Dataset → DatasetProfile	CASCADE
DatasetProfile → ColumnProfile	CASCADE
Dataset → Analysis	CASCADE
Analysis → Visualization	CASCADE
Conversation → Message	CASCADE
Dataset → Conversation	SET NULL
13. Indexation

Les index sont principalement placés sur :

users.email
datasets.user_id
dataset_profiles.dataset_id
column_profiles.dataset_profile_id
analyses.user_id
analyses.dataset_id
visualizations.analysis_id
conversations.user_id
conversations.dataset_id
messages.conversation_id

L'objectif est d'améliorer les recherches fréquentes et les jointures entre les entités.

14. Choix techniques
IDs

Le MVP utilise des IDs de type :

Integer

Le passage à UUID pourra être envisagé ultérieurement si les besoins du produit l'exigent.

Base de données
PostgreSQL
Données flexibles

Les champs dont la structure peut varier utilisent :

JSONB

notamment :

DatasetProfile.details
ColumnProfile.statistics
Analysis.filters
Analysis.result
Visualization.config
Message.message_metadata
ORM
SQLAlchemy 2
Migrations
Alembic
15. Cas d'utilisation couverts
Import d'un dataset
User
 ↓
Dataset
Profilage
Dataset
 ↓
DatasetProfile
 ↓
ColumnProfile
Analyse
Dataset
 ↓
Analysis
 ├── filters
 └── result
Visualisation
Analysis
 ↓
Visualization
Conversation avec l'AI Analyst
User
 ↓
Conversation
 ↓
Message
 ↓
AI Agent
 ↓
Analysis / Tools
16. Principe architectural important

Le modèle de données ne doit pas contenir la logique d'analyse elle-même.

PostgreSQL conserve principalement :

les utilisateurs ;
les métadonnées ;
les analyses ;
les conversations ;
les résultats structurés ;
les configurations.

Le traitement des datasets sera effectué par le Data Engine :

Pandas / DuckDB

L'AI Agent utilisera des outils contrôlés pour effectuer les analyses.

User
 ↓
AI Agent
 ↓
Tool
 ↓
Data Engine
 ↓
Résultat réel
 ↓
AI Agent
 ↓
Message

L'AI ne doit pas inventer les résultats analytiques.

17. Statut

Le modèle de données du MVP a été :

conçu ;
implémenté avec SQLAlchemy ;
migré avec Alembic ;
testé ;
vérifié au niveau des relations ;
vérifié au niveau des suppressions ;
vérifié avec les principaux cas d'utilisation.

Statut : VALIDÉ ✅

Prochaine étape :

Architecture REST API

### 🎯 Et surtout

Cette documentation devient notre **référence technique**. Quand on construira les endpoints, on pourra revenir ici pour vérifier :

> « Quelle entité manipule cette API ? Quelle relation ? Quelle règle de suppression ? »

Ça évite que l'architecture évolue au hasard.

Une fois ce fichier ajouté à `docs/data-model.md`, **la carte Trello "Concevoir le modèle de données" est réellement prête à passer en TERMINÉ**. Ensuite on ouvre **« Définir l'architecture REST API »**.