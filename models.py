import json
import datetime
from peewee import Model, SqliteDatabase, DateTimeField, TextField

db = SqliteDatabase("currency_converter.db")


class BaseModel(Model):
    class Meta:
        database = db


class Rate(BaseModel):
    raw_rates = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

    @property
    def rates(self) -> dict:
        return json.loads(self.raw_rates)
