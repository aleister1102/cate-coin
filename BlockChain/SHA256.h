#pragma once
#include <string>

using namespace std;

class SHA256
{
public:
	template<typename t1, typename t2>
	auto RIGHTROTAGE(t1 x, t2 y) { return (((x) >> (c)) | ((x) << (32 - (c)))); }
	static string hash(string input);
	
};
