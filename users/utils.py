import uuid


def get_random_number():
    number = str(uuid.uuid4())[:8].replace('-', '').lower()
    return number
