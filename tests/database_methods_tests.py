import unittest
import normal_db_functions
import sqlite3

class SimpleTest(unittest.TestCase):
    global db_file
    db_file = "../instance/myDB.sqlite"

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


if __name__ == '__main__':
    unittest.main()