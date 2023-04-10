#include "SHA256.h"

string SHA256::hash(string input)
{
	uint64_t Size = input.size();
	uint64_t new_len;

	//calculate new length
	for (new_len = Size * 8; new_len % 512 != 448; new_len++);
	{
		new_len /= 8;
	}

	//adđ 0 
	input.resize(new_len, '\0');

	//add bit '1' at the end of input
	input[Size] = 0x80;

	//add new length 
	string new_IPSize;
	for (int k = 0; k < 8; k++)
	{
		new_IPSize += (uint8_t)((8 * Size) >> (8 * k));
	}

	for (int i = 7; i >= 0; --i)
	{
		input += new_IPSize[i];
	}
	
	uint32_t h0 = 0x6A09E667;
	uint32_t h1 = 0xBB67AE85;
	uint32_t h2 = 0x3C6EF372;
	uint32_t h3 = 0xA54FF53A;
	uint32_t h4 = 0x510E527F;
	uint32_t h5 = 0x9B05688C;
	uint32_t h6 = 0x1F83D9AB;
	uint32_t h7 = 0x5BE0CD19;

	uint32_t k[64] =
	{
		0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
		0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
		0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
		0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
		0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
		0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
		0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
		0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
	};

        //Seperate into blocks
	for (int i = 0; i < message.size(); i += 64)
	{
		//16 32-bit words are extended to 80 32-bit words
		// 0-15 words dont change
		uint32_t w[64];
		for (int j = 0; j < 16; j++)
		{
			uint32_t temp = 0;
			for (int k = 0; k < 4; k++)
			{
				if ((i + (4 * j) + k) <= message.size())
				{
					temp += ((unsigned char)(message[i + (4 * j) + k])) << (24 - 8 * k);
				}
				else break;
			}
			w[j] = temp;
		}
		//16-79 words are extended and right cycle shifted
		uint32_t s0, s1;
		for (int j = 16; j < 64; j++)
		{
			s0 = rightRotate(w[j - 15], 7) ^ rightRotate(w[j - 15], 18) ^ (w[j - 15] >> 3);
			s1 = rightRotate(w[j - 2], 17) ^ rightRotate(w[j - 2], 19) ^ (w[j - 2] >> 10);
			w[j] = w[j - 16] + s0 + w[j - 7] + s1;
		}
 	        uint32_t a = h0;
		uint32_t b = h1;
		uint32_t c = h2;
		uint32_t d = h3;
		uint32_t e = h4;
		uint32_t f = h5;
		uint32_t g = h6;
		uint32_t h = h7;
		
		// MAIN LOOP
	}
	return string();
}
