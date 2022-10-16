INSERT INTO users (login, password) VALUES (%s, %s)
RETURNING _user, login, password;
