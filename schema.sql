
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE members (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  start_year INTEGER NOT NULL,
  member_until DATE NOT NULL,
  home_municipality VARCHAR(255) NOT NULL,
  user_id INTEGER REFERENCES users(id)
);

INSERT INTO users (email, password) VALUES ('admin@admin.com', 'admin');