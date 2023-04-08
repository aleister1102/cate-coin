#include "BlockChain.h"

int main()
{
	Blockchain chain = Blockchain();

	cout << "Mining block 1..." << endl;
	chain.addBlock(Block(1, "Block 1's Data"));

	return 0;
}