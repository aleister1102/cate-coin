#pragma once
#include <cstdint>
#include <vector>
#include "Block.h"

using namespace std;

class Blockchain {
public:
	Blockchain();

	void addBlock(Block newBlock);
private:
	uint32_t difficulty;

	vector<Block> chain;

	Block getLatestBlock() const;
};