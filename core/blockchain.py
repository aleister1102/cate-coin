import json
from datetime import datetime
from utils import hash
from pymerkle import MerkleTree


class Block:
    def __init__(self, transactions: list[str] = []):
        # Body
        self.transactions: list[str] = transactions

        # Header
        self.index: int = 0
        self.merkle_root_hash = self.compute_merkle_root()
        self.timestamp: str = str(datetime.now())
        self.target: int = 4
        self.nonce: int = 0
        self.prev_hash: str = ""

    def compute_merkle_root(self) -> str:
        tree = MerkleTree()
        for transaction in self.transactions:
            tree.append_entry(transaction)
        return tree.root.hex() if tree.root else "0"

    def print(self) -> None:
        print("Transactions: ", self.transactions)
        print("Merkle root hash: ", self.merkle_root_hash)
        print("Timestamp: ", self.timestamp)
        print("Nonce: ", self.nonce)
        print("Previous hash:", self.prev_hash)
        print()

    @staticmethod
    def compute_hash(block) -> str:
        payload = block.prev_hash + block.merkle_root_hash + block.timestamp + str(block.nonce)
        return hash(payload)


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.target: int = 4

        block = Block("Genesis Block")
        block.hash = block.compute_hash()

        self.chain.append(block)

    def create_block(self, proof, prev_hash):
        block = Block()

    def proof_of_work(self, block: Block):
        start = datetime.now()
        while block.hash.startswith(self.difficulty * "0") == False:
            block.nonce += 1
            block.hash = block.compute_hash()
        end = datetime.now()
        block.total_time = str(end - start)

    def add(self, transactions: list[dict]):
        block = Block(transactions)
        block.prev_hash = self.chain[-1].hash
        block.hash = block.compute_hash()
        self.proof_of_work(block)
        self.chain.append(block)

    def print(self):
        for block in self.chain:
            print("Hash: ", block.hash)
            print("Previous hash:", block.prev_hash)
            print("Transactions: ", block.transactions)
            print("Nonce: ", block.nonce)
            print("Total time: ", block.total_time)
            print()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

            if current_block.hash.startswith(self.difficulty * "0") == False:
                return False

        return True

    def get_balance(self, person: str) -> int:
        balance = 0
        for block in self.chain:
            if type(block.transactions) is not list:
                continue
            for transaction in block.transactions:
                if transaction["from"] == person:
                    balance -= transaction["amount"]
                if transaction["to"] == person:
                    balance += transaction["amount"]
        return balance


if __name__ == '__main__':
    block = Block()
    block.print()
    print(Block.compute_hash(block))
    # blockchain = Blockchain()
    # blockchain.add([
    #     {"from": "Alice", "to": "Bob", "amount": 1},
    #     {"from": "Bob", "to": "Charlie", "amount": 2},
    #     {"from": "Charlie", "to": "Dave", "amount": 3},
    # ])
    # blockchain.add([
    #     {"from": "Charlie", "to": "Bob", "amount": 5},
    #     {"from": "Bob", "to": "Charlie", "amount": 3},
    #     {"from": "Charlie", "to": "Alice", "amount": 4},
    # ])
    # blockchain.print()

    # print(f'Validity of the blockchain: ', blockchain.is_valid())
    # print()

    # print(f'Balance of Alice: {blockchain.get_balance("Alice")}')
    # print(f'Balance of Bob: {blockchain.get_balance("Bob")}')
    # print(f'Balance of Charlie: {blockchain.get_balance("Charlie")}')
