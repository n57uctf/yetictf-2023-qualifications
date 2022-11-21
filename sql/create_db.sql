CREATE TABLE IF NOT EXISTS users (
	_user serial PRIMARY KEY,
	login text NOT NULL,
	password text NOT NULL
);
CREATE TABLE IF NOT EXISTS files (
	_file serial PRIMARY KEY,
	owner_ int NOT NULL,
	name text NOT NULL,
	content bytea NOT NULL,
	size int NOT NULL,
	create_date timestamp NOT NULL,
	FOREIGN KEY (owner_) REFERENCES users(_user)
);
