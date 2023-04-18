#pragma once
# include <iostream>
# include <sstream>
# include <ctype.h>
# include <cstdlib> // for rand()
#include <iomanip>
#include <string>
#include "SHA256.h"
using namespace std;

class Transaction {
public:
    Transaction();
    ~Transaction();
    Transaction(int a, string s, string r, Transaction* p);

    int getAmount();
    string getNonce();
    string getHash();
    string getSender();
    string getReceiver();
    Transaction* getPrevious();

private:
    Transaction* prev;
    string sender;
    string receiver;
    int amount;
    string nonce;
    string hash;
};