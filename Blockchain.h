#pragma once
#include "Block.h"
#include"Transaction.h"
#include <vector>

using namespace std;

class Blockchain {
public:
	Blockchain();
	~Blockchain();
	void addBlock(Block newBlock);
	void addTransaction(int amount, string sender, string receiver);
	int getBalance(string person); // returns balance of a specific person
	void printChain(); //prints chain
	void printChainHelper(Transaction* n);
private:
	uint32_t difficulty;
	
	Transaction* n;

	vector<Block> chain;

	Block getLatestBlock() const;
};