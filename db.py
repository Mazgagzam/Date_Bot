from mazga_db import MazgaDB

db = MazgaDB("users.mazga")

#db.create_table("users", {"id": "INT", "name": "TEXT", "username": "TEXT"})

print(db.read_table("users"))