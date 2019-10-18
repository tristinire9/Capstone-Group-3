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
        cur.execute(
            "INSERT INTO components (name, version_num, date, url) VALUES ('Ahmad', '2.4.7.8', '1997-10-12', 'www.google.com')")

    @classmethod
    def tearDownClass(cls):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DELETE FROM recipes")
        cur.execute("DELETE FROM relationships")

    def test_create_component(self):
        conn = normal_db_functions.create_connection(db_file)
        cur = conn.cursor()
        cur.execute("select count(*) from components")
        one = cur.fetchone()
        number_of_components_1 = one[0]

        normal_db_functions.create_component(conn, ("Thomas", "1.2.3.4", "19/9/2019", "www.google.com"))

        cur.execute("select count(*) from components")
        one = cur.fetchone()

        number_of_components_2 = one[0]

        self.assertEqual(number_of_components_2, number_of_components_1+1)


    def test_check_duplicate_1(self):
        duplicate = normal_db_functions.check_duplicate(db_file, "Thomas", "1.2.3.4")
        self.assertEqual(duplicate, True)

    def test_check_duplicate_2(self):
        duplicate = normal_db_functions.check_duplicate(db_file, "Bob", "1.2.3.4")
        self.assertEqual(duplicate, False)

    def test_look_up(self):
        result = normal_db_functions.lookup(db_file, "test")
        self.assertEqual(result, ["1.2.3.4"])


    def test_get_URL(self):
        result = normal_db_functions.get_URL(db_file, "test", "1.2.3.4")
        result_list = []
        for data in result:
            result_list.append(data[0])
        self.assertEqual(result_list, ["https://capprojteam3.s3-ap-southeast-2.amazonaws.com/test"])


    def test_delete_component(self):
        normal_db_functions.delete_component(db_file, "Ahmad", "2.4.7.8")

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE name = 'Ahmad' AND version_num = '2.4.7.8'")
        data = cur.fetchall()
        if len(data) == 0:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_create_recipe(self):
        normal_db_functions.create_recipe(db_file, "MyRecipe", "7.8.9.4", "In development")

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE name = 'MyRecipe' AND version_num = '7.8.9.4' AND status = 'In development'")
        data = cur.fetchall()
        if len(data) == 0:
            self.assertTrue(False)
        else:
            self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
