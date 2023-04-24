from datetime import datetime
from utils import hash, merkle_root, KeyPairs, Signature


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, change: int = 0) -> None:
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: int = amount
        self.change: int = change
        self.content: str = ""
        self.generate_content()
    
    def generate_content(self):
        self.content = f'{self.receiver} <- {self.amount}'
        if self.change > 0:
            self.content += f', {self.sender} <- {self.change}'

    @staticmethod
    def to_string(transactions: list) -> str:
        return ' || '.join([transaction.content for transaction in transactions])

class Block:
    def __init__(self, transactions: list[Transaction] = []):
        # Body
        self.transactions: list[Transaction] = transactions

        # Header
        self.previous_hash: str = ""
        self.merkle_root_hash = self.compute_merkle_root()
        self.timestamp: str = str(datetime.now())
        self.target: int = 4
        self.nonce: int = 0

        # Hash
        self.hash: str = ""

    def print(self) -> None:
        border = "+--------------------------------------------------------------------------------------------+"
        padding = len(border) - 1
        print(border)
        print(f"|Previous hash: {self.previous_hash}".ljust(padding, " ") + "|")
        print(f"|Merkle root hash:  {self.merkle_root_hash}".ljust(padding, " ") + "|")
        print(f"|Timestamp:  {self.timestamp}".ljust(padding, " ") + "|")
        print(f"|Nonce:  {self.nonce}".ljust(padding, " ") + "|")
        print(f"|Hash:  {self.hash}".ljust(padding, " ") + "|")
        print(border)
        print(f"|Transactions:  {Transaction.to_string(self.transactions)}".ljust(padding, " ") + "|")
        print(border)
        print()

    def compute_merkle_root(self) -> str:
        transactions = map(lambda transaction: transaction.content, self.transactions)
        return merkle_root(transactions)
       
    def compute_hash(self) -> str:
        payload = self.previous_hash + self.merkle_root_hash + self.timestamp + str(self.nonce)
        return hash(payload).hex()

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.transactions_queue: list[Transaction] = []
        self.block_capacity: int = 3

        genesis_block = Block()
        genesis_block.hash = Block.compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def add_transactions(self, transactions: list[Transaction]) -> None:
        self.transactions_queue += transactions

    def get_transactions(self) -> list[Transaction]:
        return self.transactions_queue
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> str:
        hash = block.compute_hash()
        while hash.startswith(block.target * "0") is False:
            block.nonce += 1
            hash = block.compute_hash()
        return hash

    def add_block(self, transactions: list[Transaction]) -> None:
        block = Block(transactions)
        block.previous_hash = self.get_latest_block().hash
        block.hash = self.proof_of_work(block)

        self.chain.append(block)
     
    def mine_block(self, miner: str) -> None:
        transactions: list[Transaction] = []
        while len(transactions) < self.block_capacity - 1 and len(self.transactions_queue) > 0:
            transactions.append(self.transactions_queue.pop(0))
        transactions.append(Transaction("Owner", miner, 10)) # Reward

        self.add_block(transactions)

    def print(self):
        for block in self.chain: 
            block.print()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.previous_hash != prev_block.hash:
                print("Previous hash is not equal to the hash of the previous block")
                return False

            if current_block.merkle_root_hash != current_block.compute_merkle_root():
                print("Merkle root hash is not equal to the computed merkle root hash")
                return False

            if current_block.hash != current_block.compute_hash():
                print("Hash is not equal to the computed hash")
                return False

            if current_block.hash.startswith(current_block.target * "0") == False:
                print("Hash does not meet the difficulty target")
                return False

        return True

    def get_balance(self, person: str) -> int:
        balance = 0
        for block in self.chain:
            if type(block.transactions) is not list:
                continue
            for transaction in block.transactions:
                if transaction.sender == person:
                    balance -= (transaction.amount - transaction.change)
                if transaction.receiver == person:
                    balance += (transaction.amount - transaction.change)
        return balance


if __name__ == '__main__':
    blockchain = Blockchain()

    # Add transactions
    blockchain.add_transactions([
        Transaction("Alice", "Bob", 40, 60)
    ])
    blockchain.add_transactions([
        Transaction("Eve", "Bob", 60, 55)
    ])
    blockchain.add_transactions([
        Transaction("Alice", "Bob", 100, 30),
        Transaction("Bob", "Charlie", 60, 20),
        Transaction("Charlie", "Alice", 50, 10)
    ])
    blockchain.add_transactions([
        Transaction("Bob", "Alice", 30, 5),
        Transaction("Alice", "Charlie", 40, 70),
        Transaction("Charlie", "Bob", 55, 90),
    ])

    # Mine blocks
    blockchain.mine_block("Aleister")
    blockchain.mine_block("Injoker")

    # Print blockchain
    blockchain.print()
    
    # Check validity
    print(f'Validity of the blockchain: ', blockchain.is_valid())