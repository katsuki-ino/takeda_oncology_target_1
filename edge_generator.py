import pandas as pd 
import numpy as np
import pickle
import csv
import json

import dash_table

# # phase_df = pd.read_json('phase_data.json')
# with open('data/noVCP/gene_drug_report.pkl', 'rb') as f:
#     phase_df = pickle.load(f)

# # phase_df = phase_df.set_index('Gene')
# with open('data/noVCP/drug_properties.pkl', 'rb') as f:
#     drug_properties = pickle.load(f)


class DataVersion_Manager:
    def __init__(self):
        self.path_data = pd.read_pickle('data/v1/path.pkl')
        with open('data/miyakawa_data.json', 'r') as f:
            j = json.load(f)
        self.gene_list = j['data']

    def update_graph(self, ver):
        self.path_data = pd.read_pickle('data/'+ver+'/path.pkl')


    def paging(self):
        path = self.path_data
        
        # edge処理
        path = path[path['sources']!='S']
        path = path[path['targets']!='E']
        s = list(path['sources'].unique())
        t = list(path['targets'].unique())
        starts = [n for n in s if n not in t]
        ends = [n for n in t if n not in s]

        edges = []
        for source, target, flow in zip(path['sources'], path['targets'], path['flow']):
            score = flow
            if flow > 0.1:
                flow = 0.1
            if source=='S' or target=='E':
                continue
            else:
                edges.append({'data':{'source': source, 'target': target, 'weight':flow, 'score':score}, 'selectable': 'True'})

        # node処理
        nodes = []
        for edge in edges:
            data = edge['data']
            nodes.append(data['source'])
            nodes.append(data['target'])
        
        nodes = list(set(nodes))
        page_nodes = []

        for name in nodes:
            node = {}
            node['data'] = {'id': name, 'label': name}
            if name in starts:
                node['classes'] = 'causality'
            elif name in ends:
                node['classes'] = 'responsive'

            if name in self.gene_list:
                if 'classes' not in node.keys():
                    node['classes'] = 'havedrug'
                else:
                    node['classes'] = node['classes']+' havedrug'
            
            page_nodes.append(node)
                
        return page_nodes, edges
