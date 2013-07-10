#!/usr/bin/env python3

import codecs
from collections import defaultdict
import errno
import json
import os


def tree():
    """
    http://recursive-labs.com/blog/2012/05/31/one-line-python-tree-explained/
    """
    return defaultdict(tree)


def index_tags():
    """
    Iterate through all locally saved JSON files
    and generate the Stack Exchange Cross Tag index
    """
    # Get the script directory
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    # Let's make our index a defaultdict with autovivification
    index = tree()

    # Iterate through all files in the data directory
    for file in os.listdir(os.path.join(SCRIPT_DIR, '../data')):

        # Load the JSON file containing the tags for a site
        with codecs.open(
            os.path.join(SCRIPT_DIR, '../data/' + file),
            'r',
            encoding='utf-8'
        ) as input_file:
            tags = json.load(input_file)

        # The site ID is the filename minus the (.json) at the end
        site_id = file[:-5]

        # Iterate through all tags and add them to the index
        for tag in tags['items']:
            index[tag['name']][site_id] = tag['count']  # Autovivification ftw!

    # Create the index directory
    try:
        os.makedirs(os.path.join(SCRIPT_DIR, '../index'))
    # If the directory already exists, ignore the error, otherwise report it
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # Save the tag index to a local JSON file
    with codecs.open(
        os.path.join(SCRIPT_DIR, '../index/index_tags.json'),
        'w',
        encoding='utf-8'
    ) as output_file:
        json.dump(index, output_file, ensure_ascii=False)

    # Some status information for the console
    print('Successfully created the tag index.')


# If the script is called directly, execute the index_tags() function
if __name__ == '__main__':
    index_tags()
