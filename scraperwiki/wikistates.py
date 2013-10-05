#!/usr/bin/env python

from pyquery import PyQuery as pq
import requests
import scraperwiki

def get(straw, haystack):
    return haystack[straw] if straw in haystack else None

wikipedia = 'http://en.wikipedia.org'
states_url = '%s/wiki/List_of_sovereign_states' % wikipedia
expression = 'table > tr > td > b > a'

html_content = requests.get(states_url).content
document = pq(html_content)

state_data = []
for link_element in document(expression):
    attrs = link_element.attrib
    href = get('href', attrs),
    country = {
        'title': get('title', attrs),
        'href': href,
        'absolute_url': '%s/%s' % (wikipedia, href),
    }
    state_data.append(link_element.attrib)

scraperwiki.sql.save(['title', 'href', 'absolute_url'], state_data, table_name='sovereign_states')
