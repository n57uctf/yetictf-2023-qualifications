CREATE TABLE IF NOT EXISTS users (
	_user serial PRIMARY KEY,
	login text UNIQUE NOT NULL,
	password text NOT NULL
);
CREATE TABLE IF NOT EXISTS links (
	_link serial PRIMARY KEY,
	owner int NOT NULL,
	name text NOT NULL,
	intercept_link text NOT NULL UNIQUE,
	FOREIGN KEY (owner) REFERENCES users(_user)
);
CREATE TABLE IF NOT EXISTS interceptions (
	_interception serial PRIMARY KEY,
	link text NOT NULL,
	ip_address text NOT NULL,
	user_agent text,
	FOREIGN KEY (link) REFERENCES links(intercept_link)
);
