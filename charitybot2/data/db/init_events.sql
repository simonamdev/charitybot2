CREATE TABLE IF NOT EXISTS `events` (
    `eventId`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `identifier`       TEXT NOT NULL,
    `title`            TEXT NOT NULL,
    `startTime`        INTEGER NOT NULL,
    `endTime`          INTEGER NOT NULL,
    `currencyKey`      TEXT NOT NULL,
    `startingAmount`   REAL,
    `targetAmount`     INTEGER NOT NULL,
    `sourceUrl`        TEXT NOT NULL,
    `updateDelay`      INTEGER
);