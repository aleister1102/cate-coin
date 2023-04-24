import json
from datetime import datetime
from core.cryptography import hash, merkle_root


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, change: int = 0) -> None:
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: int = amount
        self.change: int = change
        
    def to_string(self) -> str:
        return f'{self.sender} -> {self.receiver}: {self.amount}, change: {self.change}'

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

    def to_dict(self) -> dict:
        return {
            "previous_hash": self.previous_hash,
            "merkle_root_hash": self.merkle_root_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [transaction.to_string() for transaction in self.transactions]
        }
    
    def to_string(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def compute_merkle_root(self) -> str:
        transactions = map(lambda transaction: transaction.to_string(), self.transactions)
        return merkle_root(transactions)
       
    def compute_hash(self) -> str:
        payload = self.previous_hash + self.merkle_root_hash + self.timestamp + str(self.nonce)
        return hash(payload).hex()

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.transactions_queue: list[Transaction] = []
        self.block_capacity: int = 5

        genesis_block = Block()
        genesis_block.hash = Block.compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions_queue.append(transaction)

    def add_transactions(self, transactions: list[Transaction]) -> None:
        self.transactions_queue.extend(transactions)

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
     
    def mine_block(self, miner: str) -> tuple[str, bool]:
        if len(self.transactions_queue) < self.block_capacity - 1:
            return "Not enough transactions to mine a block", False

        transactions: list[Transaction] = []
        while len(transactions) < self.block_capacity - 1:
            transactions.append(self.transactions_queue.pop(0))
        transactions.append(Transaction("Owner", miner, 10)) # Reward

        self.add_block(transactions)
        return "Mine successfully", True

    def print(self):
        for block in self.chain: 
            print(block.to_string())
            print()

    def is_valid(self) -> tuple[str, bool]:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.previous_hash != prev_block.hash:
                return "Previous hash is not equal to the hash of the previous block", False

            if current_block.merkle_root_hash != current_block.compute_merkle_root():
                return "Merkle root hash is not equal to the computed merkle root hash", False

            if current_block.hash != current_block.compute_hash():
                return "Hash is not equal to the computed hash", False

            if current_block.hash.startswith(current_block.target * "0") == False:
                return "Hash does not meet the difficulty target", False

        return "", True

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
    # Initialize blockchain
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

    # Tamper the blockchain
    blockchain.chain[1].transactions[0].amount = 1000
    blockchain.print()
    
    # Check validity
    print(f'Validity of the blockchain: ', blockchain.is_valid()[1])