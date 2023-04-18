#include "Blockchain.h"

Blockchain::Blockchain() {
	chain.emplace_back(Block(0, "Genesis Block"));
	difficulty = 1; // Tăng độ khó nếu thích
	n = NULL;
}

Blockchain::~Blockchain() {
	Transaction* m = n;
	while (m != NULL) {
		Transaction* n = n;
		n = n->getPrevious();
		delete m;
		m = n;
	}
}

void Blockchain::addBlock(Block newBlock) {
	newBlock.prevHash = getLatestBlock().getHash();
	newBlock.mineBlock(difficulty);
	chain.push_back(newBlock);
}

Block Blockchain::getLatestBlock() const {
	return chain.back();
}


void Blockchain::addTransaction(int amount, string sender, string receiver) {
	Transaction* new1 = new Transaction(amount, sender, receiver, this->n);
	n = new1;
}


int Blockchain::getBalance(string person) {
    //initial Balance
    int total = 50;
    Transaction* p = n;
    while (p != NULL) {
        if (p->getSender() == person) {
            total = total - p->getAmount();
        }
        else if (p->getReceiver() == person) {
            total = total + p->getAmount();
        }
        p = p->getPrevious();
    }
    return total;
}

void Blockchain::printChain() {
    Transaction* p = n;
    printChainHelper(p);
}

void Blockchain::printChainHelper(Transaction* n) {
    if (n == NULL) {
        return;
    }
    printChainHelper(n->getPrevious());
    cout << "Amount: " << n->getAmount() << endl;
    cout << "Sender: " << n->getSender() << endl;
    cout << "Receiver: " << n->getReceiver() << endl;
    cout << "Nonce: " << n->getNonce() << endl;
    cout << "Hash: " << n->getHash() << endl;
}