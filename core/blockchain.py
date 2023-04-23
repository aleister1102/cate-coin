import json
from datetime import datetime
from utils import compute_hash
from merkle_tree import MerkleTree

class Transaction:
    def __init__(self, from_address="", to_address="", amount=0):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
    
class Block:
    def __init__(self, transactions: list[Transaction]):
        self.prev_hash = ""
        self.transactions = [json.dumps(transaction.__dict__) for transaction in transactions]
        self.nonce = 0
        self.hash = ""
        self.total_time = 0

    def get_transactions(self) -> str:
        return ", ".join(self.transactions)

    def get_hash(self) -> str:
        merkle_tree = MerkleTree(self.transactions)
        merkle_root = merkle_tree.root.hash
        payload = self.prev_hash + merkle_root + str(self.nonce)
        return compute_hash(payload)


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.difficulty = 4

        block = Block([Transaction()])
        block.hash = block.get_hash()

        self.chain.append(block)

    def find_nonce(self, block: Block):
        start = datetime.now()
        while block.hash.startswith(self.difficulty * "0") == False:
            block.nonce += 1
            block.hash = block.get_hash()
        end = datetime.now()
        block.total_time = str(end - start)

    def add(self, value: list[Transaction]):
        block = Block(value)
        block.prev_hash = self.chain[-1].hash
        block.hash = block.get_hash()
        self.find_nonce(block)
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.get_hash():
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

            if current_block.hash.startswith(self.difficulty * "0") == False:
                return False

        return True

    def print(self):
        for block in self.chain:
            print("Previous hash:", block.prev_hash)
            print("Transactions: ", block.get_transactions())
            print("Nonce: ", block.nonce)
            print("Hash: ", block.hash)
            print("Total time: ", block.total_time)
            print()


if __name__ == '__main__':
    transactions = [
        Transaction("A", "B", 1),
        Transaction("B", "C", 2),
        Transaction("C", "D", 3),
    ]
    transactions = [
        Transaction("A", "B", 1),
        Transaction("B", "C", 2),
        Transaction("C", "D", 3),
    ]
    blockchain = Blockchain()
    blockchain.add(transactions)
    blockchain.print()
    print(blockchain.is_valid())
