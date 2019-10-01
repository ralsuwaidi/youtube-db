import json
import os
import sqlite3
import copy

import dateutil.parser
import googleapiclient.discovery
import googleapiclient.errors
import yaml


class Channel:
	"""Youtube channel class with functions to get basic data"""
	def __init__(self, channel_id):
		self.channel_id = channel_id
		self.get_api()
		for key in self.get_channel_details():
			setattr(self, key, self.get_channel_details()[key])

	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		return self

	def get_attributes(self):
		"""print all attributes in the class instance"""
		attrs = vars(self)
		print(''.join("%s: %s\n" % item for item in attrs.items()))

	def get_api(self):
		"""get api from config file when class is instanced"""
		config = yaml.safe_load(open('config_default.yaml'))
		if not config:
			raise ValueError('No config file found!')
		api_service_name = config['api_service_name']
		api_version = config['api_version']
		api_key = config['api_key']
		self.youtube = googleapiclient.discovery.build(
    		api_service_name, api_version, developerKey=api_key)

	def get_id_response(self):
		"""returns basic channel information"""
		try: 
			request = self.youtube.channels().list(
            part="contentDetails",
            id=self.channel_id,)
			response = request.execute()
			response['items'][0]['id']
		except:
			request = self.youtube.channels().list(
            part="contentDetails",
            forUsername=self.channel_id,)
			response = request.execute()
			self.channel_name = self.channel_id
		return response

	def get_upload_id(self):
		"""returns upload id"""
		return self.get_id_response()['items'][0]\
			["contentDetails"]["relatedPlaylists"]["uploads"]

	def print_first_page(self):
		print(json.dumps(self.get_channel_details(), indent=4, sort_keys=True))

	def get_channel_details(self, pageToken='', maxResults=1):
		request = self.youtube.playlistItems().list(
        part="snippet",
		playlistId= self.get_upload_id(),
		pageToken=pageToken,
		maxResults=maxResults)
		response = request.execute()
		return response

	def get_video_no(self):
		"""prints the number of videos in the channel"""
		return self.pageInfo['totalResults']

	def get_all_videos(self):
		"""get the api response of all the videos """
		results = self.get_channel_details(maxResults=50)
		pageToken = results['nextPageToken']
		if results['nextPageToken']:
			while pageToken: 
				more_results = self.get_channel_details(
					pageToken = pageToken ,
					maxResults = 50
				)
				for item in more_results['items']:
					results['items'].append(item)
				try: 
					# try to get next page token, break if no more
					pageToken = more_results['nextPageToken']
				except:
					break
			return results
	
	def print_all_videos(self):
		""" print certain results from all the videos """
		for item in self.get_all_videos()["items"]:
			print(item['snippet']['title'])

	# FIXME: make this work
	def get_clean_results(self, response):
		detail_list = []

		for item in response['items']:
			print("got here")
			detail_dict = {}
			detail_dict['channelTitle'] = item['snippet']['channelTitle']
			detail_dict['channelId'] = item['snippet']['channelId']
			detail_dict['title'] = item['snippet']['title']
			detail_dict['playlistId'] = item['snippet']['playlistId']
			detail_dict['publishedAt'] = item['snippet']['publishedAt']
			detail_dict['videoId'] = item['snippet']['resourceId']['videoId']
			detail_dict['thumbnailDefault'] = item['snippet']['thumbnails']['default']['url']
			detail_dict['thumbnailMaxres'] = item['snippet']['thumbnails']['maxres']['url']
			detail_list.append(detail_dict)
	
		print(detail_list)
				



if __name__ == "__main__":
	with Channel("UC9mFio7rXEgtRQAhoIeGAew") as channel:
		channel.get_clean_results(channel.get_channel_details(maxResults=5))