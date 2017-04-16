CREATE TABLE `donations` (
    `donationId`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `eventInternalName` TEXT NOT NULL,
    `timeRecorded`      INTEGER NOT NULL,
    `donationAmount`    REAL NOT NULL,
    `runningTotal`      REAL NOT NULL,
    `notes`             TEXT,
    `valid`             INTEGER NOT NULL CHECK (valid BETWEEN 0 AND 1),
    FOREIGN KEY(eventInternalName) REFERENCES events(internalName)
);