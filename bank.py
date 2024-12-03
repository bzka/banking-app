import customtkinter as ctk
import pickle
import os


class TransactionTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Transaction Tracker")

        self.data_file = "transaction_data.pkl"
        self.transactions_file = "transactions.txt"
        self.total_amount = self.load_data()

        self.initial_frame = ctk.CTkFrame(master)
        self.initial_frame.pack(pady=10)

        self.initial_label = ctk.CTkLabel(self.initial_frame, text="Set your initial amount:")
        self.initial_label.pack(side=ctk.LEFT)

        self.initial_entry = ctk.CTkEntry(self.initial_frame)
        self.initial_entry.pack(side=ctk.LEFT)

        self.set_button = ctk.CTkButton(self.initial_frame, text="Set Amount", command=self.set_initial_amount)
        self.set_button.pack(side=ctk.LEFT)

        self.transaction_frame = ctk.CTkFrame(master)
        self.transaction_frame.pack(pady=10)

        self.description_label = ctk.CTkLabel(self.transaction_frame, text="Website/Description:")
        self.description_label.pack(side=ctk.LEFT)

        self.description_entry = ctk.CTkEntry(self.transaction_frame)
        self.description_entry.pack(side=ctk.LEFT)

        self.transaction_label = ctk.CTkLabel(self.transaction_frame, text="Transaction Amount:")
        self.transaction_label.pack(side=ctk.LEFT)

        self.transaction_entry = ctk.CTkEntry(self.transaction_frame)
        self.transaction_entry.pack(side=ctk.LEFT)

        self.add_button = ctk.CTkButton(self.transaction_frame, text="Add Transac3wtion", command=self.add_transaction)
        self.add_button.pack(side=ctk.LEFT)

        self.balance_frame = ctk.CTkFrame(master)
        self.balance_frame.pack(pady=10)

        self.balance_label = ctk.CTkLabel(self.balance_frame, text=f"Current Balance: ${self.total_amount:.2f}")
        self.balance_label.pack()

        self.log_frame = ctk.CTkFrame(master)
        self.log_frame.pack(pady=10)

        self.log_label = ctk.CTkLabel(self.log_frame, text="Transaction Log:")
        self.log_label.pack()

        self.log_text = ctk.CTkTextbox(self.log_frame, width=300, height=200)
        self.log_text.pack()
        self.log_text.configure(state='disabled')

        self.show_transactions()

    def set_initial_amount(self):
        try:
            self.total_amount = float(self.initial_entry.get())
            self.balance_label.configure(text=f"Current Balance: ${self.total_amount:.2f}")
            self.initial_entry.delete(0, ctk.END)
            self.save_data()
        except ValueError:
            self.initial_entry.delete(0, ctk.END)

    def add_transaction(self):
        try:
            description = self.description_entry.get()
            transaction_amount = float(self.transaction_entry.get())

            if description and transaction_amount:
                self.total_amount -= transaction_amount 
                self.balance_label.configure(text=f"Current Balance: ${self.total_amount:.2f}")
                self.log_transaction(description, transaction_amount)

                self.description_entry.delete(0, ctk.END)
                self.transaction_entry.delete(0, ctk.END)

                self.save_data()  
                self.show_transactions()
        except ValueError:
            self.transaction_entry.delete(0, ctk.END)

    def log_transaction(self, description, amount):
        with open(self.transactions_file, "a") as f:
            f.write(f"{description}: -${amount:.2f}\n")
    
    def show_transactions(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, ctk.END)  
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, "r") as f:
                transactions = f.readlines()
                for transaction in transactions:
                    self.log_text.insert(ctk.END, transaction)
        self.log_text.configure(state='disabled')

    def save_data(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.total_amount, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                return pickle.load(f)
        return 0.0

if __name__ == "__main__":
    root = ctk.CTk()
    app = TransactionTrackerApp(root)
    root.mainloop()
