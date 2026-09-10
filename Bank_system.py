import gradio as gr


class BankAccount:

    account_count = 0

    def __init__(self, name, email, balance):
        self.name = name
        self.email = email
        self._balance = balance
        BankAccount.account_count += 1

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value >= 0:
            self._balance = value
        else:
            print("Balance must be zero or greater.")

    def deposit(self, amount):
        if amount <= 0:
            return "⚠️ Please enter an amount greater than zero."

        self._balance += amount

        return (
            f"✓ Deposit completed successfully.\n"
            f"Added amount: ${amount:.2f}\n"
            f"New balance: ${self.balance:.2f}"
        )

    def withdraw(self, amount):
        if amount <= 0:
            return "⚠️ Please enter an amount greater than zero."

        if amount > self._balance:
            return (
                "⚠️ Transaction could not be completed.\n"
                f"Available balance: ${self.balance:.2f}"
            )

        self._balance -= amount

        return (
            f"✓ Withdrawal completed successfully.\n"
            f"Withdrawn amount: ${amount:.2f}\n"
            f"Remaining balance: ${self.balance:.2f}"
        )

    def display_account(self):
        return (
            f"Customer: {self.name}\n"
            f"Email: {self.email}\n"
            f"Balance: ${self.balance:.2f}"
        )


accounts = []


def create_account(name, email, balance):

    if not name or not email:
        return "⚠️ Please enter both your name and email."

    if "@" not in email or "." not in email.split("@")[-1]:
        return "⚠️ Please enter a valid email address."

    if balance is None:
        return "⚠️ Please enter an opening balance."

    if balance < 0:
        return "⚠️ Opening balance cannot be negative."

    account = BankAccount(
        name=name,
        email=email,
        balance=balance
    )

    accounts.append(account)

    return (
        "✓ Your account has been created!\n\n"
        f"Customer: {account.name}\n"
        f"Email: {account.email}\n"
        f"Balance: ${account.balance:.2f}"
    )


def show_accounts():

    if len(accounts) == 0:
        return "No customer accounts are currently available."

    result = ""

    for index, account in enumerate(accounts, start=1):
        result += (
            f"──────── Account {index} ────────\n"
            f"{account.display_account()}\n\n"
        )

    return result


def get_account(account_number):

    if len(accounts) == 0:
        return None, "No accounts are available."

    if account_number is None:
        return None, "Please select an account number."

    account_number = int(account_number)

    if account_number < 1 or account_number > len(accounts):
        return None, "The selected account number is not valid."

    return accounts[account_number - 1], None


def deposit_money(account_number, amount):

    account, error = get_account(account_number)

    if error:
        return error

    if amount is None:
        return "Please enter the amount you want to deposit."

    return account.deposit(amount)


def withdraw_money(account_number, amount):

    account, error = get_account(account_number)

    if error:
        return error

    if amount is None:
        return "Please enter the amount you want to withdraw."

    return account.withdraw(amount)


def show_account_count():
    return f"Number of registered accounts: {BankAccount.account_count}"


account1 = BankAccount("Alaa", "alaa@gmail.com", 1000)
accounts.append(account1)

account2 = BankAccount("Ahmed", "ahmed@gmail.com", 2000)
accounts.append(account2)

account3 = BankAccount("Mariam", "mariam@gmail.com", 3500)
accounts.append(account3)

account4 = BankAccount("Omar", "omar@gmail.com", 1500)
accounts.append(account4)

account5 = BankAccount("Sara", "sara@gmail.com", 5000)
accounts.append(account5)


with gr.Blocks(
    title="BlueBank",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="blue"
    )
) as app:

    gr.Markdown(
        """
        # 🏦 BlueBank
        ### Simple Banking Management System

        Manage customer accounts, deposits and withdrawals easily.
        """
    )

    with gr.Tab("➕ New Account"):

        gr.Markdown("## Create a New Customer Account")

        name_input = gr.Textbox(
            label="Customer Name",
            placeholder="Enter customer name"
        )

        email_input = gr.Textbox(
            label="Email Address",
            placeholder="example@gmail.com"
        )

        balance_input = gr.Number(
            label="Opening Balance",
            minimum=0
        )

        create_button = gr.Button(
            "Create Account",
            variant="primary"
        )

        create_output = gr.Textbox(
            label="Account Information",
            lines=6
        )

        create_button.click(
            fn=create_account,
            inputs=[
                name_input,
                email_input,
                balance_input
            ],
            outputs=create_output
        )

    with gr.Tab("👥 Customers"):

        gr.Markdown("## Customer Accounts")

        show_accounts_button = gr.Button(
            "View All Customers",
            variant="primary"
        )

        accounts_output = gr.Textbox(
            label="Registered Accounts",
            lines=18
        )

        show_accounts_button.click(
            fn=show_accounts,
            inputs=[],
            outputs=accounts_output
        )

        count_button = gr.Button(
            "Show Account Count"
        )

        count_output = gr.Textbox(
            label="Account Statistics"
        )

        count_button.click(
            fn=show_account_count,
            inputs=[],
            outputs=count_output
        )

    with gr.Tab("💳 Transactions"):

        gr.Markdown("## Account Transactions")

        account_number_input = gr.Number(
            label="Account Number",
            minimum=1,
            precision=0
        )

        amount_input = gr.Number(
            label="Transaction Amount",
            minimum=0
        )

        with gr.Row():

            deposit_button = gr.Button(
                "Deposit",
                variant="primary"
            )

            withdraw_button = gr.Button(
                "Withdraw",
                variant="secondary"
            )

        transaction_output = gr.Textbox(
            label="Transaction Details",
            lines=6
        )

        deposit_button.click(
            fn=deposit_money,
            inputs=[
                account_number_input,
                amount_input
            ],
            outputs=transaction_output
        )

        withdraw_button.click(
            fn=withdraw_money,
            inputs=[
                account_number_input,
                amount_input
            ],
            outputs=transaction_output
        )


app.launch(share=True)

