-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- connect to tournament database
\c tournament
-- drop the database (all tables and views) if it exists
DROP DATABASE IF EXISTS tournament;

-- create player table
CREATE TABLE player (id serial primary key, name text);

-- crate table to keep track of matches
CREATE TABLE match (winner integer references player(id),
					loser integer references player(id));

-- create a view to return the number of games played for a player
CREATE VIEW gamesPlayed AS 
SELECT player.id, 
	   COUNT(*) as games 
FROM match, player 
WHERE player.id = match.winner 
   OR player.id = match.loser 
GROUP BY player.id;

-- create a view to return the number of games won
CREATE VIEW gamesWon AS 
SELECT winner, 
	   COUNT(*) as wins 
FROM match 
GROUP BY match.winner;

-- create a view to show the player standings - player id, name, gamesWon and gamesPlayed
CREATE VIEW playerStandings as 
SELECT player.id, 
	   name, 
	   CASE WHEN gamesWon.wins IS NULL 
	   		THEN 0 
	   		ELSE gamesWon.wins 
	   END,
       CASE WHEN gamesPlayed.games IS NULL 
       		THEN 0 
       		ELSE gamesPlayed.games 
       END
FROM player 
LEFT JOIN gamesWon ON gamesWon.winner = player.id 
LEFT JOIN gamesPlayed ON gamesPlayed.id = player.id
ORDER BY wins DESC, 
		 player.id ASC;

-- create a view to return all the players a player has already played
CREATE VIEW playerOpponents as 
SELECT player.id, 
	   CASE WHEN winner = player.id 
	   		THEN loser 
	   		ELSE winner 
	   END AS opponent 
FROM match, player 
WHERE winner = player.id 
   OR loser = player.id 
ORDER BY player.id;
