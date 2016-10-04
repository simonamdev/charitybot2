DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL UNIQUE,
	`uuid`	INTEGER NOT NULL UNIQUE
);
INSERT INTO `events` (id, name, uuid) VALUES (?, 'event_one', 123456);
INSERT INTO `events` (id, name, uuid) VALUES (?, 'event_two', 123457);