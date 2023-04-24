import hashlib
from pymerkle import MerkleTree
from ecdsa import SigningKey, VerifyingKey, SECP256k1


def hash(data) -> bytes:
    data = data.encode('utf-8')
    return hashlib.sha256(data).digest()

def merkle_root(values: list[str]) -> str:
    tree = MerkleTree()
    for value in values:
        tree.append_entry(value)
    return tree.root.decode() if tree.root else ""

class KeyPairs:
    def __init__(self, signing_key: SigningKey, verifying_key: VerifyingKey) -> None:
        self.signing_key: SigningKey = signing_key
        self.verifying_key: VerifyingKey = verifying_key
        self.signing_key_hex = signing_key.to_string().hex()
        self.verifying_key_hex = verifying_key.to_string().hex()

    def to_string(self) -> str:
        return f'Signing key: {self.signing_key_hex}\nVerifying key: {self.verifying_key_hex}'

    @staticmethod
    def to_signing_key(signing_key_hex: str) -> SigningKey:
        return SigningKey.from_string(bytes.fromhex(signing_key_hex), curve=SECP256k1)

    @staticmethod
    def to_verifying_key(verifying_key_hex: str) -> VerifyingKey:
        return VerifyingKey.from_string(bytes.fromhex(verifying_key_hex), curve=SECP256k1)

class DigitalSignature:
    @staticmethod
    def generate_signing_key() -> SigningKey:
        return SigningKey.generate(curve=SECP256k1)

    @staticmethod
    def generate_verifying_key(signing_key: SigningKey) -> VerifyingKey:
        return signing_key.get_verifying_key()

    @staticmethod
    def generate_keys() -> KeyPairs:
        signing_key = DigitalSignature.generate_signing_key()
        verifying_key = DigitalSignature.generate_verifying_key(signing_key)
        return KeyPairs(signing_key, verifying_key)

    @staticmethod
    def sign(signing_key_hex: str, message: str) -> str:
        signing_key = KeyPairs.to_signing_key(signing_key_hex)
        return signing_key.sign(hash(message)).hex()
    
    @staticmethod
    def verify(verifying_key_hex: str, signature: str, message: str) -> bool:
        try:
            verifying_key = KeyPairs.to_verifying_key(verifying_key_hex)
            verifying_key.verify(bytes.fromhex(signature), hash(message))
            return True
        except:
            return False
        
if __name__ == '__main__':
    keys = DigitalSignature.generate_keys()
    print(keys.to_string())

    message = 'Hello world!'
    signature = DigitalSignature.sign(keys.signing_key_hex, message)
    print(f'Signature of {message}: {signature}')

    print(f'Verification of {message}: {DigitalSignature.verify(keys.verifying_key_hex, signature, message)}')

