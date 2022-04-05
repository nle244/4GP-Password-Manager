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