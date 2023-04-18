#include "Transaction.h"



Transaction::Transaction() {
    prev = this->getPrevious();
}
Transaction::~Transaction() {
    prev = NULL;
}

int Transaction::getAmount() {
    return this->amount;
}
string Transaction::getSender() {
    return this->sender;
}
string Transaction::getReceiver() {
    return this->receiver;
}
Transaction* Transaction::getPrevious() {
    return this->prev;
}
string Transaction::getNonce() {
    return this->nonce;
}
string Transaction::getHash() {
    return this->hash;
}

Transaction::Transaction(int a, string s, string r, Transaction* p) {
    prev = p;
    sender = s;
    receiver = r;
    amount = a;

    int found = 0;
    srand(time(NULL));
    // While loop will be used to find nonce
    while (found == 0) {
        char first = char(rand() % 26 + 97);
        char second = char(rand() % 26 + 97);
        string nonceGenerated;
        nonceGenerated += first;
        nonceGenerated += second;
        string hashGenerated = SHA256::hash(to_string(this->amount) + this->sender + this->receiver + nonceGenerated);
        if (hashGenerated.back() == '0') {
            found = 1;
            nonce = nonceGenerated;
        }
    }
    // hash will be calciulated using the previous transaction's data
    if (p) {
        this->hash = SHA256::hash(to_string(p->getAmount()) + p->getSender() + p->getReceiver() + p->getHash() + p->getNonce());
    }
    else {
        hash = "NULL";
    }
}