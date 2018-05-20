CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL
);

CREATE TABLE Matches(
    id1 INTEGER UNIQUE,
    id2 INTEGER UNIQUE
);

CREATE VIEW MatchedUsers AS 
    SELECT id1 FROM Matches
    UNION 
    SELECT id2 FROM Matches; 


CREATE VIEW UnmatchedUsers AS 
    SELECT id FROM Users
    WHERE id NOT IN MatchedUsers;

