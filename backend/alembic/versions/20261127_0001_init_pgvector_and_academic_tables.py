"""enable pgvector and create academic offer tables

Revision ID: 20261127_0001
Revises:
Create Date: 2026-11-27 16:35:00
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261127_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "formations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("titre", sa.String(length=200), nullable=False),
        sa.Column("niveau", sa.String(length=50), nullable=False),
        sa.Column("duree_annees", sa.SmallInteger(), nullable=False),
        sa.Column("langue_enseignement", sa.String(length=30), nullable=False),
        sa.Column("mode", sa.String(length=30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("est_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("duree_annees > 0", name=op.f("ck_formations_duree_annees_positive")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_formations")),
        sa.UniqueConstraint("code", name=op.f("uq_formations_code")),
    )

    op.create_table(
        "matieres",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("nom", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("credits_ects", sa.SmallInteger(), nullable=True),
        sa.Column("volume_horaire", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matieres")),
        sa.UniqueConstraint("code", name=op.f("uq_matieres_code")),
    )

    op.create_table(
        "specialites",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("formation_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("nom", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("capacite_accueil", sa.Integer(), nullable=True),
        sa.Column("est_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["formation_id"], ["formations.id"], name=op.f("fk_specialites_formation_id_formations"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_specialites")),
        sa.UniqueConstraint("code", name=op.f("uq_specialites_code")),
    )
    op.create_index(op.f("ix_specialites_formation_id"), "specialites", ["formation_id"], unique=False)

    op.create_table(
        "programmes_etudes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("specialite_id", sa.Uuid(), nullable=False),
        sa.Column("annee_universitaire", sa.String(length=9), nullable=False),
        sa.Column("niveau_annee", sa.SmallInteger(), nullable=False),
        sa.Column("semestre", sa.String(length=20), nullable=False),
        sa.Column("credits_ects", sa.SmallInteger(), nullable=True),
        sa.Column("volume_horaire_total", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("niveau_annee > 0", name=op.f("ck_programmes_etudes_niveau_annee_positive")),
        sa.ForeignKeyConstraint(["specialite_id"], ["specialites.id"], name=op.f("fk_programmes_etudes_specialite_id_specialites"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_programmes_etudes")),
        sa.UniqueConstraint("specialite_id", "annee_universitaire", "niveau_annee", "semestre", name="uq_programme_specialite_periode"),
    )
    op.create_index(op.f("ix_programmes_etudes_specialite_id"), "programmes_etudes", ["specialite_id"], unique=False)

    op.create_table(
        "conditions_admission",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("formation_id", sa.Uuid(), nullable=False),
        sa.Column("specialite_id", sa.Uuid(), nullable=True),
        sa.Column("titre", sa.String(length=200), nullable=False),
        sa.Column("diplome_requis", sa.String(length=150), nullable=False),
        sa.Column("moyenne_minimale", sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column("type_selection", sa.String(length=50), nullable=False),
        sa.Column("pieces_a_fournir", sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["formation_id"], ["formations.id"], name=op.f("fk_conditions_admission_formation_id_formations"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["specialite_id"], ["specialites.id"], name=op.f("fk_conditions_admission_specialite_id_specialites"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_conditions_admission")),
    )
    op.create_index(op.f("ix_conditions_admission_formation_id"), "conditions_admission", ["formation_id"], unique=False)
    op.create_index(op.f("ix_conditions_admission_specialite_id"), "conditions_admission", ["specialite_id"], unique=False)

    op.create_table(
        "prerequis",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("formation_id", sa.Uuid(), nullable=True),
        sa.Column("specialite_id", sa.Uuid(), nullable=True),
        sa.Column("matiere_id", sa.Uuid(), nullable=True),
        sa.Column("categorie", sa.String(length=50), nullable=False),
        sa.Column("intitule", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("est_obligatoire", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "formation_id IS NOT NULL OR specialite_id IS NOT NULL OR matiere_id IS NOT NULL",
            name=op.f("ck_prerequis_prerequis_has_target"),
        ),
        sa.ForeignKeyConstraint(["formation_id"], ["formations.id"], name=op.f("fk_prerequis_formation_id_formations"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["matiere_id"], ["matieres.id"], name=op.f("fk_prerequis_matiere_id_matieres"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["specialite_id"], ["specialites.id"], name=op.f("fk_prerequis_specialite_id_specialites"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prerequis")),
    )
    op.create_index(op.f("ix_prerequis_formation_id"), "prerequis", ["formation_id"], unique=False)
    op.create_index(op.f("ix_prerequis_matiere_id"), "prerequis", ["matiere_id"], unique=False)
    op.create_index(op.f("ix_prerequis_specialite_id"), "prerequis", ["specialite_id"], unique=False)

    op.create_table(
        "programme_matieres",
        sa.Column("programme_id", sa.Uuid(), nullable=False),
        sa.Column("matiere_id", sa.Uuid(), nullable=False),
        sa.Column("coefficient", sa.Numeric(precision=4, scale=2), nullable=False),
        sa.Column("est_obligatoire", sa.Boolean(), nullable=False),
        sa.Column("ordre", sa.SmallInteger(), nullable=True),
        sa.CheckConstraint("coefficient > 0", name=op.f("ck_programme_matieres_coefficient_positive")),
        sa.ForeignKeyConstraint(["matiere_id"], ["matieres.id"], name=op.f("fk_programme_matieres_matiere_id_matieres"), ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["programme_id"], ["programmes_etudes.id"], name=op.f("fk_programme_matieres_programme_id_programmes_etudes"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("programme_id", "matiere_id", name=op.f("pk_programme_matieres")),
    )

    op.create_table(
        "tarifs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("formation_id", sa.Uuid(), nullable=False),
        sa.Column("specialite_id", sa.Uuid(), nullable=True),
        sa.Column("annee_universitaire", sa.String(length=9), nullable=False),
        sa.Column("categorie_etudiant", sa.String(length=50), nullable=False),
        sa.Column("frais_inscription", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("montant_scolarite", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("devise", sa.String(length=10), nullable=False),
        sa.Column("modalites_paiement", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("frais_inscription >= 0", name=op.f("ck_tarifs_frais_inscription_non_negative")),
        sa.CheckConstraint("montant_scolarite >= 0", name=op.f("ck_tarifs_montant_scolarite_non_negative")),
        sa.ForeignKeyConstraint(["formation_id"], ["formations.id"], name=op.f("fk_tarifs_formation_id_formations"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["specialite_id"], ["specialites.id"], name=op.f("fk_tarifs_specialite_id_specialites"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tarifs")),
    )
    op.create_index(op.f("ix_tarifs_formation_id"), "tarifs", ["formation_id"], unique=False)
    op.create_index(op.f("ix_tarifs_specialite_id"), "tarifs", ["specialite_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tarifs_specialite_id"), table_name="tarifs")
    op.drop_index(op.f("ix_tarifs_formation_id"), table_name="tarifs")
    op.drop_table("tarifs")
    op.drop_table("programme_matieres")
    op.drop_index(op.f("ix_prerequis_specialite_id"), table_name="prerequis")
    op.drop_index(op.f("ix_prerequis_matiere_id"), table_name="prerequis")
    op.drop_index(op.f("ix_prerequis_formation_id"), table_name="prerequis")
    op.drop_table("prerequis")
    op.drop_index(op.f("ix_conditions_admission_specialite_id"), table_name="conditions_admission")
    op.drop_index(op.f("ix_conditions_admission_formation_id"), table_name="conditions_admission")
    op.drop_table("conditions_admission")
    op.drop_index(op.f("ix_programmes_etudes_specialite_id"), table_name="programmes_etudes")
    op.drop_table("programmes_etudes")
    op.drop_index(op.f("ix_specialites_formation_id"), table_name="specialites")
    op.drop_table("specialites")
    op.drop_table("matieres")
    op.drop_table("formations")
    op.execute("DROP EXTENSION IF EXISTS vector")
