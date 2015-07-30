-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- connect to tournament database
\c tournament
-- drop all views if they exist in the correct order
DROP VIEW IF EXISTS playerOpponents;
DROP VIEW IF EXISTS playerStandings;
DROP VIEW IF EXISTS gamesWon;
DROP VIEW IF EXISTS gamesPlayed;
-- drop tables 
DROP TABLE match;
DROP TABLE player;
-- create player table
CREATE TABLE player (id serial primary key, name text);
-- crate table to keep track of matches
CREATE TABLE match (winner integer references player(id),
					loser integer references player(id));
-- create a view to return the number of games played for a player
CREATE VIEW gamesPlayed AS SELECT player.id, COUNT(*) as games FROM match, player WHERE player.id = match.winner OR player.id = match.loser GROUP BY player.id;
-- create a view to return the number of games won
CREATE VIEW gamesWon AS SELECT match.winner, COUNT(*) as wins FROM match GROUP BY match.winner;
-- create a view to show the player standings - player id, name, gamesWon and gamesPlayed
CREATE VIEW playerStandings as select player.id, 
									  name, 
									  CASE WHEN gamesWon.wins IS NULL THEN 0 ELSE gamesWon.wins END,
									  CASE WHEN gamesPlayed.games IS NULL THEN 0 ELSE gamesPlayed.games END
									  from player left join gamesWon on gamesWon.winner = player.id left join gamesPlayed on gamesPlayed.id = player.id
									  ORDER BY wins DESC, player.id ASC;
-- create a view to return all the players a player has already played
CREATE VIEW playerOpponents as select player.id, 
									  case when winner = player.id then loser else winner end as opponent 
									  from match, player where winner = player.id or loser = player.id order by player.id;