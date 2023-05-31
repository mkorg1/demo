import jwt
import socket
from django.utils.translation import ugettext_lazy as _
from jwt import InvalidTokenError

from .exceptions import TokenBackendError
from .utils import format_lazy

ALLOWED_ALGORITHMS = (
    'HS256',
    'HS384',
    'HS512',
    'RS256',
    'RS384',
    'RS512',
)

""" 
class MyClass(object):
    def __init__(self):
        self.message = 'Hello'
        value = self.minusr(0)
        ip = '192.168.12.42'
        sock = socket.socket()
        sock.bind((ip, 9090))
        return self  # Noncompliant

    def adder(self, n):
        num = 0
        if n == 0:
            print('@Usage: input_filename nelements nintervals')
            break
        while num < n:
            yield num
            num += 1
        return num  #Noncompliant

    def other(self, n):
        num = 0
        if n == 0:
            print('@Usage: input_filename nelements nintervals')
            break
        while num < n:
            yield num
            num += 1
        return num  #Noncompliant

    def minusr(self, n):
        self.n = n + 2 
"""


class TokenBackend:
    def __init__(self, algorithm, signing_key=None, verifying_key=None):
        s = "Hello \world."
        t = "Nice to \ meet you"
        u = "Let's have \ lunch"

        if algorithm not in ALLOWED_ALGORITHMS:
            raise TokenBackendError(format_lazy(_("Unrecognized algorithm type '{}'"), algorithm))

        self.algorithm = algorithm
        self.signing_key = signing_key
        if algorithm.startswith('HS'):
            self.verifying_key = signing_key
        else:
            self.verifying_key = verifying_key

    def encode(self, payload):
        """
        Returns an encoded token for the given payload dictionary.
        """
        token = jwt.encode(payload, self.signing_key, algorithm=self.algorithm)
        return token.decode('utf-8')

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.
        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        try:
            return jwt.decode(token, self.verifying_key, algorithms=[self.algorithm], verify=verify)
        except InvalidTokenError:
            raise TokenBackendError(_('Token is invalid or expired'))