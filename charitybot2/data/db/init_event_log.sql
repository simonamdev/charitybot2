CREATE TABLE IF NOT EXISTS `eventLog` (
    `internalName`     TEXT NOT NULL PRIMARY KEY,
    `timeUpdated`      INTEGER NOT NULL,
    FOREIGN KEY(internalName) REFERENCES events(internalName)
);