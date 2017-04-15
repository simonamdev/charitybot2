PRAGMA writable_schema = 1;
DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger');
PRAGMA writeable_schema = 0;
VACUUM;
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
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (5, 1477257000, 40, 5.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (6, 1477257025, 42, 2.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (7, 1477257300, 52, 10.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (8, 1477257980, 73, 21.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (9, 1477258000, 106.3, 33.3);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (10, 1477258100, 115.06, 8.76);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (11, 1477258222, 121, 5.94);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (12, 1477258505, 160, 39.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (13, 1477258631, 180, 20.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (14, 1477258844, 222, 42.0);
INSERT INTO `test` (id, timestamp, amount, delta) VALUES (15, 1477258999, 230.5, 8.5);