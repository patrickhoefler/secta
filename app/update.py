#!/usr/bin/env python3

from query_tags import query_tags
from index_tags import index_tags
from export_cross_tag_occurences import export_cross_tag_occurences

"""
This script runs the complete workflow to query the most popular tags
from all main Stack Exchange sites to indexing them and finally creating
a CSV file with all cross-tag occurences.
"""

# Start by querying the tags for all main Stack Exchange sites
query_tags()

# Next, index the tags
index_tags()

# Finally, export the CSV file for Gephi
export_cross_tag_occurences()
