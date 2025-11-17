CREATE DATABASE TowerOfHanoi;

USE TowerOfHanoi;

CREATE TABLE leaderboard (
    PlayerID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerName VARCHAR(50) NOT NULL UNIQUE,
    Score INT DEFAULT 0
);

SELECT * FROM leaderboard;

UPDATE leaderboard
SET Score = 0
WHERE PlayerName = 'bhardwaj';

TRUNCATE leaderboard;

