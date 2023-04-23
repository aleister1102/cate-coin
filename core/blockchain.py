import hashlib
from datetime import datetime, timedelta

class Block:
    def __init__(self, data: str):
        self.data = data
        self.prev_hash = ""
        self.nonce = 0
        self.hash = ""
        self.total_time = 0

def hash(block: Block) -> str:
    data = block.prev_hash + block.data + str(block.nonce)
    data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        
        block = Block("Genesis Block")
        block.hash = hash(block)

        self.chain.append(block)

    def add_block(self, data):
        block = Block(data)
        block.prev_hash = self.chain[-1].hash
        block.hash = hash(block)
        start = datetime.now()
        while block.hash.startswith("0" * self.difficulty) == False:
            block.nonce += 1
            block.hash = hash(block)   
        end = datetime.now()

        block.total_time = str(end - start)
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            if current_block.hash != hash(current_block):
                return False
            
            if current_block.prev_hash != prev_block.hash:
                return False
        
        return True

    def print(self):
        for block in self.chain:
            print("Data: ", block.data)
            print("Previous hash:", block.prev_hash)
            print("Hash: ", block.hash)
            print("Nonce: ", block.nonce)
            print("Total time: ", block.total_time)
            print()

# blockchain = Blockchain()
# blockchain.add_block("Pikachu")
# blockchain.add_block("Bulbasaur")
# blockchain.add_block("Charmander")
# blockchain.print()