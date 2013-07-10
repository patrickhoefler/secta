#!/usr/bin/env python3

import codecs
from collections import defaultdict
import datetime
import errno
import json
import os
import re
from string import Template


def export_cross_tag_occurences():
    """
    Export the Stack Exchange Cross Tag occurences to a CSV file
    suitable for import into Gephi
    """
    # Get the script directory
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    # Load the tag index from the locally saved JSON file
    with codecs.open(
        os.path.join(SCRIPT_DIR, '../index/index_tags.json'),
        'r',
        encoding='utf-8'
    ) as input_file:
        tags = json.load(input_file)

    # This is where we build our CSV and JSON output
    csv_output = ''
    json_output = {}
    occurence_count = defaultdict(int)

    # Iterate through all tags
    for tag, occurences in tags.items():

        # We're only interested if the tag occurs in more than one site
        if len(occurences) > 1:

            # Add a line to the output listing all sites where the current
            # tag occurs, separated by ;
            occurence_list = []
            for occurence, count in occurences.items():
                occurence_list.append(occurence)
            csv_output += ';'.join(occurence_list) + '\n'

            for i in range(len(occurence_list)):
                for j in range(i + 1, len(occurence_list)):
                    index = ';'.join(
                        sorted([occurence_list[i], occurence_list[j]])
                    )
                    occurence_count[index] += 1

            # Build the nodes and edges for our JSON file
            nodes_set = set()
            edges = []
            max_weight = 0
            for occurence_pair, weight in occurence_count.items():
                if weight >= 5:
                    source, target = occurence_pair.split(';')
                    nodes_set.add(source)
                    nodes_set.add(target)
                    if weight > max_weight:
                        max_weight = weight
                    edges.append({
                        'source': source,
                        'target': target,
                        'weight': weight,
                    })

    nodes = []
    for node in nodes_set:
        nodes.append({'name': node})

    for edge in edges:
        edge['source'] = nodes.index({'name': edge['source']})
        edge['target'] = nodes.index({'name': edge['target']})
        edge['weight'] = float(edge['weight']) / max_weight

    json_output = {
        'nodes': nodes,
        'edges': edges,
        'created': datetime.datetime.utcnow().isoformat() + '+00:00',
    }

    # Write the CSV file
    with codecs.open(
        os.path.join(SCRIPT_DIR, '../www/shared_tags_gephi.csv'),
        'w',
        encoding='utf-8'
    ) as output_file:
        output_file.write(csv_output)

    print('Successfully exported the CSV file for Gephi.')

    # Export the JSON file for the web visualization
    with codecs.open(
        os.path.join(SCRIPT_DIR, '../www/graph.json'),
        'w',
        encoding='utf-8'
    ) as json_file:
        json.dump(json_output, json_file, ensure_ascii=False)

    print('Successfully exported the JSON file for D3.')


# If the script is called directly, execute the
# export_cross_tag_occurences() function
if __name__ == '__main__':
    export_cross_tag_occurences()
