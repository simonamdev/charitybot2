DROP TABLE IF EXISTS `test`;
DROP TABLE IF EXISTS `test_event`;
CREATE TABLE `test` (
	`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`timestamp`	INTEGER NOT NULL UNIQUE,
	`amount`	REAL NOT NULL UNIQUE,
	`delta`	    REAL NOT NULL UNIQUE
);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (1, 1477256983, 33.2, 11.45);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (2, 1477256990, 34.8, 1.6);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (3, 1477256995, 35, 0.2);
