import json
from collections import defaultdict
#from flask import Flask, request
from pytrie import Trie
import uuid
import requests

#app = Flask(__name__)

university_data = list()
university_country_index = defaultdict(list)
university_domain_index = defaultdict(list)
university_name_index = dict()


def search(domain='',country='',name=''):
    if not uni_data_loaded:
        load_data()

    #country = request.args.get('country')
    #name = request.args.get('name')
    #domain = request.args.get('domain')
    filtered = university_data

    if name and country:
        name = name.lower()
        country = country.lower()
        name_filtered = prefix_tree.values(prefix=name)
        country_filtered = university_country_index[country]
        filtered = [i for i in name_filtered if i['name'] in [_i['name'] for _i in country_filtered]]

    elif domain:
        domain = domain.lower()
        filtered = university_domain_index[domain]

    elif name:
        name = name.lower()
        filtered = prefix_tree.values(prefix=name)
    elif country:
        country = country.lower()
        filtered = university_country_index[country]

    return len(filtered)

uni_data_loaded = False


def load_data():
    [print('Loading uni data') for i in range(10)]
    global uni_data_loaded, prefix_tree, university_data, university_country_index, university_name_index, university_domain_index
    response = requests.get("https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json")
    university_data = response.json()
    for i in university_data:
        #university_country_index[i["country"].lower()].append(i)
        [university_domain_index[j.lower()].append(i) for j in i["domains"]]
        #university_name_index[i['name'].lower()] = i
        '''
        splitted = i['name'].split(" ")
        if len(splitted) > 1:
            for splitted_name in splitted[1:]:
                university_name_index[splitted_name.lower() + str(uuid.uuid1())] = i
        '''
    #prefix_tree = Trie(**university_name_index)

    uni_data_loaded = True

'''
@app.route('/')
def index():

    if not data_loaded:
        load_data()

    data = {'author': {'name': 'hipo', 'website': 'http://hipolabs.com'},
            'example': 'http://universities.hipolabs.com/search?name=middle&country=Turkey',
            'github': 'https://github.com/Hipo/university-domains-list'}
    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=False)
'''