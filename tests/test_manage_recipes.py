import unittest
import normal_db_functions
import sqlite3

class SimpleTest(unittest.TestCase):
    global db_file
    db_file = "../instance/myDB.sqlite"

    @classmethod
    def setUpClass(cls):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

    @classmethod
    def tearDownClass(cls):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DELETE FROM recipes WHERE name != 'Hiii' AND name != '100'")
        cur.execute("DELETE FROM relationships")
        conn.commit()

    def test_change_recipe_name(self):
        normal_db_functions.create_recipe(db_file, "1", "1.2.3.4", "In Dev")

        normal_db_functions.change_recipe_name(db_file, "1", "1.2.3.4", "Hi")

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE name = 'Hi'")

        data = cur.fetchall()
        if len(data) == 0:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_change_recipe_version_num(self):
        normal_db_functions.create_recipe(db_file, "2", "4.3.2.1", "In Dev")

        normal_db_functions.change_recipe_version_num(db_file, "2", "4.3.2.1", "6.7.8.9")

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE version_num = '6.7.8.9'")

        data = cur.fetchall()
        if len(data) == 0:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_change_recipe_status(self):
        normal_db_functions.create_recipe(db_file, "3", "5.3.2.1", "In Dev")

        normal_db_functions.change_recipe_status(db_file, "3", "5.3.2.1", "Good")

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE status = 'Good'")

        data = cur.fetchall()
        if len(data) == 0:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_get_a_recipe_ID(self):
        # normal_db_functions.create_recipe(db_file, "Hiii", "1.2.3.4", "In dEV")
        ID = normal_db_functions.get_a_recipe_ID(db_file, "Hiii", "1.2.3.4")
        ID = int(ID)
        self.assertEqual(ID, 28)

    def test_get_a_component_ID(self):
        # normal_db_functions.create_component(conn, ("nihao", "1.2.3.5", "2019.10.1", "www.google.com"))
        ID = normal_db_functions.get_a_component_ID(db_file, "nihao", "1.2.3.5")
        ID = int(ID)
        self.assertEqual(ID, 22)

    def test_create_a_relationship(self):
        # normal_db_functions.create_recipe(db_file, "100", "4.3.2.1", "HHH")

        conn = sqlite3.connect(db_file, isolation_level=None)
        # normal_db_functions.create_component(conn, ("hey", "1.2.3.7", "2019.10.2", "www.baidu.com"))
        normal_db_functions.create_a_relationship(db_file, "100", "4.3.2.1", "hey", "1.2.3.7", "/data")

        cur = conn.cursor()
        cur.execute("SELECT * FROM relationships WHERE destination_path = '/data'")
        relationship = cur.fetchall()
        componentID = int(relationship[0][1])
        recipeID = int(relationship[0][2])
        self.assertEqual([componentID, recipeID], [23, 52])


if __name__ == '__main__':
    unittest.main()
