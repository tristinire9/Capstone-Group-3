import db

connection = db.create_connection("../instance/flaskr.sqlite")



# all_rows = connection.execute(
# #         'SELECT * FROM components'
# #     ).fetchall()
# #
# # rows = ""
# # for row in all_rows:
# #     row = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "\n"
# #     rows = rows + row
# #
# # print(rows)
