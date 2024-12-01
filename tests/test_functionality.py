import os
import sqlite3
from contextlib import contextmanager

import pytest

from libwardenpy.funtionality import (
    AuthenticatedData,
    Entry,
    UnAuthData,
    add_password,
    authenticate_user,
    delete_passwod,
    get_password,
    list_passwords,
    register_user,
)

# Test database path
TEST_DB = "test_db.sqlite3"


@contextmanager
def get_test_connection():
    conn = sqlite3.connect(TEST_DB)
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: Create test database and tables
    conn = sqlite3.connect(TEST_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt BLOB NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            site TEXT NOT NULL,
            encrypted_password BLOB NOT NULL,
            nonce BLOB NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    conn.close()

    yield

    os.remove(TEST_DB)


def test_register_user():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)

        cursor = conn.execute(
            "SELECT username FROM users WHERE username = ?", (test_user.username,)
        )
        result = cursor.fetchall()
        assert result is not None
        assert len(result) == 1
        assert result[0][0] == test_user.username


def test_register_duplicate_user():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        # Try to register the same user again
        register_user(conn, test_user)
        register_user(conn, test_user)

        cursor = conn.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", (test_user.username,)
        )
        count = cursor.fetchone()
        assert count[0] == 1


def test_authenticate_user():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        key = authenticate_user(conn, test_user)
        assert key is not None


def test_authenticate_wrong_password():
    test_user = UnAuthData("testuser", "testpassword123")
    wrong_pass_user = UnAuthData("testuser", "wrongpassword")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        key = authenticate_user(conn, wrong_pass_user)
        assert key is None


def test_add_and_get_password():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        key = authenticate_user(conn, test_user)
        auth_data = AuthenticatedData(test_user.username, key)

        test_entry = Entry("example.com", "password123")
        add_password(conn, auth_data, test_entry)

        passwords = get_password(conn, auth_data, "example.com")
        assert passwords is not None
        assert len(passwords) == 1
        assert passwords[0][1] == "example.com"
        assert passwords[0][2].decode() == "password123"


def test_list_passwords():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        key = authenticate_user(conn, test_user)
        auth_data = AuthenticatedData(test_user.username, key)

        # Add multiple passwords
        add_password(conn, auth_data, Entry("site1.com", "pass1"))
        add_password(conn, auth_data, Entry("site2.com", "pass2"))

        passwords = list_passwords(conn, auth_data)
        assert passwords is not None
        assert len(passwords) == 2
        assert any(p[0] == "site1.com" and p[1] == "pass1" for p in passwords)
        assert any(p[0] == "site2.com" and p[1] == "pass2" for p in passwords)


def test_delete_password():
    test_user = UnAuthData("testuser", "testpassword123")
    with get_test_connection() as conn:
        register_user(conn, test_user)
        key = authenticate_user(conn, test_user)
        auth_data = AuthenticatedData(test_user.username, key)

        add_password(conn, auth_data, Entry("example.com", "password123"))
        passwords = get_password(conn, auth_data, "example.com")
        if passwords is not None:
            password_id = str(passwords[0][0])
            delete_passwod(conn, auth_data, password_id)

        passwords_after_delete = get_password(conn, auth_data, "example.com")
        assert passwords_after_delete is None
