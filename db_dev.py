import develop
import sqlite3
import os


class YoutubeDatabase:
    def __init__(self, db_name='youtubeDb.db'):
        """Connect to existing database or create a new one"""
        self.__db_name = db_name
        self.__db_connection = sqlite3.connect(self.__db_name)
        self.cursor = self.__db_connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()

    def create_table(self, channel_id):
        # TODO: get first page data and use the channel name as table name
        result = develop.Channel(channel_id).get_channel_details()
        channel_name = result["items"][0]['snippet']['channelTitle']
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {channel_name}\
            (channelId TEXT PRIMARY KEY, title TEXT,\
                playlistId TEXT, publishedAt DATETIME, \
                videoId TEXT, thumbnailDefault TEXT,\
                thumbnailMaxres TEXT,  downloaded BOOLEAN DEFAULT 0)""")
        print(channel_name + " created")

    def print_tables(self):
        sql = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""
        self.cursor.execute(sql)
        table_list = self.cursor.fetchall()
        # SQL returns an array of size 2 for each table, we pick just one
        table_names=[]
        for item in table_list:
            table_names.append(item[0])

        print(table_names)

    def insert_all_videos(self):
        response = develop.Channel.get_all_videos()

    def insert_specific_video(self, table, channelId, title, playlistId, publishedAt, videoId, thumbnailDefult, thumbnailMaxres):
        sql = f"INSERT OR IGNORE INTO {table} VALUES(?,?,?,?,?,?,?,0)"
        self.cursor.execute(sql, ( channelId, title, playlistId, publishedAt, videoId, thumbnailDefult, thumbnailMaxres))

    def update_download_flag(self):
        pass


if __name__ == '__main__':
    with YoutubeDatabase() as yd:
        yd.create_table("UC9mFio7rXEgtRQAhoIeGAew")