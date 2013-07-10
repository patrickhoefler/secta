#!/usr/bin/env python3

import codecs
import errno
import json
import os
import requests
import time


def query_tags():
    """
    Query the first 100 tags of every main Stack Exchange site
    and save them locally to separate JSON files
    """
    # Get the script directory
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    # Get all current Stack Exchange sites, no authentication used
    sites_request = requests.get(
        'https://api.stackexchange.com/2.2/sites?pagesize=1000'
    )
    sites = sites_request.json()
    del sites_request  # Let's free up some memory

    # Wait a second ...
    time.sleep(1)

    # Iterate through all received sites
    for site in sites['items']:

        # We're only interested in 'main' sites, not 'meta' sites
        if site['site_type'] == 'main_site':

            # Get the ID of the current site
            site_id = site['api_site_parameter']

            # Request the first 100 tags for the current site
            tags_request = requests.get(
                'https://api.stackexchange.com/2.2/tags' +
                '?pagesize=100&order=desc&sort=popular&site=' + site_id
            )
            request_json = tags_request.json()

            # Create the data directory
            try:
                os.makedirs(os.path.join(SCRIPT_DIR, '../data'))
            # If the directory already exists, ignore the error,
            # otherwise report it
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

            # Save them to a file
            with codecs.open(
                os.path.join(SCRIPT_DIR, '../data/', site_id + '.json'),
                'w',
                encoding='utf-8'
            ) as output_file:
                json.dump(request_json, output_file, ensure_ascii=False)

            # Some status information for the console
            print(
                'Successfully saved ' + site_id + '. ' +
                str(request_json['quota_remaining']) +
                ' API calls left for today.'
            )

            # Wait a second ...
            time.sleep(1)


# If the script is called directly, execute the query_tags() function
if __name__ == '__main__':
    query_tags()
