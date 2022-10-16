INSERT INTO users (login, password)
VALUES ('admin', '9e77b0bb3e173ada46935bf94d968d2d73e69fab3214df266b4872d1bcffbf96')
RETURNING _user, login, password;
