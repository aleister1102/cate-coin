from flask import Flask, jsonify, request
from flask_cors import CORS
from blockchain import Blockchain, Transaction

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/")
def home_page():
    # Write API document here
    return "This is the homepage of the API"

@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {
        "chain": [block.to_dict() for block in blockchain.chain],
        "transactions_queue": [transaction.to_string() for transaction in blockchain.transactions_queue],
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/add-transaction', methods=['POST'])
def post_transaction():
    json = request.json
    transaction_keys = ["sender", "receiver", "amount", "change"]

    if not all(key in json for key in transaction_keys):
        return "Some elements of the transaction are missing", 400
    
    transaction = Transaction(json["sender"], json["receiver"], json["amount"], json["change"])
    blockchain.add_transaction(transaction)

    response = {
        "message": f"This transaction will be added to the blockchain soon"
    }

    return jsonify(response), 201

if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=8080, debug=True)