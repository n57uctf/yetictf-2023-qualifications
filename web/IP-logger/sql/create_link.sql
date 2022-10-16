INSERT INTO links (owner, name, intercept_link) VALUES (%s, %s, %s)
RETURNING owner, name, intercept_link;
