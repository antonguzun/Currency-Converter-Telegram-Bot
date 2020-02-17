from models import db, Rate

db.connect()
db.create_tables(
    [Rate,]
)
