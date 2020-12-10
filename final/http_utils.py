import config
import string, secrets


def validate_request(cl):
    """
    Validates the request by analyzing the cl object.
    Returns a response message and response code.
    """
    try:
        data = cl.recv(4096)
        request = data.decode('utf-8')
        return "Request was successful\r\n\r\n", "200 OK", request
    except:
        return "Request was unsuccessful\r\n\r\n", "400 Bad Request", ""


def generate_ID(id_len=config.idlen):
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                                                  for i in range(id_len))
