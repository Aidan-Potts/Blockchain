import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash)).encode()).hexdigest()

class ConsortiumBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = set()  # Set to store participating nodes

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), [], "0")

    def register_node(self, node):
        self.nodes.add(node)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        latest_block = self.get_latest_block()
        new_block = Block(latest_block.index + 1, datetime.datetime.now(), transactions, latest_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def update_chain(self):
        # Logic to update the blockchain from external source (e.g., other consortium members)
        pass

    def add_transaction(self, sender, recipient, amount):
        self.get_latest_block().transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

# The interface code remains the same as you provided
