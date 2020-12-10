import json, os, requests
import db
import config, http_utils

"""
Detect -> Add Face to personGroup
Detect -> Identify person in personGroup
"""

def create_PersonGroup(PersonGroup_name, description):
    """
    creates a personGroup at the azure endpoint
    """
    params = {
        'name' : PersonGroup_name,
        'userData' : description,
        "recognitionModel" : "recognition_03"
    }
    PersonGroupID = http_utils.generate_ID()

    face_api_url = config.face_endpoint + '/face/v1.0/persongroups/' + PersonGroupID
    response = requests.put(face_api_url, json=params,
                             headers=config.face_headers)
    if response.ok:
        result = db.add_PersonGroup(PersonGroup_name, description, PersonGroupID)
        if result:
            print("PersonGroup '{}' created successfully!".format(PersonGroup_name))
            return PersonGroup_name, description, PersonGroupID
        delete_response = requests.delete(face_api_url, headers=config.face_headers)
        if not response.ok:
            print("Please contact admin, db and api out of sync.")
    print("PersonGroup not created.")
    return None, None, None


def delete_PersonGroup(PersonGroup_name):
    """
    delete a PersonGroup
    """
    PersonGroup = db.get_PersonGroup(PersonGroup_name)
    PersonGroupID = list(PersonGroup)[0]['PersonGroupID']
    #remove from DB
    face_api_url = config.face_endpoint + '/face/v1.0/persongroups/' + PersonGroupID
    delete_response = requests.delete(face_api_url, headers=HEADERS)
    if delete_response.ok:
        delete_result = db.delete_PersonGroup(PersonGroup_name)
        if delete_result:
            print("PersonGroup {} successfully deleted!".format(PersonGroup_name))
            return True
    print("PersonGroup not deleted.")
    return False


def list_PersonGroups():
    """
    List all personGroups at endpoint
    """
    face_api_url = config.face_endpoint + '/face/v1.0/persongroups/'
    response = requests.get(face_api_url, headers=config.face_headers)
    PersonGroups = response.json()
    return str(PersonGroups)


def add_person_to_PersonGroup(Person_name, PersonGroup_name, image_url, train=True):
    """
    add a person to a personGroup
    """
    PersonGroup = list(db.get_PersonGroup(PersonGroup_name))[0]
    PersonGroupID = PersonGroup['PersonGroupID']
    params = {
        'name' : Person_name
    }
    face_api_url = config.face_endpoint + '/face/v1.0/persongroups/' + PersonGroupID + '/persons'
    response = requests.post(face_api_url, json=params, headers=config.face_headers)
    if response.ok:
        personID = response.json()['personId']
        add_face_api_url = '{}/face/v1.0/persongroups/{}/persons/{}/persistedFaces'.format(
                            config.face_endpoint, PersonGroupID, personID)
        params = {
            "url" : image_url
        }
        add_face_response = requests.post(add_face_api_url, json=params, headers=config.face_headers)
        if add_face_response.ok:
            if train:
                train_url = '{}/face/v1.0/persongroups/{}/train'.format(config.face_endpoint, PersonGroupID)
                train_response = requests.post(train_url, headers=config.face_headers)
                if train_response.ok:
                    print("{} successfully added to {}".format(Person_name, PersonGroup_name))
                    return True
    print("Person add/train was not successful.")
    return False


def recognize_faces(image_url):
    """
    Detects face(s) in image, returns ID's of each face to then be identified
    param:
        image_url: the url of the image to be analyzed

    returns:
        faceIds of faces in image
    """
    params = {
        'detectionModel': 'detection_01',
        'returnFaceId': 'true',
        'recognitionModel' : 'recognition_03'
    }
    face_api_url = config.face_endpoint + '/face/v1.0/detect'
    response = requests.post(face_api_url, params=params,
                             headers=config.face_headers, json={"url": image_url})
    face_ids = []
    # print("response: ", response.json())
    """
    ADD ERROR HANDLING
    """
    for dict in response.json():
        # print("dict: ", dict)
        face_ids.append(dict['faceId'])
    return face_ids


def identify_face(face_id, PersonGroup_name):
    """
    determine if face_id is in person group
    """
    PersonGroup = list(db.get_PersonGroup(PersonGroup_name))[0]
    PersonGroupID = PersonGroup['PersonGroupID']
    params = {
        'faceIds' : [face_id],
        'personGroupId' : PersonGroupID
    }
    headers = config.face_headers.copy()
    headers.update({'Content-Type' : 'application/json'})
    face_api_url = config.face_endpoint + '/face/v1.0/identify'
    response = requests.post(face_api_url, json=params,
                             headers=config.face_headers)
    return response.content


def identify_person(personGroup_name, image_url):
    face_ids = recognize_faces(image_url)
    num_faces = len(face_ids)
    identified = False
    for face_id in face_ids:
        response = identify_face(face_id, personGroup_name)
        candidates = json.loads(response.decode("UTF-8").strip('][').split(', ')[0])['candidates']
        for candidate in candidates:
            if candidate['confidence'] >= 0.6:
                identified = True
    return num_faces, identified
