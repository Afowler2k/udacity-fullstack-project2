#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM match")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM player")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM player")
    result=cur.fetchone()
    number_of_players = result[0]
    db.close()
    return number_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO player (name) VALUES(%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    sql = ('SELECT * from playerStandings;')
    cur.execute(sql)
    standings = list(cur.fetchall())
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO match (winner, loser) VALUES(%s, %s);", (winner, loser,))
    db.commit()
    db.close()
 

def getOpponents(player):
    """Returns a list of players the player has played so far

    Args:
        player: the id of the player to get the opponents for
    Returns:
        A list of player ids that the player has played

    """
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT opponent from playerOpponents where id = %s;", [player])
    opponents = list(cur.fetchall())
    db.close()

    # return list of tuples as list of single items
    return [opponent[0] for opponent in opponents]

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairCount = len(standings)/2;
    pairs = list()
    # loop through the players in pairs and match them together with the next one 
    for pair in range(0, pairCount):
        standingIndex = pair * 2;
        (id1, n1, w, m) = standings[standingIndex]
        (id2, n2, w, m) = standings[standingIndex+1]
        pairs.append( [id1, n1, id2, n2] )
    return pairs

def swissPairingsNoRematch():
    """Returns a list of pairs of players for the next round of a match preventing rematches
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings who has not already played that player.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # get standings
    standings = playerStandings()
    # create empty list of who has been matched so far
    matched = list()
    # list of paired players
    pairs = list()
    # loop through all the standings
    for idx, (pId, pName, pWins, pMatches) in enumerate(standings):
        # if player not already matched
        if pId not in matched:
            # get players played against already
            playersPlayed = getOpponents(pId)
            # loop through remaining players to find someone to pair with
            # It is possible to exit this loop without matching this player to anyone
            # if they have played all the unmatched players already
            for idx2 in range(idx + 1, len(standings)):
                (p2Id, p2Name, p2Wins, p2Matches) = standings[idx2]
                # if player has not already been matched and not already played player above, 
                # pair them
                if p2Id not in matched and p2Id not in playersPlayed:
                    pairs.append( [pId, pName, p2Id, p2Name] )
                    # save ids of matched players
                    matched.append(pId)
                    matched.append(p2Id)
                    break

    return pairs;


