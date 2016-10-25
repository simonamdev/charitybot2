DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE,
	`uuid`	TEXT NOT NULL UNIQUE,
	`state` TEXT NOT NULL DEFAULT `REGISTERED`
);
INSERT INTO `events` (id, name, uuid) VALUES (1, 'event_one', 123456);
INSERT INTO `events` (id, name, uuid) VALUES (2, 'event_two', 123457);