import requests
import base64
import hashlib
from dataclasses import dataclass


@dataclass
class Session:
    host: str
    salt: bytes
    session_id: str


def login(hostname):
    login_url = f'http://{hostname}/api/login.json'
    ans = requests.get(login_url).json()

    session = Session(hostname, salt=ans['salt'], session_id=ans['session']['sessionId'])
    data = {
        'mode': 1,
        'userId': 'pvserver',
        'pwh': get_pwh(session.salt, b'pvwr')
    }
    ans = requests.post(f'http://{hostname}/api/login.json', data=data, params={'sessionId': session.session_id}).json()
    assert ans['session']['rolId'] == 2
    assert ans['status']['code'] == 0
    print(f'logged in. session id: {session.session_id}')


#print(login('piko'))
def get_pwh(salt: str, password: bytes):

    salt_bytes = base64.b64decode(salt)
    pwh = hashlib.scrypt(password, salt=salt_bytes, n=16, )
    return base64.b64encode(pwh)



login('piko')