import pytest
from unittest.mock import patch
from pm.cryptography import Cryptography
from pm import exceptions


@pytest.fixture
def mvc():
    crypt = Cryptography()
    return crypt

class Test_Cryptography_encrypt:
    def test_encrypt(self, mvc):
        crypt = mvc
        bytes = b'captian_rex' #create plaintext
        assert crypt.encrypt(bytes) != bytes #test encryption doesnt equal plaintext

class Test_Cryptography_decrypt:
    def test_decrypt(self, mvc):
        crypt = mvc
        bytes = b'cad_bane'
        new_encrypt = crypt.encrypt(bytes) #encrypt the plaintext
        assert crypt.decrypt(new_encrypt) == bytes #decrypt and test to see if it matches plaintext