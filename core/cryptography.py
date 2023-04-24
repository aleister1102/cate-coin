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

    def get_signing_key_hex(self) -> str:
        return self.signing_key.to_string().hex()
    
    def get_verifying_key_hex(self) -> str:
        return self.verifying_key.to_string().hex()

    def to_string(self) -> str:
        return f'Signing key: {self.get_signing_key_hex()}\nVerifying key: {self.get_verifying_key_hex()}'


class Signature:
    @staticmethod
    def generate_signing_key() -> SigningKey:
        return SigningKey.generate(curve=SECP256k1)

    @staticmethod
    def generate_verifying_key(signing_key: SigningKey) -> VerifyingKey:
        return signing_key.get_verifying_key()

    @staticmethod
    def generate_keys() -> KeyPairs:
        signing_key = Signature.generate_signing_key()
        verifying_key = Signature.generate_verifying_key(signing_key)
        return KeyPairs(signing_key, verifying_key)

    @staticmethod
    def sign(signing_key: SigningKey, message: str) -> str:
        return signing_key.sign(hash(message)).hex()
    
    @staticmethod
    def verify(verifying_key: VerifyingKey, signature: str, message: str) -> bool:
        try:
            verifying_key.verify(bytes.fromhex(signature), hash(message))
            return True
        except:
            return False
        
if __name__ == '__main__':
    keys = Signature.generate_keys()
    print(keys.to_string())

    message = 'Hello world!'
    signature = Signature.sign(keys.signing_key, message)
    print(f'Signature of {message}: {signature}')

    print(f'Verification of {message}: {Signature.verify(keys.verifying_key, signature, message)}')

