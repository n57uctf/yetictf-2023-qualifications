SELECT
        u._user as user_id,
        u.login as username,
        u.password as password
    FROM users u
    WHERE u.login = %(user)s