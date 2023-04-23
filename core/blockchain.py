import json
from datetime import datetime
from utils import compute_hash

class Block:
    def __init__(self, transactions: list[dict]):
        self.prev_hash = ""
        self.transactions = json.dumps(transactions)
        self.nonce = 0
        self.hash = ""
        self.total_time = 0

    def get_hash(self) -> str:
        payload = self.prev_hash + self.transactions + str(self.nonce)
        return compute_hash(payload)


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.difficulty = 4

        block = Block("Genesis Block")
        block.hash = block.get_hash()

        self.chain.append(block)

    def find_nonce(self, block: Block):
        start = datetime.now()
        while block.hash.startswith(self.difficulty * "0") == False:
            block.nonce += 1
            block.hash = block.get_hash()
        end = datetime.now()
        block.total_time = str(end - start)

    def add(self, transactions: list[dict]):
        block = Block(transactions)
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
            print("Transactions: ", block.transactions)
            print("Nonce: ", block.nonce)
            print("Hash: ", block.hash)
            print("Total time: ", block.total_time)
            print()


if __name__ == '__main__':
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 1},
        {"from": "Bob", "to": "Charlie", "amount": 2},
        {"from": "Charlie", "to": "Dave", "amount": 3},
    ]
    blockchain = Blockchain()
    blockchain.add(transactions)
    blockchain.print()
    print(blockchain.is_valid())
