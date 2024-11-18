import secrets
import argon2
import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from libwardenpy.colors import colored_string


def add_password(username: str, master_password: str, site: str, password: str):
    """Add an encrypted password for a site."""
    key = authenticate_user(username, master_password)
    if not key:
        return
    # Generate a random nonce
    nonce = secrets.token_bytes(12)
    # Create cipher instance
    cipher = ChaCha20Poly1305(key)
    # Encrypt the password
    encrypted_password = cipher.encrypt(nonce, password.encode(), None)
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute(
            "INSERT INTO passwords (username, site, encrypted_password, nonce) VALUES (?, ?, ?, ?)",
            (username, site, encrypted_password, nonce),
        )
    print(f"Password for {site} stored successfully!")


def get_password(username: str, master_password: str, site: str):
    """Retrieve and decrypt password for a site."""
    key = authenticate_user(username, master_password)
    if not key:
        return
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.execute(
            "SELECT site, encrypted_password, nonce FROM passwords WHERE username = ? AND site LIKE ?",
            (username, f"%{site}%"),
        )
        result = cursor.fetchall()
        # new_result = cursor.fetchall()

        if not result:
            print(f"No password found for {site}")
            return

        for entryies in result:
            site, encrypted_password, nonce = entryies
            cipher = ChaCha20Poly1305(key)
            try:
                decrypted_password = cipher.decrypt(nonce, encrypted_password, None)
                print(
                    f"----------\nsite: {colored_string(site, 'BLUE')}\npassword: {colored_string(decrypted_password.decode('utf-8'), 'RED')}"
                )
            except Exception as e:
                print(f"Error decrypting password: {e}")
                return None


def list_passwords(username: str, master_password: str):
    """Retrieve and decrypt password for a site."""
    key = authenticate_user(username, master_password)
    if not key:
        return
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.execute(
            "SELECT encrypted_password, nonce, site FROM passwords WHERE username = ?;",
            (username,),
        )
        result = cursor.fetchall()
        if not result:
            print(f"No password found for {username}")
            return
        cipher = ChaCha20Poly1305(key)
        for entry in result:
            encrypted_password, nonce, site = entry
            try:
                decrypted_password = cipher.decrypt(nonce, encrypted_password, None)
                print(
                    f"----------\nsite: {colored_string(site, 'BLUE')}\npassword: {colored_string(decrypted_password.decode('utf-8'), 'RED')}"
                )
            except Exception as e:
                print(f"Error decrypting password: {e}")


def register_user(username: str, master_password: str):
    salt = secrets.token_bytes(16)
    # Hash the master password for authentication
    password_hash = argon2.PasswordHasher().hash(master_password)
    try:
        with sqlite3.connect("db.sqlite3") as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )
        print(f"User {username} registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")


def authenticate_user(username: str, master_password: str):
    """Authenticate user and return encryption key if successful."""
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        if not result:
            print("User not found!")
            exit()
        stored_hash, salt = result
        try:
            argon2.PasswordHasher().verify(stored_hash, master_password)
            # If verification succeeds, derive the encryption key
            return derive_key(master_password, salt)
        except argon2.exceptions.VerifyMismatchError as err:
            print(f"Incorrect password! {err}")
            return None


def derive_key(master_password: str, salt: bytes):
    """Derive encryption key from master password using Argon2. using ARGON2ID versino"""
    hasher = argon2.low_level.hash_secret_raw(
        secret=master_password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=argon2.low_level.Type.ID,
    )
    return hasher
