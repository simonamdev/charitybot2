PRAGMA writable_schema = 1;
DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger');
PRAGMA writeable_schema = 0;
VACUUM;

CREATE TABLE `events` (
    `eventId`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `internalName`     TEXT NOT NULL,
    `externalName`     TEXT NOT NULL,
    `startTime`        INTEGER NOT NULL,
    `endTime`          INTEGER NOT NULL,
    `currencyId`       TEXT NOT NULL,
    `startingAmount`   REAL,
    `targetAmount`     REAL NOT NULL,
    `sourceUrl`        TEXT NOT NULL,
    `updateDelay`      INTEGER
);

CREATE TABLE `donations` (
    `donationId`     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `eventId`        INTEGER NOT NULL,
    `timeRecorded`   INTEGER NOT NULL,
    `donationAmount` REAL NOT NULL,
    `runningTotal`   REAL NOT NULL,
    `notes`          TEXT,
    `valid`          INTEGER NOT NULL CHECK (valid BETWEEN 0 AND 1),
    FOREIGN KEY(eventId) REFERENCES events(eventId)
);

CREATE TABLE `donationRegressions` (
    `donationRegressionId`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `eventId`               INTEGER NOT NULL,
    `donationId`            INTEGER NOT NULL,
    `previousTotal`         REAL NOT NULL,
    `newTotal`              REAL NOT NULL,
    `regressionAmount`      REAL NOT NULL,
    FOREIGN KEY(eventId) REFERENCES events(eventId),
    FOREIGN KEY(donationId) REFERENCES donations(donationId)
);

INSERT INTO `events` (eventId, internalName, externalName, startTime, endTime, currencyId, startingAmount, targetAmount, sourceUrl, updateDelay)
VALUES
(1, "TestOne", "Test One Title", 1477256983, 1477256985, "GBP", 0, 1000, "http://127.0.0.1:5000/justgiving", 5),
(2, "TestTwo", "Test Two Title", 1477256989, 1477256995, "USD", 10.0, 1000, "http://127.0.0.1:5000/justgiving", 5),
(3, "TestThree", "Test Three Title", 1477256999, 1477257999, "GBP", 3000.5, 5000, "http://127.0.0.1:5000/justgiving", 5),
(4, "TestFour", "Test Four Title", 1477256999, 1477257999, "GBP", 0, 5000, "http://127.0.0.1:5000/justgiving", 5),
(5, "TestFive", "Test Five Title", 0, 9999999999999, "EUR", 50, 1000, "http://127.0.0.1:5000/justgiving", 5);

INSERT INTO `donations` (donationId, eventId, timeRecorded, donationAmount, runningTotal, notes, valid)
VALUES
(1, 1, 1477256983, 10.5, 10.5, NULL, 1),
(2, 1, 1477256988, 10.5, 21.0, NULL, 1),
(3, 1, 1477256990, 5.33, 26.33, NULL, 1),
(4, 1, 1477256999, 10.5, 36.83, NULL, 1),
(5, 1, 1477256999, 63.17, 100.0, NULL, 1),
(6, 2, 1477257000, 10.0, 20.0, NULL, 1),
(7, 2, 1477257010, 10.0, 30.0, NULL, 1),
(8, 2, 1477257020, -10.0, 20.0, "Mistake", 0),
(9, 3, 1477257030, -10.0, 10.0, "Mistake 2", 0),
(10, 3, 1477257040, 100.0, 3100.0, NULL, 1),
(11, 3, 1477257050, 100.0, 3200.0, NULL, 1),
(12, 3, 1477257060, 100.0, 3300.0, NULL, 1),
(13, 4, 1477257060, 100.0, 100.0, NULL, 1),
(14, 4, 1477257061, -25.0, 75.0, "Chargeback", 0),
(15, 4, 1477257062, 75.0, 150.0, NULL, 1);

INSERT INTO `donationRegressions` (donationRegressionId, eventId, donationId, previousTotal, newTotal, regressionAmount)
VALUES
(1, 2, 8, 30.0, 20.0, 10.0),
(2, 2, 9, 20.0, 10.0, 10.0),
(3, 4, 14, 100, 75.0, 25.0);