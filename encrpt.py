import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

data = b"a secret message"

aad = b"authenticated but unencrypted data"

key = ChaCha20Poly1305.generate_key()
print(f"Key is {key}" )

chacha = ChaCha20Poly1305(key)

nonce = os.urandom(12)
print(f"Nonce is {nonce}")

ct = chacha.encrypt(nonce, data, aad)
print(ct)
print(chacha.decrypt(nonce, ct, aad))
