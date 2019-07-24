# coding=utf-8
import unittest

from datetime import date
from sqlalchemy.orm import sessionmaker

from petsrus.petsrus import app, engine
from petsrus.models.models import Base, Pet


class PetsRUsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_index(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(bytes("Login Page", "utf-8"), result.data)

    def test_get_pets(self):
        # No pets
        result = self.app.get("/pets")
        self.assertEqual(result.status_code, 200)
        expected_data = (
            "<!doctype html>\n<title>PetsRUs</title>\n\n    No pets found.\n"
        )
        self.assertEqual(bytes(expected_data, "utf-8"), result.data)

        # Add pets and test
        maxx = Pet(
            name="Max",
            date_of_birth=date(2001, 1, 1),
            species="canine",
            breed="Jack Russell Terrier",
            sex="m",
            colour_and_identifying_marks="White with tan markings",
        )
        self.session.add(maxx)
        duke = Pet(
            name="Duke",
            date_of_birth=date(2001, 1, 2),
            species="canine",
            breed="Newfoundland",
            sex="m",
            colour_and_identifying_marks="Black",
        )
        self.session.add(duke)
        self.session.commit()
        result = self.app.get("/pets")
        expected_data = "<!doctype html>\n<title>PetsRUs</title>\n\n<ul>\n    \n    <li> Name: Max Breed: Jack Russell Terrier Species: canine </li>\n    \n    <li> Name: Duke Breed: Newfoundland Species: canine </li>\n    \n</ul>\n"  # noqa
        self.assertEqual(result.status_code, 200)
        self.assertEqual(bytes(expected_data, "utf-8"), result.data)


if __name__ == "__main__":
    unittest.main()
