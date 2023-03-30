"""
database.py
-----------

This module contains the classes for managing the Hug database
"""
from pathlib import Path
import sqlite3


class HugDatabase:
    """
    This class manages the data associated with the discord bot.
    """

    def __init__(self):
        # folder where "database" is stored
        # self._folder = Path('.') / 'db'
        self._folder = Path(__file__).parent / 'db'
        self._path = self._folder / 'hugging.db'

        if not self._folder.exists():
            self._folder.mkdir()
        if not self._path.exists():
            self._path.touch()

        self._connection = sqlite3.Connection(self._path)

        self._setup()

        self._connection.commit()

    def __str__(self):
        cur = self._connection.cursor()

        res = cur.execute("SELECT * FROM hugs")

        return str(res.fetchall())

    def _setup(self):
        cur = self._connection.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE name='hugs';")

        if res.fetchone() is None:
            cur.execute("""
                CREATE TABLE hugs(authorid, guildid, timestamp, huggivento);
                """
                        )

        """
        Guilds metadata:
        ----------------

        | GuildID | GuildName |
        -----------------------
        | #       | str       |

        Users metadata:
        ---------------

        | AuthorId | GuildID | Timestamp | HugGivenTo |
        ---------------------------------------------
        | str    | GuildID | UTC-time  | UserID     |
        """

    def _ETL(self):
        raise NotImplementedError("ETL not yet implemented")

    def addHug(self, authorid, guildid, timestamp, huggive=None):
        """Add hug to database"""
        inputs = [authorid, guildid, timestamp, huggive]
        cur = self._connection.cursor()

        cur.executemany("""
            INSERT INTO hugs VALUES
                (?, ?, ?, ?);
            """,
                        (inputs,)
                        )

        self._connection.commit()

    def getUserHugs(self, userid, guildid):
        """Get count of hugs that a user has had over complete time"""
        inputs = [guildid, userid]
        cur = self._connection.cursor()

        query = """
            SELECT COUNT(huggivento) FROM hugs
            WHERE guildid LIKE ?
            AND huggivento LIKE ?
            GROUP BY huggivento;
            """

        cur.execute(query, inputs)

        return cur.fetchall()

    def getUserHugLinks(self, authorid, userid, guildid):
        """Get the count of hugs from author to user"""
        inputs = [guildid, authorid, userid]
        cur = self._connection.cursor()

        query = """
            SELECT COUNT(huggivento) FROM hugs
            WHERE guildid LIKE ?
            AND authorid LIKE ?
            AND huggivento LIKE ?
            GROUP BY authorid;
            """

        cur.execute(query, inputs)

        return cur.fetchall()

    def getGuildHugs(self, guildid):
        """Get count of hugs that a user has had over complete time"""
        inputs = [guildid]
        cur = self._connection.cursor()

        query = """
            SELECT huggivento, COUNT(huggivento) AS hug_count FROM hugs
            WHERE guildid LIKE ?
            GROUP BY huggivento
            ORDER BY hug_count DESC;
            """

        cur.execute(query, inputs)

        return cur.fetchall()


class HugETL:
    pass
