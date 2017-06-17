CREATE TABLE IF NOT EXISTS `events` (
    `internalName`     TEXT NOT NULL PRIMARY KEY,
    `externalName`     TEXT NOT NULL,
    `startTime`        INTEGER NOT NULL,
    `endTime`          INTEGER NOT NULL,
    `currencyKey`      TEXT NOT NULL,
    `startingAmount`   REAL,
    `currentAmount`    REAL NOT NULL,
    `targetAmount`     INTEGER NOT NULL,
    `sourceUrl`        TEXT NOT NULL,
    `updateDelay`      INTEGER
);