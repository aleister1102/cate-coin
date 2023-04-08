#include "Block.h"
#include "SHA256.h"

Block::Block(uint32_t index, const string& data) : index(index), data(data) {
	nonce = -1;
	timestamp = time(nullptr);
}
string Block::getHash() {
	return hash;
}

void Block::mineBlock(uint32_t difficulty) {
	char* cstr = new char[difficulty + 1];

	memset(cstr, '0', difficulty);
	cstr[difficulty] = '\0';

	string str(cstr);

	do {
		nonce++;
		hash = calculateHash();
	} while (hash.substr(0, difficulty) != str);

	cout << "Block mined: " << hash << endl;
}

string Block::calculateHash() const {
	stringstream ss;
	ss << index << time << data << nonce << prevHash;

	return SHA256::hash(ss.str());
}