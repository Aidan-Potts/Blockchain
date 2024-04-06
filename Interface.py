import tkinter as tk
from tkinter import ttk
from blockchain import ConsortiumBlockchain 
from tkinter import messagebox

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
        
        self.transaction_text = tk.Text(self, height=10, width=70, font=("Arial", 12))
        self.transaction_text.pack()
        
        self.refresh_button = ttk.Button(self, text="Refresh", command=self.refresh_blocks)
        self.refresh_button.pack()
        
        self.add_block_button = ttk.Button(self, text="Add Block", command=self.add_block)
        self.add_block_button.pack()
        
        self.transaction_sender_label = ttk.Label(self, text="Sender:", font=("Arial", 12))
        self.transaction_sender_label.pack()
        self.transaction_sender_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_sender_entry.pack()
        
        self.transaction_recipient_label = ttk.Label(self, text="Recipient:", font=("Arial", 12))
        self.transaction_recipient_label.pack()
        self.transaction_recipient_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_recipient_entry.pack()
        
        self.transaction_amount_label = ttk.Label(self, text="Amount:", font=("Arial", 12))
        self.transaction_amount_label.pack()
        self.transaction_amount_entry = ttk.Entry(self, font=("Arial", 12))
        self.transaction_amount_entry.pack()
        
        self.add_transaction_button = ttk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.pack()
        
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
        amount_str = self.transaction_amount_entry.get()

        try:
            amount = int(amount_str)
        except ValueError:
            # If the input cannot be converted to an integer, show an error message and return
            tk.messagebox.showerror("Error", "Amount must be a valid integer.")
            return

        # Check if any item is selected in the block listbox
        if not self.block_listbox.curselection():
            # If nothing is selected, show an error message and return
            tk.messagebox.showerror("Error", "Please select a block.")
            return

        selected_block_index = self.block_listbox.curselection()[0]
        selected_block = self.blockchain.chain[selected_block_index]

        self.blockchain.add_transaction(sender, recipient, amount)
        self.transaction_sender_entry.delete(0, tk.END)
        self.transaction_recipient_entry.delete(0, tk.END)
        self.transaction_amount_entry.delete(0, tk.END)
        self.update_transaction_display()
    
    def update_transaction_display(self):
        selected_block_index = self.block_listbox.curselection()[0]  # Get the index of the selected block
        selected_block = self.blockchain.chain[selected_block_index]  # Get the selected block
        self.transaction_text.delete(1.0, tk.END)  # Clear the text widget
        for transaction in selected_block.transactions:
            self.transaction_text.insert(tk.END, f"Sender: {transaction['sender']}, Recipient: {transaction['recipient']}, Amount: {transaction['amount']}\n")  # Display transactions in the text widget

if __name__ == "__main__":
    app = BlockchainApp()
    app.mainloop()
