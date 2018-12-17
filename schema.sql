DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL);

INSERT INTO users ( username, name, password ) VALUES ( "Sim4n6", "simo", "AAF4C61DDCC5E8A2DABEDE0F3B482CD9AEA9434D");

SELECT * FROM users WHERE username = "Sim4n6";

SELECT * FROM users ;