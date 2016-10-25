DROP TABLE IF EXISTS `test`;
DROP TABLE IF EXISTS `test_event`;
DROP TABLE IF EXISTS `test_one`;
DROP TABLE IF EXISTS `test_two`;
DROP TABLE IF EXISTS `test_three`;
CREATE TABLE `test` (
	`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`timestamp`	INTEGER NOT NULL,
	`amount`	REAL NOT NULL,
	`delta`	    REAL NOT NULL
);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (1, 1477256983, 33.2, 11.45);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (2, 1477256990, 34.8, 1.6);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (3, 1477256995, 35, 0.2);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (4, 1477256995, 35, 0.0);
