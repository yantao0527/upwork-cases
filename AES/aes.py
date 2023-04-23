import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

#CBC with Fix IV

#FIX IV
_iv_ =  'BBBBBBBBBBBBBBBB'.encode('utf-8') #16 char for AES128

def aes_encrypt(data,key):
        data= pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,_iv_)
        return base64.b64encode(cipher.encrypt(data))

def aes_decrypt(enc,key):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, _iv_)
        return unpad(cipher.decrypt(enc),16)


if __name__ == '__main__':
    data = 'I love you'
    key = 'AAAAAAAAAAAAAAAA' #16 char for AES128

    encrypted = aes_encrypt(data,key)
    print('encrypted CBC base64 : ',encrypted.decode("utf-8", "ignore"))

    decrypted = aes_decrypt(encrypted,key)
    print('data: ', decrypted.decode("utf-8", "ignore"))