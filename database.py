import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL
            )
        """
        )
        self.conn.commit()

    def change_username(self, id, new_username):
        self.cursor.execute(
            """UPDATE users SET username = ? WHERE id = ?""",
            (new_username, id),
        )
        self.conn.commit()

    def create_channel_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS channel")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS channel (
                channel_id INTEGER PRIMARY KEY
            )
        """
        )
        self.conn.commit()

    def create_user_activity_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS user_activity")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_activity (
                user_id INTEGER,
                duration INTEGER,
                date TEXT,
                joining_time TEXT,
                leaving_time TEXT,
                FOREIGN KEY(user_id) REFERENCES users(rowid)
            )
        """
        )
        self.conn.commit()

    def user_exists(self, id):
        self.cursor.execute(
            """SELECT * FROM users WHERE id = ?""",
            (id,),
        )
        return self.cursor.fetchone() is not None

    def insert_user(self, id, username):
        self.cursor.execute(
            """
            INSERT INTO users (id, username) VALUES (?, ?)
        """,
            (id, username),
        )
        self.conn.commit()

    def insert_user_activity(self, user_id, duration, date, joining_time, leaving_time):
        self.cursor.execute(
            """
            INSERT INTO user_activity (user_id, duration, date, joining_time, leaving_time) VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, duration, date, joining_time, leaving_time),
        )
        self.conn.commit()

    def insert_channel(self, channel_id):
        self.cursor.execute(
            """
            INSERT INTO channel (channel_id) VALUES (?)
        """,
            (channel_id,),
        )
        self.conn.commit()

    def delete_channel(self, channel_id):
        self.cursor.execute(
            """
            DELETE FROM channel WHERE channel_id = ?
        """,
            (channel_id,),
        )
        self.conn.commit()

    def get_channel(self):
        self.cursor.execute(
            """
            SELECT channel_id FROM channel
        """
        )
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def get_total_time(self, user_id):
        self.cursor.execute(
            """
            SELECT SUM(duration) FROM user_activity WHERE user_id = ?
        """,
            (user_id,),
        )
        return self.cursor.fetchone()[0]

    def leaderboard(self):
        self.cursor.execute(
            """
            SELECT user_id, SUM(duration) FROM user_activity
            GROUP BY user_id
            ORDER BY SUM(duration) DESC
        """
        )
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
