#include "Blockchain.h"

Blockchain::Blockchain() {
	chain.emplace_back(Block(0, "Genesis Block"));
	difficulty = 1; // Tăng độ khó nếu thích
}

void Blockchain::addBlock(Block newBlock) {
	newBlock.prevHash = getLatestBlock().getHash();
	newBlock.mineBlock(difficulty);
	chain.push_back(newBlock);
}

Block Blockchain::getLatestBlock() const {
	return chain.back();
}