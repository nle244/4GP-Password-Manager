from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


# key
KEYLEN = 32
SALTLEN = 16

# aes
MACLEN = 16
NONCELEN = 32
ROUNDS = 150000

# payload
PAYLOAD_OFFSET = MACLEN + NONCELEN + SALTLEN


class Cryptography:

    def __init__(self):
        # set to empty for now
        self.__passwd_hash = b''
        self.__mac = b''
        self.__nonce = b''
        self.__salt = b''


    @property
    def params(self) -> bytes:
        '''Concatenated cryptographic parameters.

        Returns
            Concatenated bytestring of MAC, nonce, and salt values
        '''
        return self.__mac + self.__nonce + self.__salt


    def __derive_key(self, regenerate=False) -> bytes:
        '''Derive master key from current values in object.

        Params
            regenerate=False: If True, regenerate master key.
        Returns
            key: PBKDF2-derived master key.
        '''
        # salt should be empty if this is the first time encrypting.
        if self.__salt == b'' or regenerate:
            self.__salt = get_random_bytes(SALTLEN)
        key = PBKDF2(
            self.__passwd_hash,         # type: ignore
            self.__salt, KEYLEN,
            count=ROUNDS,
            hmac_hash_module=SHA512
        )
        return key


    def decrypt(self, ciphertext: bytes) -> bytes:
        '''Decrypt ciphertext using current cryptographic parameters via AES-256.

        Params
            ciphertext: bytes object containing ciphertext.
        Returns
            plaintext: bytes object containing decrypted values.
        '''
        return b''


    def encrypt(self, plaintext: bytes) -> bytes:
        '''Encrypt plaintext using current cryptographic parameters via AES-256.

        Params
            plaintext: bytes object containing value to be encrypted.
        Returns
            ciphertext: bytes object containing encrypted values.
        '''
        key = self.__derive_key(regenerate=True)

        self.__nonce = get_random_bytes(NONCELEN)
        cipher = AES.new(key, AES.MODE_EAX, nonce=self.__nonce, mac_len=MACLEN)
        ciphertext, self.__mac = cipher.encrypt_and_digest(plaintext)  # type: ignore
        del key
        return ciphertext


    def parse_params(self, data: bytes) -> int:
        '''Configure this object using raw encrypted password file.

        Params
            data: bytes object containing raw data from encrypted password file.
        Returns
            payload_offset: index of where the actual database payload begins.
        '''
        payload_offset = MACLEN + NONCELEN + SALTLEN
        header = data[:payload_offset]
        if len(header) < payload_offset:
            raise ValueError('Not enough cryptographic parameters.')

        offset = 0
        self.__mac = header[offset : offset+MACLEN]
        offset += MACLEN
        self.__nonce = header[offset : offset+NONCELEN]
        offset += NONCELEN
        self.__salt = header[offset : offset+SALTLEN]
        return payload_offset


    def set_password(self, passwd: str) -> None:
        '''Configure this object using user's password input.

        Params
            passwd: str object containing user's password. Deleted when function completes.
        '''
        sha512 = SHA512.new(truncate='256')
        sha512.update(passwd.encode())
        self.__passwd_hash = sha512.digest()
        del passwd, sha512
