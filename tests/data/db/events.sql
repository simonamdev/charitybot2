DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE,
	`state` TEXT NOT NULL DEFAULT `REGISTERED`
);
INSERT INTO `events` (id, name) VALUES (1, 'event_one');
INSERT INTO `events` (id, name) VALUES (2, 'event_two');