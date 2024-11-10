CREATE TABLE IF NOT EXISTS passwords (
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	site TEXT NOT NULL,
	encrypted_password BLOB NOT NULL,
	nonce BLOB NOT NULL,
	FOREIGN KEY (username) REFERENCES users(id)
);
