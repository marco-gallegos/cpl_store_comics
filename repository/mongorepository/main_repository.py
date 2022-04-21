import pymongo
from passlib.hash import pbkdf2_sha256 as sha256
from config.config import APP_CONFIG

client = \
    pymongo.MongoClient(APP_CONFIG['MONGO_URL'])

db = client.coppel

# db.users.insert_one(new_user)

# print(db.users.find_one())


def store_comic(comic):
    try:
        db.user_comics.insert_one(comic)
        return True
    except Exception as e:
        print(e)


