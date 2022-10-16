SELECT
    l.name as name,
    l.intercept_link as link,
    i.ip_address as ip,
    i.user_agent as user_agent
FROM interceptions i
FULL JOIN links l ON l.intercept_link = i.link
FULL JOIN users u ON u._user = l.owner
WHERE u.login = %s
