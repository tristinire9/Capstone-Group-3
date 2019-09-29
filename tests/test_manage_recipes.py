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
        cur.execute("DELETE FROM recipes")
        cur.execute("DELETE FROM relationships")

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

if __name__ == '__main__':
    unittest.main()
