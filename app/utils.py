import os
import uuid

def random_filename(filename):
    extension = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + extension
    return new_filename