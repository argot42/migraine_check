/* config */
PRAGMA foreign_keys = ON;

/* schema */
CREATE TABLE migraine(id INTEGER NOT NULL PRIMARY KEY, start TEXT NOT NULL UNIQUE, end TEXT, duration REAL, intensity INTEGER, comment TEXT);
CREATE TABLE day(date TEXT NOT NULL PRIMARY KEY UNIQUE, sleep_time REAL, comment TEXT);
CREATE TABLE food(id INTEGER PRIMARY KEY, type TEXT NOT NULL UNIQUE, comment TEXT);
CREATE TABLE daily_menu(day_id TEXT NOT NULL, food_id INTEGER NOT NULL, FOREIGN KEY(day_id) REFERENCES day(date), FOREIGN KEY(food_id) REFERENCES food(id));


/* basic population */
INSERT INTO food(type, comment) VALUES ('Carne', 'Carne, Pescado, Huevos, etc');
INSERT INTO food(type, comment) VALUES ('Vegetales', 'Vegetales & Legumbres');
INSERT INTO food(type, comment) VALUES ('Granos', 'Granos, arroz y pasta');
INSERT INTO food(type, comment) VALUES ('Fruta', NULL);
INSERT INTO food(type, comment) VALUES ('Lacteos', 'Leche, Yogurt y Queso');
