from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

JSON_TYPE = JSON().with_variant(JSONB(), "postgresql")


class Formation(TimestampMixin, Base):
    """Academic degree or training program offered by the institution."""

    __tablename__ = "formations"
    __table_args__ = (
        CheckConstraint("duree_annees > 0", name="duree_annees_positive"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    niveau: Mapped[str] = mapped_column(String(50), nullable=False)
    duree_annees: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    langue_enseignement: Mapped[str] = mapped_column(String(30), nullable=False, default="Français")
    mode: Mapped[str] = mapped_column(String(30), nullable=False, default="Présentiel")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    est_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    specialites: Mapped[list["Specialite"]] = relationship(
        back_populates="formation",
        cascade="all, delete-orphan",
    )
    conditions_admission: Mapped[list["ConditionAdmission"]] = relationship(
        back_populates="formation",
        cascade="all, delete-orphan",
    )
    prerequis: Mapped[list["Prerequis"]] = relationship(
        back_populates="formation",
        cascade="all, delete-orphan",
    )
    tarifs: Mapped[list["Tarif"]] = relationship(
        back_populates="formation",
        cascade="all, delete-orphan",
    )


class Specialite(TimestampMixin, Base):
    """Specialization track belonging to a formation."""

    __tablename__ = "specialites"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    formation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    capacite_accueil: Mapped[int | None] = mapped_column(Integer, nullable=True)
    est_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    formation: Mapped["Formation"] = relationship(back_populates="specialites")
    programmes_etudes: Mapped[list["ProgrammeEtude"]] = relationship(
        back_populates="specialite",
        cascade="all, delete-orphan",
    )
    conditions_admission: Mapped[list["ConditionAdmission"]] = relationship(
        back_populates="specialite",
    )
    prerequis: Mapped[list["Prerequis"]] = relationship(
        back_populates="specialite",
    )
    tarifs: Mapped[list["Tarif"]] = relationship(
        back_populates="specialite",
    )


class ProgrammeEtude(TimestampMixin, Base):
    """Study curriculum for a specialty, academic year, level, and semester."""

    __tablename__ = "programmes_etudes"
    __table_args__ = (
        UniqueConstraint(
            "specialite_id",
            "annee_universitaire",
            "niveau_annee",
            "semestre",
            name="uq_programme_specialite_periode",
        ),
        CheckConstraint("niveau_annee > 0", name="niveau_annee_positive"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    specialite_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("specialites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    annee_universitaire: Mapped[str] = mapped_column(String(9), nullable=False)
    niveau_annee: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    semestre: Mapped[str] = mapped_column(String(20), nullable=False)
    credits_ects: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    volume_horaire_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    specialite: Mapped["Specialite"] = relationship(back_populates="programmes_etudes")
    programme_matieres: Mapped[list["ProgrammeMatiere"]] = relationship(
        back_populates="programme",
        cascade="all, delete-orphan",
    )


class Matiere(TimestampMixin, Base):
    """Course or subject taught across one or more study programs."""

    __tablename__ = "matieres"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    credits_ects: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    volume_horaire: Mapped[int | None] = mapped_column(Integer, nullable=True)

    programme_matieres: Mapped[list["ProgrammeMatiere"]] = relationship(
        back_populates="matiere",
    )
    prerequis: Mapped[list["Prerequis"]] = relationship(
        back_populates="matiere",
    )


class ProgrammeMatiere(Base):
    """Many-to-many link associating subjects with study programs and weights."""

    __tablename__ = "programme_matieres"
    __table_args__ = (
        CheckConstraint("coefficient > 0", name="coefficient_positive"),
    )

    programme_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("programmes_etudes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    matiere_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("matieres.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    coefficient: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False, default=Decimal("1.00"))
    est_obligatoire: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ordre: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    programme: Mapped["ProgrammeEtude"] = relationship(back_populates="programme_matieres")
    matiere: Mapped["Matiere"] = relationship(back_populates="programme_matieres")


class ConditionAdmission(TimestampMixin, Base):
    """Admission requirements and required documents for a formation or specialty."""

    __tablename__ = "conditions_admission"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    formation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    specialite_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("specialites.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    diplome_requis: Mapped[str] = mapped_column(String(150), nullable=False)
    moyenne_minimale: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    type_selection: Mapped[str] = mapped_column(String(50), nullable=False, default="Dossier")
    pieces_a_fournir: Mapped[list[Any] | dict[str, Any] | None] = mapped_column(JSON_TYPE, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    formation: Mapped["Formation"] = relationship(back_populates="conditions_admission")
    specialite: Mapped["Specialite | None"] = relationship(back_populates="conditions_admission")


class Prerequis(TimestampMixin, Base):
    """Academic, technical, or language prerequisite linked to a formation, specialty, or subject."""

    __tablename__ = "prerequis"
    __table_args__ = (
        CheckConstraint(
            "formation_id IS NOT NULL OR specialite_id IS NOT NULL OR matiere_id IS NOT NULL",
            name="prerequis_has_target",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    formation_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    specialite_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("specialites.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    matiere_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("matieres.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    categorie: Mapped[str] = mapped_column(String(50), nullable=False)
    intitule: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    est_obligatoire: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    formation: Mapped["Formation | None"] = relationship(back_populates="prerequis")
    specialite: Mapped["Specialite | None"] = relationship(back_populates="prerequis")
    matiere: Mapped["Matiere | None"] = relationship(back_populates="prerequis")


class Tarif(TimestampMixin, Base):
    """Tuition and registration fees per academic year and student category."""

    __tablename__ = "tarifs"
    __table_args__ = (
        CheckConstraint("frais_inscription >= 0", name="frais_inscription_non_negative"),
        CheckConstraint("montant_scolarite >= 0", name="montant_scolarite_non_negative"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    formation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    specialite_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("specialites.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    annee_universitaire: Mapped[str] = mapped_column(String(9), nullable=False)
    categorie_etudiant: Mapped[str] = mapped_column(String(50), nullable=False, default="National")
    frais_inscription: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    montant_scolarite: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    devise: Mapped[str] = mapped_column(String(10), nullable=False, default="TND")
    modalites_paiement: Mapped[str | None] = mapped_column(Text, nullable=True)

    formation: Mapped["Formation"] = relationship(back_populates="tarifs")
    specialite: Mapped["Specialite | None"] = relationship(back_populates="tarifs")
