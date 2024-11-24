# Caesar Cipher

This Python script implements the Caesar Cipher, a type of substitution cipher where each letter in the plaintext is shifted by a certain number of places in the alphabet. This can be used for simple encryption (encoding) or decryption.

## How the Cipher Works:
- Each letter in the message is shifted by a specified number of positions in the alphabet.
- If you want to **encode** a message, it shifts the letters forward in the alphabet by the specified amount.
- If you want to **decode** a message, it shifts the letters backward by the same amount.
- Non-alphabet characters (e.g., spaces, punctuation) are not altered.

## Example:
If the shift number is 3:
- 'a' becomes 'd'
- 'b' becomes 'e'
- 'z' becomes 'c'

## Features:
- Encrypt and decrypt messages with the Caesar Cipher.
- Non-alphabet characters (e.g., spaces, punctuation) are ignored and remain unchanged.
- The user can choose to encode or decode their message.
- The user can specify a shift number for the cipher.

## How to Use:
1. **Run the Python script**:
   ```bash
   python caesar_cipher.py
