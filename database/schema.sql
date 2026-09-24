CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL,
  -- Eindeutige Nutzerauthentifizierung
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

