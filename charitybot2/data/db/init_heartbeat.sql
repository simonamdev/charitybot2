CREATE TABLE IF NOT EXISTS `heartbeats` (
    `entryId`   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `source`    TEXT NOT NULL,
    `state`     TEXT NOT NULL,
    `timestamp` INTEGER NOT NULL
);