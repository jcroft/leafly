import json
import requests
import datetime

class Leafly:

	def parse_affects_json(self, data):
		affects = []
		for i in data:
			affects.append({
				'name'	: i['Name'],
				'score'	: i['Score'],
			})
		return affects

	def parse_reviews_json(self, data):
		reviews = []

		for i in data:

			# Date conversion
			date_added_seconds = int(i['DateAdded'].strip('/Date(').strip(')/'))/1000.0

			reviews.append({
				'buzz_length'	: i['BuzzLength'],	# This seems deprecated
				'notes'			: i['Notes'],
				'date_added'	: datetime.datetime.utcfromtimestamp(date_added_seconds),
				'rating'	    : int(i['Rating']),
			})
		return reviews

	def parse_strain_json(self, data, include_reviews=False):

		strain = {}

		# Some of these are only in the list API method, and some are only
		# in the detail API method. Check for both, add whatever you can.

		if data.has_key('Id'): 
			strain['id'] = data['Id']

		if data.has_key('Key'): 
			strain['key'] = data['Key']

		if data.has_key('Symbol'): 
			strain['symbol'] = data['Symbol']

		if data.has_key('Name'): 
			strain['name'] = data['Name']

		if data.has_key('Abstract'): 
			strain['abstract'] = data['Abstract']

		if data.has_key('Overview'): 
			strain['overview'] = data['Overview']

		if data.has_key('Category'): 
			strain['category'] = data['Category']

		if data.has_key('Url'): 
			strain['url'] = data['Url']

		if data.has_key('RateUrl'): 
			strain['rate_url'] = data['RateUrl']

		if data.has_key('DetailUrl'): 
			strain['detail_url'] = data['DetailUrl']

		if data.has_key('Rating'): 
			strain['rating'] = float(data['Rating'])

		if data.has_key('Negative'): 
			strain['negative'] = self.parse_affects_json(data['Negative'])
		
		if data.has_key('Effects'): 
			strain['effects'] = self.parse_affects_json(data['Effects'])
		
		if data.has_key('Medical'): 
			strain['medical'] = self.parse_affects_json(data['Medical'])
		
		if data.has_key('Reviews') and include_reviews: 
			strain['reviews'] = self.parse_reviews_json(data['Reviews'])
		

		# These seem deprecated
		if data.has_key('TopEffect'):
			if not data['TopEffect'] == 'n/a':
				strain['top_effect'] = data['TopEffect']
		
		if data.has_key('TopMedical'):
			if not data['TopMedical'] == 'n/a':
				strain['top_medical'] = data['TopMedical']

		if data.has_key('TopActivity'):
			if not data['TopActivity'] == 'n/a':
				strain['top_activity'] = data['TopActivity']

		return strain

	def get_strain_list(self, category=None):
		params = {}
		url = 'http://www.leafly.com/api/strains'
		if category:
			params['category'] = category
		r = requests.get(url, params=params)
		data = r.json()
		strains = []
		for i in data:
			strains.append(self.parse_strain_json(i))
		return strains

	def get_strain_details(self, strain_key, include_reviews=False):
		params = {}
		url = 'http://www.leafly.com/api/details/%s' % strain_key
		r = requests.get(url, params=params)
		data = r.json()
		strain = self.parse_strain_json(data, include_reviews=include_reviews)
		return strain




