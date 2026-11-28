import unittest

from app.db import Base


class AcademicSchemaTests(unittest.TestCase):
    def test_academic_tables_registered_on_metadata(self) -> None:
        expected_tables = {
            "formations",
            "specialites",
            "programmes_etudes",
            "matieres",
            "programme_matieres",
            "conditions_admission",
            "prerequis",
            "tarifs",
        }
        self.assertTrue(expected_tables.issubset(set(Base.metadata.tables.keys())))

    def test_foreign_key_relationships_exist(self) -> None:
        tables = Base.metadata.tables
        self.assertEqual(
            {fk.column.table.name for fk in tables["specialites"].foreign_keys},
            {"formations"},
        )
        self.assertEqual(
            {fk.column.table.name for fk in tables["programmes_etudes"].foreign_keys},
            {"specialites"},
        )
        self.assertEqual(
            {fk.column.table.name for fk in tables["programme_matieres"].foreign_keys},
            {"programmes_etudes", "matieres"},
        )
        self.assertEqual(
            {fk.column.table.name for fk in tables["prerequis"].foreign_keys},
            {"formations", "specialites", "matieres"},
        )


if __name__ == "__main__":
    unittest.main()
