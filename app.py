from __future__ import print_function
from flask import Flask, request, jsonify
import json
import pprint
import requests
import sys
import urllib
import os
import json
import psycopg2

app = Flask(__name__)

class Location:

    API_KEY = '4_ZmI4BtucMbMADbxYTWt43Pnq-XXGun-pnBSSHL4oh7EKWj4KlIdDFKy-BCOMmVjfH1BIrzAKuPeVtDGRn7M-IvwgPCfWi_A65opw9wsyWxPUt4lfEIoEcoPfJfX3Yx' 
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

    def __init__(self, term, location, limit):

        self.term = term
        self.location = location
        self.limit = limit

    def make_request(self, term, location, limit):

        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': limit
        }

        url = self.API_HOST + self.SEARCH_PATH
        headers = {
            'Authorization': 'Bearer %s' % self.API_KEY,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()

    def get_business(self, biz_id):

        url = self.API_HOST + self.BUSINESS_PATH + '/' + biz_id
        headers = {
            'Authorization': 'Bearer %s' % self.API_KEY,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers)
        return response.json()

    def main(self, term, location, limit):

        try:
            results = self.make_request(term, location, limit)
            return results
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )

@app.route('/api/location', methods=['GET'])
def location_search(): 

    # Receive GET body and parse for values
    term = request.args.get('term')
    location = request.args.get('location')
    limit = request.args.get('limit')

    searchLocation = Location(term, location, limit)

    results = searchLocation.main(term, location, limit)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)