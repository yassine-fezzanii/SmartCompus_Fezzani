# Modèle de données PostgreSQL — SmartCampus AI

Ce document présente la conception du modèle de données relationnel de **SmartCampus AI** (avec extension `pgvector` activée pour le futur pipeline RAG).

## Tâche 1 : Offre académique, programmes, prérequis, admission et tarifs

### Diagramme Entité-Relation (ERD)

```mermaid
erDiagram
    FORMATIONS ||--o{ SPECIALITES : "propose"
    FORMATIONS ||--o{ CONDITIONS_ADMISSION : "definit"
    FORMATIONS ||--o{ PREREQUIS : "exige"
    FORMATIONS ||--o{ TARIFS : "tarife"

    SPECIALITES ||--o{ PROGRAMMES_ETUDES : "organise"
    SPECIALITES |o--o{ CONDITIONS_ADMISSION : "precise"
    SPECIALITES |o--o{ PREREQUIS : "exige"
    SPECIALITES |o--o{ TARIFS : "adapte"

    PROGRAMMES_ETUDES ||--o{ PROGRAMME_MATIERES : "contient"
    MATIERES ||--o{ PROGRAMME_MATIERES : "est_enseignee_dans"
    MATIERES |o--o{ PREREQUIS : "requiert"

    FORMATIONS {
        uuid id PK
        varchar code UK
        varchar titre
        varchar niveau
        smallint duree_annees
        varchar langue_enseignement
        varchar mode
        text description
        boolean est_active
        timestamptz created_at
        timestamptz updated_at
    }

    SPECIALITES {
        uuid id PK
        uuid formation_id FK
        varchar code UK
        varchar nom
        text description
        int capacite_accueil
        boolean est_active
        timestamptz created_at
        timestamptz updated_at
    }

    PROGRAMMES_ETUDES {
        uuid id PK
        uuid specialite_id FK
        varchar annee_universitaire
        smallint niveau_annee
        varchar semestre
        smallint credits_ects
        int volume_horaire_total
        text description
        timestamptz created_at
        timestamptz updated_at
    }

    MATIERES {
        uuid id PK
        varchar code UK
        varchar nom
        text description
        smallint credits_ects
        int volume_horaire
        timestamptz created_at
        timestamptz updated_at
    }

    PROGRAMME_MATIERES {
        uuid programme_id PK,FK
        uuid matiere_id PK,FK
        numeric coefficient
        boolean est_obligatoire
        smallint ordre
    }

    CONDITIONS_ADMISSION {
        uuid id PK
        uuid formation_id FK
        uuid specialite_id FK
        varchar titre
        varchar diplome_requis
        numeric moyenne_minimale
        varchar type_selection
        jsonb pieces_a_fournir
        text description
        timestamptz created_at
        timestamptz updated_at
    }

    PREREQUIS {
        uuid id PK
        uuid formation_id FK
        uuid specialite_id FK
        uuid matiere_id FK
        varchar categorie
        varchar intitule
        text description
        boolean est_obligatoire
        timestamptz created_at
        timestamptz updated_at
    }

    TARIFS {
        uuid id PK
        uuid formation_id FK
        uuid specialite_id FK
        varchar annee_universitaire
        varchar categorie_etudiant
        numeric frais_inscription
        numeric montant_scolarite
        varchar devise
        text modalites_paiement
        timestamptz created_at
        timestamptz updated_at
    }
```

### Relations et cardinalités

| Relation | Cardinalité | Règle métier |
| :--- | :--- | :--- |
| `formations` → `specialites` | `1:N` | Une formation regroupe une ou plusieurs spécialités (`ON DELETE CASCADE`). |
| `specialites` → `programmes_etudes` | `1:N` | Chaque spécialité possède des programmes par année universitaire, niveau et semestre (`UNIQUE(specialite_id, annee_universitaire, niveau_annee, semestre)`). |
| `programmes_etudes` ↔ `matieres` | `N:N` via `programme_matieres` | Une matière peut appartenir à plusieurs programmes avec un coefficient, un caractère obligatoire et un ordre propres. |
| `formations` / `specialites` → `conditions_admission` | `1:N` / `0..1:N` | Les conditions sont définies au niveau de la formation et peuvent être précisées pour une spécialité donnée. |
| `formations` / `specialites` / `matieres` → `prerequis` | `0..1:N` | Un prérequis cible au moins une formation, une spécialité ou une matière (`CHECK` contrainte). |
| `formations` / `specialites` → `tarifs` | `1:N` / `0..1:N` | Les tarifs sont définis par année universitaire et catégorie d'étudiant (`NUMERIC(10,2)` non négatif). |
