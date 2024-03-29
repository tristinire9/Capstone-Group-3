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
        cur.execute("DELETE FROM relationships WHERE id !=11 AND id != 12")
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

    def test_get_a_component_by_ID(self):
        component = normal_db_functions.get_a_component_by_ID(db_file, '22')
        self.assertEqual(component, [22, 'nihao', '1.2.3.5', '2019.10.1', 'www.google.com'])

    def test_all_components_in_a_recipe(self):
        result_list = normal_db_functions.all_components_in_a_recipe(db_file, "Hiii", "1.2.3.4")
        self.assertEqual(result_list, [[22, 'nihao', '1.2.3.5', '2019.10.1', 'www.google.com', '/tttt', False], [24, '1heyhey', '1.4.8.9', '2019.10.3', 'www.hhhh.com', '/tttt', False]])

    def test_is_folder_empty_1(self):
        self.assertEqual(normal_db_functions.is_folder_empty("D:\hhhh"), True)

    def test_is_folder_empty_2(self):
        self.assertEqual(normal_db_functions.is_folder_empty("../tests"), False)

    def test_are_there_newer_versions_of_this_component_1(self):
        self.assertEqual(normal_db_functions.are_there_newer_versions_of_this_component(db_file, "Thomas", "1.2.3.4"), True)

    def test_are_there_newer_versions_of_this_component_2(self):
        self.assertEqual(normal_db_functions.are_there_newer_versions_of_this_component(db_file, "Thomas", "1.4.3.4"), False)
if __name__ == '__main__':
    unittest.main()
