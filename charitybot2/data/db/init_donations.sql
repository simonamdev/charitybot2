CREATE TABLE IF NOT EXISTS `donations` (
    `donationId`            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `amount`                REAL NOT NULL,
    `eventInternalName`     TEXT NOT NULL,
    `timeRecorded`          INTEGER NOT NULL,
    `internalReference`     TEXT NOT NULL,
    `externalReference`     TEXT,
    `donorName`             TEXT,
    `notes`                 TEXT,
    `valid`                 INTEGER NOT NULL CHECK (valid BETWEEN 0 AND 1),
    FOREIGN KEY(eventInternalName) REFERENCES events(internalName)
);