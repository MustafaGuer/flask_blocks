from flask import Flask, render_template, request, redirect

from typing import List
from models.transaction import Transaction
from models.blockchain import Blockchain
from models.block import Block

app = Flask(__name__)

# Blockchain
blockchain = Blockchain()

# Mempool
transactions: List[Transaction] = []


@app.route("/")
def home():
    return render_template("index.html")


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
        print(sender, receiver, amount)

        # Transaktion erstellen
        transaction = Transaction(len(transactions), sender, receiver, amount)

        # aktuelle Transaktion aus dem Formular in den Mempool übertragen
        # transactions.append("{0} schickt {1} {2} Coins".format(sender, receiver, amount))
        transactions.append(transaction)

        return render_template(
            "transactions.html", transactions=transactions, transactions_there=True
        )

    else:
        # Formular anzeigen
        return render_template("new_transaction.html")


@app.route("/transactions")
def transactions_page():
    if len(transactions) > 0:
        return render_template(
            "transactions.html", transactions=transactions, transactions_there=True
        )
    else:
        return render_template(
            "transactions.html", transactions=transactions, transactions_there=False
        )


@app.route("/transactions/<transaction_id>")
def transaction_detail(transaction_id):
    for transaction in transactions:
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
    block = Block(len(blockchain.blocks), transactions, blockchain.blocks[-1].hash, 2)
    blockchain.add_block(block)
    transactions = []
    print("MINING DONE")
    return redirect("/blockchain")
    # return render_template("blockchain.html", blokchain_there=True, blockchain=blockchain.blocks)


@app.route("/blockchain")
def blockchain_page():
    return render_template("blockchain.html", blockchain=blockchain.blocks)


# Server starten
app.run(debug=True)


# Routes /mine und /blockchain definieren
# bei /mine die Liste blockchain[] mit Transaktionen füllen (Liste aus Strings oder Transaktion-Objekte)
# bei /blockchain die Blockchain auslesen (per Konsole oder HTML)


# # Übungsaufgaben

# @app.route("/blockchain")
#     # Blockchain auflisten

# @app.route("/transaktionen")
#     # Mempool anzeigen (offene Transaktion)

# @app.route("/mine")
#     # Prozess anstoßen: Block minen (dabei Mempool aufnehmen und wieder leeren) und neuen Block in BC integrieren
