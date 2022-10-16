INSERT INTO interceptions (link, ip_address) VALUES (%s, %s)
RETURNING _interception, link, ip_address;
