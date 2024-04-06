import hashlib
import datetime
import tkinter as tk
from tkinter import ttk
from blockchain import ConsortiumBlockchain
from tkinter import messagebox


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.transactions) + str(
            self.previous_hash)).encode()).hexdigest()


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


class BlockchainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blockchain Interface")

        # Initialize blockchain
        self.blockchain = ConsortiumBlockchain()

        # Create widgets
        self.label = ttk.Label(self, text="Blockchain Information", font=("Arial", 16))
        self.label.pack()

        self.block_listbox = tk.Listbox(self, width=70, font=("Arial", 14))
        self.block_listbox.pack()

        self.transaction_label = ttk.Label(self, text="Transactions:", font=("Arial", 14))
        self.transaction_label.pack()

        self.refresh_button = ttk.Button(self, text="Refresh", command=self.refresh_blocks)
        self.refresh_button.pack()

        self.add_block_button = ttk.Button(self, text="Add Block", command=self.add_block)
        self.add_block_button.pack()

        self.transaction_sender_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_sender_entry.pack()

        self.transaction_recipient_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_recipient_entry.pack()

        self.transaction_amount_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_amount_entry.pack()

        self.add_transaction_button = ttk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.pack()

        self.transaction_text = tk.Text(self, height=10, width=70, font=("Arial", 12))
        self.transaction_text.pack()

        self.update_interface()

    def update_interface(self):
        self.block_listbox.delete(0, tk.END)
        for block in self.blockchain.chain:
            self.block_listbox.insert(tk.END, f"Block {block.index} - Hash: {block.hash}")

    def refresh_blocks(self):
        self.blockchain.update_chain()
        self.update_interface()

    def add_block(self):
        self.blockchain.add_block(self.blockchain.get_latest_block().transactions)
        self.update_interface()

    def add_transaction(self):
        sender = self.transaction_sender_entry.get()
        recipient = self.transaction_recipient_entry.get()
        amount = int(self.transaction_amount_entry.get())
        self.blockchain.add_transaction(sender, recipient, amount)
        self.transaction_sender_entry.delete(0, tk.END)
        self.transaction_recipient_entry.delete(0, tk.END)
        self.transaction_amount_entry.delete(0, tk.END)
        self.update_transaction_display()

    def update_transaction_display(self):
        selected_block_index = self.block_listbox.curselection()[0]  # Get the index of the selected block
        selected_block = self.blockchain.chain[selected_block_index]  # Get the selected block
        self.transaction_text.delete(1.0, tk.END)  # Clear the text widget
        transactions = [f"Sender: {transaction['sender']}, Recipient: {transaction['recipient']}, Amount: {transaction['amount']}"
                        for transaction in selected_block.transactions]
        self.transaction_text.insert(tk.END, "\n".join(transactions))  # Display transactions in the text widget


if __name__ == "__main__":
    app = BlockchainApp()
    app.mainloop()