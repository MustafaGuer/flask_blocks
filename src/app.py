from flask import Flask, render_template, request, redirect
import requests
from typing import List
from models.transaction import Transaction
from models.blockchain import Blockchain
from models.block import Block
from models.mempool import Mempool

app = Flask(__name__)

# Blockchain
blockchain = Blockchain()

# Mempool
# transactions: List[Transaction] = []
transactions = Mempool()


@app.route("/")
def home():
    response = requests.get("https://api.blockchain.com/v3/exchange/tickers/")

    if response.status_code == 200:
        data = response.json()
        return render_template("index.html", coins=data)
    else:
        return render_template(
            "index.html",
            error="Fehler beim laden der aktuellen Daten.",
        )


# Routing
# Methods vorher definieren, sonst 405: Method Not Allowed
@app.route("/transaction", methods=["POST", "GET"])
def transaction_form():
    # Check ob POST-Daten vom Formular vorliegen

    if request.method == "POST":
        print("Formular wurde abgeschickt")

        # Daten verarbeiten
        # Sender von Anfrage an Server abgreifen
        sender = request.form["sender"]  # new_transaction.html: name="sender"
        receiver = request.form["receiver"]
        amount = request.form["amount"]
        # Testausgabe in der Konsole
        # print(sender, receiver, amount)
        if sender == "" or receiver == "" or amount == "":
            return render_template(
                "new_transaction.html", error="Bitte alle Felder ausfüllen!"
            )

        # Transaktion erstellen
        transaction = Transaction(
            len(transactions.pending_transactions), sender, receiver, amount
        )

        # aktuelle Transaktion aus dem Formular in den Mempool übertragen
        # transactions.append("{0} schickt {1} {2} Coins".format(sender, receiver, amount))
        transactions.pending_transactions.append(transaction)

        return render_template(
            "transactions.html",
            transactions=transactions.pending_transactions,
            transactions_there=True,
        )

    else:
        # Formular anzeigen
        return render_template("new_transaction.html")


@app.route("/transactions")
def transactions_page():
    if len(transactions.pending_transactions) > 0:
        return render_template(
            "transactions.html",
            transactions=transactions.pending_transactions,
            transactions_there=True,
        )
    else:
        return render_template(
            "transactions.html",
            transactions=transactions.pending_transactions,
            transactions_there=False,
        )


@app.route("/transactions/<transaction_id>")
def transaction_detail(transaction_id):
    for transaction in transactions.pending_transactions:
        if transaction_id == str(transaction.id):
            return render_template("transaction.html", transaction=transaction)

    return render_template("404.html")
    # return "<h2>{} schickt {} {} Coins</h2>".format(transaction["sender"], transaction["receiver"], transaction["amount"])

    # if transaction in transactions:
    #     return "<h2>{}</h2>".format(transaction)
    # else:
    #     return render_template("404.html")


@app.route("/mine")
def mine():
    global transactions
    block = Block(
        len(blockchain.chain),
        transactions.pending_transactions,
        blockchain.chain[-1].hash,
        2,
    )
    blockchain.add_block(block)
    transactions.pending_transactions = []
    print("MINING DONE")

    return redirect("/blockchain")
    # return render_template("blockchain.html", blokchain_there=True, blockchain=blockchain.blocks)


@app.route("/blockchain")
def blockchain_page():
    return render_template("blockchain.html", blockchain=blockchain.chain)


# Server starten
app.run(debug=True)
