# AES

AES (Advanced Encryption Standard) is a symmetric block cipher standardized by NIST. It has a fixed data block size of 16 bytes. Its keys can be 128, 192, or 256 bits long.

AES is very fast and secure, and it is the de facto standard for symmetric encryption.

Encryption and decryption AES128 CBC mode with Fix IV both in Python and in Javascript.

## Python

```
pip install pycryptodome
```

```
python3 aes.py

encrypted CBC base64 :  h+8w4llImQJECTZ3CS1pYw==
data:  I love you
```

## Javascript

Load aes.html into an browser and check console log.

```
encrypted CBC base64 : h+8w4llImQJECTZ3CS1pYw==
data: I love you
```

## Nodejs

```
npm install
```

```
node aes_test.js

encrypted CBC base64 : h+8w4llImQJECTZ3CS1pYw==
data: I love you
```