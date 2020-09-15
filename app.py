from __future__ import print_function
from flask import Flask, request, jsonify
import argparse
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

    def make_request(self, host):
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % API_KEY,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)


    def search(self, api_key, term, location, limit):

        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': limit
        }
        return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


    def get_business(self, api_key, business_id):

        business_path = BUSINESS_PATH + business_id

        return request(API_HOST, business_path, api_key)


    def query_api(self, term, location):

        response = search(API_KEY, term, location)

        businesses = response.get('businesses')

        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return

        business_id = businesses[0]['id']

        print(u'{0} businesses found, querying business info ' \
            'for the top result "{1}" ...'.format(
                len(businesses), business_id))
        response = get_business(API_KEY, business_id)

        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)

        return response

    def main(self, term, location):
        parser = argparse.ArgumentParser()

        parser.add_argument('-q', '--term', dest='term', default=term,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=location, type=str,
                            help='Search location (default: %(default)s)')

        input_values = parser.parse_args()

        try:
            results = query_api(input_values.term, input_values.location)
            return results
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )

        return 0

@app.route('/api/location', methods=['GET'])
def location_search(): 

    # Receive GET body and parse for values
    term = request.args.get('term')
    location = request.args.get('location')
    limit = request.args.get('limit')

    location = Location(term, location, limit)

    results = location.main()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)