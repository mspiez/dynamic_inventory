#!/usr/bin/env python
import argparse
import json
import sys

from st2client.client import Client
from st2client.models import KeyValuePair

from elasticsearch import helpers
from elasticsearch import Elasticsearch



API_KEY = 'NTQyNGI3YWI5MjAwMDc3OGIwZDI2OGFkZThlMTA5NzgwZTAyYTZiY2Y5N2RjMGUxNTI2ZmE1MDU3ZTNjNmQxOQ'
client = Client(api_key=API_KEY, api_url='http://localhost:9101/v1/')
batch_id = int(client.keys.get_by_name(name='batch_id').value)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def output_list_inventory(json_output):
    print json.dumps(json_output) 

def find_host(search_host, inventory):
    host_attribs = inventory.get(search_host, {})
    print json.dumps(host_attribs, indent=4) 


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Ansible dynamic inventory")
    parser.add_argument("--list", help="Ansible inventory of all of the groups",
        action="store_true", dest="list_inventory")
    parser.add_argument("--host",
        help="Ansible inventory of a particular host", action="store",
        dest="ansible_host", type=str)
    args = parser.parse_args()
    list_inventory = args.list_inventory
    ansible_host = args.ansible_host

    # print "list_inventory: {}".format(list_inventory)
    # print "ansible_host: {}".format(ansible_host)

    if list_inventory:
        ANSIBLE_INV = {
            'inventory_test': {
                'hosts': [ host['_source']['hostname'] for host in nodes_from_batch(batch_id)]}}
        output_list_inventory(ANSIBLE_INV)

    if ansible_host:
        find_host(ansible_host, HOST_VARS)

def nodes_from_batch(batch_id):
    batch_search = es.search(index='lab_nodes', body={'query': {'match': {'batch': '{}'.format(batch_id)}}})
    try:
        results = batch_search['hits']['hits']
    except Exception:
        print 'No Match'
    else:
        return results

def get_host_vars(results):
    HOST_VARS = {host['_source']['hostname']: host['_source'] for host in results}
    return HOST_VARS

# ANSIBLE_INV = {
#     'inventory_test': {
#                         'hosts': [ host['_source']['hostname'] for host in nodes_from_batch(1) ]
#                         }
# }

HOST_VARS = get_host_vars(nodes_from_batch(1))


if __name__ == "__main__":
    main()
