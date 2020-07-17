import uuid


def get_default_email():
    email = str(uuid.uuid4())
    email = email + '@toraxnet.net'
    return email
