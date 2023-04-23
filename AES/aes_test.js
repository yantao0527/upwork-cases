const {aes_encrypt, aes_decrypt} = require('./aes');

function test() {
    const data = "I love you";
    const key = "AAAAAAAAAAAAAAAA";
    
    var enc = aes_encrypt(data, key);
    console.log('encrypted CBC base64 : ' + enc);
    console.log('data: ' + aes_decrypt(enc, key));
}

test();
