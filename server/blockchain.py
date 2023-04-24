import json
from datetime import datetime
from cryptography import hash, merkle_root


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, change: int = 0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.change = change

    def to_string(self) -> str:
        string = f'{self.sender} -> {self.receiver}: {self.amount}, change: {self.change}'
        return string


class Block:
    def __init__(self, transactions: list[Transaction] = []):
        # Body
        self.transactions = transactions

        # Header
        self.previous_hash = ""
        self.merkle_root_hash = self.compute_merkle_root()  # compute once
        self.timestamp = str(datetime.now())
        self.target = 4
        self.nonce = 0

        # Hash
        self.hash = ""

    def to_dict(self) -> dict:
        dictionary = {
            "previous_hash": self.previous_hash,
            "merkle_root_hash": self.merkle_root_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [transaction.to_string() for transaction in self.transactions]
        }
        return dictionary

    def to_json_string(self) -> str:
        json_string = json.dumps(self.to_dict(), indent=4)
        return json_string

    def compute_merkle_root(self) -> str:
        transactions: list[str] = map(
            lambda transaction: transaction.to_string(), self.transactions)
        return merkle_root(transactions)

    def compute_hash(self) -> str:
        payload = f'{self.previous_hash}{self.merkle_root_hash}{self.timestamp}{str(self.nonce)}'
        return hash(payload).hex()


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.transactions_queue: list[Transaction] = []
        self.block_capacity = 5

        # Rewarding mechanism
        self.reward = 128
        self.interval = 60  # in seconds
        self.timestamp = datetime.now()

        genesis_block = Block()
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions_queue.append(transaction)

    def add_transactions(self, transactions: list[Transaction]) -> None:
        self.transactions_queue.extend(transactions)

    def get_current_reward(self) -> int:
        duration = datetime.now() - self.timestamp
        seconds = int(duration.total_seconds())

        if seconds != 0:
            # Halving every interval seconds
            reward = self.reward / (2 ** int(seconds / self.interval))
        else:
            reward = self.reward

        return int(reward)

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

    def mine_block(self, miner: str) -> tuple[bool, str]:
        if len(self.transactions_queue) < self.block_capacity - 1:
            return False, "Not enough transactions to mine a block"

        transactions: list[Transaction] = [
            Transaction("Owner", miner, self.get_current_reward())]  # rewarding for miner
        while len(transactions) < self.block_capacity:
            transactions.append(self.transactions_queue.pop(0))
        self.add_block(transactions)

        return True, "Mine successfully"

    def print(self):
        for block in self.chain:
            print(block.to_json_string())
            print()

    def is_valid(self) -> tuple[bool, str]:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.previous_hash != prev_block.hash:
                return False, "Previous hash is not equal to the hash of the previous block"

            if current_block.merkle_root_hash != current_block.compute_merkle_root():
                return False, "Merkle root hash is not equal to the computed merkle root hash"

            if current_block.hash != current_block.compute_hash():
                return False, "Hash is not equal to the computed hash"

            if current_block.hash.startswith(current_block.target * "0") is False:
                return False, "Hash does not meet the difficulty target"
            
        return True, None

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
    blockchain.add_transaction(Transaction("Alice", "Bob", 40, 60))
    blockchain.add_transaction(Transaction("Eve", "Bob", 60, 55))
    blockchain.add_transactions([
        Transaction("Alice", "Bob", 100, 30),
        Transaction("Bob", "Charlie", 60, 20),
        Transaction("Charlie", "Alice", 50, 10)
    ])

    # Mine blocks
    blockchain.mine_block("Aleister")
    blockchain.mine_block("Injoker")

    # Print blockchain
    blockchain.print()

    # Check validity
    print(f'Validity of the blockchain: ', blockchain.is_valid())
