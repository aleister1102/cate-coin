from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from blockchain import Blockchain, Transaction

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
blockchain = Blockchain()


@app.route("/")
def home_page():
    return "This is the homepage of the API, write the document here 🤓!"


@app.route('/get-chain', methods=['GET'])
def handle_get_chain() -> Response:
    response = {
        "chain": [block.to_dict() for block in blockchain.chain],
        "transactions_queue": [transaction.to_string() for transaction in blockchain.transactions_queue],
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/add-transactions', methods=['POST'])
def handle_add_transactions() -> Response:
    transactions: list[dict] = request.json['transactions'] if 'transactions' in request.json else []
    transactions_keys = ["sender", "receiver", "amount", "change"]

    num_of_transactions = len(transactions)
    if num_of_transactions == 0:
        return "No transactions found 😔", 400
    else:
        response = {
            "message": f"Your transaction will be added to the blockchain soon 😉"
        }

    for transaction in transactions:
        if not all(key in transaction for key in transactions_keys):
            return f"Some elements of the transaction {transaction} are missing 🤨", 400

        blockchain.add_transaction(
            Transaction(
                transaction['sender'],
                transaction['receiver'],
                transaction['amount'],
                transaction['change']
            )
        )

    return jsonify(response), 201


@app.route('/mine-block', methods=['GET'])
def handle_mine_block() -> Response:
    miner = request.remote_addr
    mining_result, mining_message = blockchain.mine_block(miner)

    response = {"message": mining_message}

    if mining_result is True:
        response["block"] = blockchain.get_latest_block().to_dict()
        return jsonify(response), 200
    else:
        return jsonify(response), 400


@app.route('/is-valid', methods=['GET'])
def handle_is_valid():
    validity, error = blockchain.is_valid()

    response = {
        "message": "The blockchain is valid 😄" if validity else "The blockchain is not valid 😰"}

    if error is None:
        return jsonify(response), 200
    else:
        response['error'] = error
        return jsonify(response), 400


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=8080, debug=True)
