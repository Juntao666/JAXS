import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SE_DB = 'seDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://annateng8000:{password}'
                                    + '@jaxscluster1.qbdn4.mongodb.net/'
                                    + '?retryWrites=true&w=majority',
                                    connectTimeoutMS=30000,
                                    socketTimeoutMS=None,
                                    connect=False,
                                    maxPoolsize=1)
            # mongodb+srv://annateng8000:<db_password>@jaxscluster1.qbdn4.
            # mongodb.net/?retryWrites=true&w=majority&appName=JAXSCluster1
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def convert_mongo_id(doc: dict):
    if MONGO_ID in doc:
        # Convert mongo ID to a string so it works as JSON
        doc[MONGO_ID] = str(doc[MONGO_ID])


def create(collection, doc, db=SE_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def read_one(collection, filt, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        convert_mongo_id(doc)
        return doc


def delete(collection: str, filt: dict, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    print(f'{filt=}')
    del_result = client[db][collection].delete_one(filt)
    return del_result.deleted_count


def update(collection, filters, update_dict, db=SE_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


# def fetch_all(collection, db=GAME_DB):
#     ret = []
#     for doc in client[db][collection].find():
#         ret.append(doc)
#     return ret


# def fetch_all_as_dict(key, collection, db=GAME_DB):
#     ret = {}
#     for doc in client[db][collection].find():
#         del doc[MONGO_ID]
#         ret[doc[key]] = doc
#     return ret

def read(collection, db=SE_DB, no_id=True) -> list:
    """
    Returns a list from the db.
    """
    ret = []
    for doc in client[db][collection].find():
        if no_id:
            del doc[MONGO_ID]
        ret.append(doc)
    return ret


def read_dict(collection, key, db=SE_DB, no_id=True) -> dict:
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict = {}
    for rec in recs:
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


def close_db():
    global client
    if client is not None:
        client.close()
        client = None
        print("MongoDB connection closed.")
