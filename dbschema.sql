/* config */
PRAGMA foreign_keys = ON;

/* schema */
CREATE TABLE migraine(id INTEGER NOT NULL PRIMARY KEY, start TEXT NOT NULL UNIQUE, end TEXT, duration REAL, intensity INTEGER, comment TEXT);
CREATE TABLE day(date TEXT NOT NULL PRIMARY KEY UNIQUE, sleep_time REAL, comment TEXT);
CREATE TABLE food(type TEXT PRIMARY KEY NOT NULL UNIQUE, comment TEXT);
CREATE TABLE daily_menu(day_id TEXT NOT NULL, food_id INTEGER NOT NULL, FOREIGN KEY(day_id) REFERENCES day(date), FOREIGN KEY(food_id) REFERENCES food(type));


/* basic population */
INSERT INTO food(type, comment) VALUES ('carne', 'Carne, Pescado, Huevos, etc');
INSERT INTO food(type, comment) VALUES ('vegetales', 'Vegetales & Legumbres');
INSERT INTO food(type, comment) VALUES ('granos', 'Granos, arroz y pasta');
INSERT INTO food(type, comment) VALUES ('fruta', NULL);
INSERT INTO food(type, comment) VALUES ('lacteos', 'Leche, Yogurt y Queso');
