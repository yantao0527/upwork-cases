const crypto = require("crypto");

const algorithm = "aes-128-cbc";
const _iv_ = "BBBBBBBBBBBBBBBB";

function aes_encrypt(data, key) {
    const cipher = crypto.createCipheriv(algorithm, key, _iv_);
    let enc = cipher.update(data, "utf8", "base64") + cipher.final('base64');
    return enc;
}

function aes_decrypt(enc, key) {
    const decipher = crypto.createDecipheriv(algorithm, key, _iv_);
    var data = decipher.update(enc, "base64", "utf8");
    return data + decipher.final("utf8");
}

module.exports = {
    aes_encrypt,
    aes_decrypt
}
