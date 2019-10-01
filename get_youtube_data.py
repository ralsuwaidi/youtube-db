# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors
import yaml
import dateutil.parser

import yt_database

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# use config file to populate api details
config = yaml.safe_load(open('config_default.yaml'))

api_service_name = config['api_service_name']
api_version = config['api_version']
api_key = config['api_key']

# Get credentials and create an API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)


# name database
# start database and/or connect to it
database_name = 'ytDatabase.db'
try:
    yt_database.create_connection()
except:
    print("cannot create or connect to database")

# get names from text file
def scrape_names():

    with open('channel_list.txt', 'r') as channel:
        channel_list = channel.read().splitlines()
    
    return channel_list

# return channel id from array list of names
def get_channel_id():

    channel_array =[]
    channel_list = scrape_names()
    for channel in channel_list:
        try: 
            request = youtube.channels().list(
            part="contentDetails",
            forUsername=channel,
            )
            response = request.execute()

            channel = response["items"][0]['contentDetails']["relatedPlaylists"]['uploads']
        except:
            request = youtube.channels().list(
            part="contentDetails",
            id=channel,
            )
            response = request.execute()

            channel = response["items"][0]['contentDetails']["relatedPlaylists"]['uploads']
        channel_array.append(channel)
    
    return channel_array


# get page from channel and pageid 
def get_next_page_data(channel: str, nextPageToken: str):

    request = youtube.playlistItems().list(
            part="snippet",
            playlistId=str(channel),
            maxResults=50,
            pageToken=nextPageToken,
    )
    response = request.execute()
    return response

# converts channel name into channel id
def get_channel_video(channel_id: str):
            
    request = youtube.playlistItems().list(
    part="snippet",
    playlistId=str(channel_id),
    maxResults=50,
    )
    response = request.execute()
    return response

# get all videos in channel
def main():

    # list of names 
    channel_name_list = scrape_names()
    count = 0   #track channel
    added = 0   #track number of rows

    # iterate through each channel
    channel_array = get_channel_id()
    for channel_id in channel_array:

        # create table and use channel name as table name
        yt_database.create_table(channel_name_list[count])
        
        # print first 50 pages
        response = get_channel_video(channel_id)
        print("adding {}".format(response["items"][count]["snippet"]['channelTitle']))
        for item in response["items"]:
            # try to get max resolution image, if not then get default
            try: 
                yt_database.new_table_entry(channel_name_list[count],
                item['snippet']['resourceId']['videoId'],
                item["snippet"]["title"],
                dateutil.parser.parse(item["snippet"]["publishedAt"]),
                item["snippet"]["thumbnails"]["maxres"]["url"])
                added+=1
            except:
                yt_database.new_table_entry(channel_name_list[count],
                item['snippet']['resourceId']['videoId'],
                item["snippet"]["title"],
                dateutil.parser.parse(item["snippet"]["publishedAt"]),
                item["snippet"]["thumbnails"]["default"]["url"])
                added+=1

        
        # get rest of videos and check if more are available
        while 1:
            response = get_next_page_data(channel_id, response["nextPageToken"])
            for item in response["items"]:
                try: 
                    yt_database.new_table_entry(channel_name_list[count],
                    item['snippet']['resourceId']['videoId'],
                    item["snippet"]["title"],
                    dateutil.parser.parse(item["snippet"]["publishedAt"]),
                    item["snippet"]["thumbnails"]["maxres"]["url"])
                    added+=1
                except:
                    yt_database.new_table_entry(channel_name_list[count],
                    item['snippet']['resourceId']['videoId'],
                    item["snippet"]["title"],
                    dateutil.parser.parse(item["snippet"]["publishedAt"]),
                    item["snippet"]["thumbnails"]["default"]["url"])
                    added+=1

                
            # check if next page is available, break if there is no more
            try:
                response["nextPageToken"]
            except:
                print(f"Added {added} videos")
                count+=1
                added=0
                break


if __name__ == "__main__":
    main()
