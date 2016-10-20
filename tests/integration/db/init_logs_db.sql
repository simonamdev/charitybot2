CREATE TABLE IF NOT EXISTS `test` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`time`	INTEGER NOT NULL,
	`level`	INTEGER NOT NULL DEFAULT 0,
	`event`	TEXT NOT NULL,
	`message`   TEXT NOT NULL
);

INSERT INTO `test` (id, time, level, event, message) VALUES (?, 1476950164, 1, 'test_event', 'bla foo bar whizz fizz buss');