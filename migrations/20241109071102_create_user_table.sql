CREATE TABLE IF NOT EXISTS users (
	username TEXT PRIMARY KEY,
	password_hash TEXT NOT NULL,
	salt BLOB NOT NULL
);
