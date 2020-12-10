import pymongo as p

ROOT_USER = 'admin'
ROOT_PWD = 'password'
SERVER_PUBLIC_IP = '18.222.187.211'

connection_string = "mongodb://{}:{}@{}/admin".format(ROOT_USER, ROOT_PWD, SERVER_PUBLIC_IP)    # string for connecting to mongoDB

def get_client():
    """
    connects to the dayrate database
    """
    client = p.MongoClient(connection_string)                             # use connection string to instantiate client object
    return client.final


def add_PersonGroup(PersonGroup_name, description, PersonGroupID):
    """
    creates a personGroup document
    """
    client = get_client()
    personGroup_collection = client['personGroups']
    check_duplicate_names = personGroup_collection.find({"PersonGroup_name" : PersonGroup_name})
    if len(list(check_duplicate_names)) > 0:
        return False
    result = personGroup_collection.insert_one({ "PersonGroup_name" : PersonGroup_name,
                                                 "description" : description,
                                                 "PersonGroupID" : PersonGroupID})
    return result.acknowledged


def get_PersonGroup(PersonGroup_name):
    """
    return a personGroup document by PersonGroup_name
    """
    client = get_client()
    personGroup_collection = client['personGroups']
    result = personGroup_collection.find({ "PersonGroup_name" : PersonGroup_name })
    return result


def delete_PersonGroup(PersonGroup_name):
    """
    delete a personGroup from the DB
    """
    client = get_client()
    personGroup_collection = client['personGroups']
    result = personGroup_collection.delete_one({ "PersonGroup_name" : PersonGroup_name })
    return result.acknowledged
