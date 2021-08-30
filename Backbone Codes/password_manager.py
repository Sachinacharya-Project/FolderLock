from cryptography.fernet import Fernet # pip install cryptography
import bcrypt, os, pickle # Standard library except bcrypt (pip install bcrypt)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def setPassword(password):
    encrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    obj = {
        "password": encrypted
    }
    filepath = os.path.join(BASE_DIR, 'secret.pkl')
    with open(filepath, 'wb') as file:
        pickle.dump(obj, file)
    return True
def checkPassword(password):
    filepath = os.path.join(BASE_DIR, 'secret.pkl')
    if os.path.exists(filepath):
        with open(filepath, 'rb') as file:
            data = pickle.load(file)
        hashed_password = data['password']
        if bcrypt.checkpw(password.encode(), hashed_password):
            return True
        else:
            return False
    else:
        return "no-pass"