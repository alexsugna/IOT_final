from flask import Flask, request, jsonify
import s3, face_recognition, http_utils, config
import requests

app = Flask(__name__)

"""
BEGIN ORIGINAL METHODS
"""
@app.route('/create_personGroup', methods=['POST', 'GET'])
def create_PersonGroup():
    try:
        personGroup_name = request.args.get('personGroup_name')
        description = request.args.get('description')
        create_result = face_recognition.create_PersonGroup(personGroup_name, description)
        if create_result[0] is None:
            data = {"error" : "Something went wrong. Make sure you include arguments 'personGroup_name' and 'description'. It's also possible that you are creating a personGroup with a duplicate name. To check all personGroup names use /list_personGroups."}
            return jsonify(data), 400
        data = {"message" : "personGroup {} created successfully.".format(personGroup_name)}
        return jsonify(data), 200
    except:
        data = {"error" : "Something went wrong. Make sure you include arguments 'personGroup_name' and 'description'. It's also possible that you are creating a personGroup with a duplicate name. To check all personGroup names use /list_personGroups."}
        return jsonify(data), 400


@app.route('/add_person_to_personGroup', methods=['POST', 'GET'])
def add_person_to_personGroup():
    try:
        person_name = request.args.get('person_name')
        personGroup_name = request.args.get('personGroup_name')
        filename = http_utils.generate_ID(id_len=10) + '.jpg'
        if not extract_image(request, filename):
            data = {"error" : "Image not found in request."}
            return jsonify(data), 400
        if upload(filename):
            image_url = config.s3_endpoint + 'uploads/' + filename
            face_recognition.add_person_to_PersonGroup(person_name, personGroup_name, image_url)
            if not s3.delete('uploads/' + filename):
                print("{} not deleted from S3".format(filename))
            if not local_delete(filename):
                print("{} not deleted locally".format(filename))
            data = {"message" : "{} successfully added to {}".format(person_name, personGroup_name)}
            return jsonify(data), 200
        data = {"error" : "Image was not uploaded properly to S3, person add failed."}
        return jsonify(data), 500
    except:
        data = {"error" : "Something went wrong. Make sure you include arguments 'person_name' and 'personGroup_name'."}
        return jsonify(data), 400


@app.route('/delete_personGroup', methods=['POST', 'GET'])
def delete_personGroup():
    try:
        personGroup_name = request.args.get('personGroup_name')
        face_recognition.delete_PersonGroup(personGroup_name)
        data = {"message" : "personGroup {} deleted successfully."}
        return jsonify(data), 200
    except:
        data = {"error" : "Something went wrong. Make sure you include argument 'personGroup_name'."}
        return jsonify(data), 400


@app.route('/identify_person', methods=['POST', 'GET'])
def identify_person():
    try:
        personGroup_name = request.args.get('personGroup_name')
        filename = http_utils.generate_ID(id_len=10) + '.jpg'
        if not extract_image(request, filename):
            return "Image not found in request."
        if upload(filename):
            image_url = config.s3_endpoint + 'uploads/' + filename
            print('personGroup_name: ', personGroup_name)
            print('image_url: ', image_url)
            num_faces, identified = face_recognition.identify_person(personGroup_name, image_url)
            if not s3.delete('uploads/' + filename):
                print("{} not deleted from S3".format(filename))
            if not local_delete(filename):
                print("{} not deleted locally".format(filename))
            if identified:
                data = {"message" : "Person in personGroup {} successfully identified.".format(personGroup_name)}
                return jsonify(data), 200
            data = {"message" : "No one in {} identified.".format(personGroup_name)}
            return jsonify(data), 200
    except:
        data = {"error" : "Something went wrong. Make sure you include argument 'personGroup_name' and json formatted image."}
        return jsonify(data), 400


@app.route('/list_personGroups', methods=['POST', 'GET'])
def list_personGroups():
    try:
        data = {"personGroups" : face_recognition.list_PersonGroups()}
        return jsonify(data), 200
    except:
        data = {"error" : "Something went wrong."}
        return jsonify(data), 400

"""
END ORIGINAL METHODS
"""
"""
BEGIN ESP METHODS
"""
@app.route('/initiate_check', methods=['POST', 'GET'])
def initiate_check():
    try:
        data = {"message" : "check initiated"}
        return jsonify(data)
    except:
        data = {"error" : "Something went wrong."}
        return jsonify(data), 400


@app.route('/verify_coords', methods=['POST', 'GET'])
def verify_coords():
    try:
        lat = request.args.get('lat')
        long = request.args.get('long')
        lat_long_response = requests.get(config.android_endpoint + 'insert_get_coords_from_android_method_here')
        """
        decode lat_long_response here
        """
        android_lat = lat
        android_long = long
        verified = False
        if compare_coords(lat, long, android_lat, android_long):
            verified = True
        data = {"verified" : verified}
        return jsonify(data), 200
    except:
        data = {"error" : "Something went wrong."}
        return jsonify(data), 400


@app.route('/initiate_image_transfer', methods=['POST', 'GET'])
def initiate_image_transfer():
    try:
        data = {
            "server_ip" : config.ec2_public_ip,
            "upload_port" : config.ec3_upload_port
        }
        esp_response = requests.post(config.esp_endpoint, json=data)
        if esp_response.ok:
            filename = receive.receive_from_esp("uploads/" + http_utils.generate_ID(10))
            data = {"message" : "image transferred"}
            return jsonify(data), 200
        data = {"error" : "Image transfer failed"}
        return jsonify(data), 500
    except:
        data = {"error" : "Something went wrong."}
        return jsonify(data), 400
"""
END ESP METHODS
"""
"""
BEGIN HELPER FUNCTIONS
"""
def upload(filename):
    """
    Makes 10 attempts to upload image to S3 server. Returns true if image is
    uploaded successfully, false if not
    """
    uploaded = False
    attempts = 0
    while (not uploaded) and (attempts < 10):
        uploaded = s3.upload('uploads/' + filename)
        attempts += 1
    return uploaded


def extract_image(request, filename):
    """
    Extracts and saves image found in request. If image is found and saved,
    returns True, if not returns False.
    """
    if 'file' not in request.files:
        return False
    image = request.files['file']
    image.save(os.path.join('uploads', filename))
    return True


def local_delete(filename):
    try:
        os.remove('uploads/' + filename)
        return True
    except:
        return False

def compare_coords(lat, long, android_lat, android_long):
    if abs(lat - android_lat) < 1e-3: # a little more than 100 m difference
        if abs(long - android_long) < 1e-3:
            return True
    return False

"""
END HELPER FUNCTIONS
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0')
