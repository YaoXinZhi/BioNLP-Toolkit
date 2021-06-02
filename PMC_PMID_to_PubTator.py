# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 02/06/2021 10:13
@Author: XINZHI YAO
"""


"""
PubTator API to get PubTator/Biocjson Annotation
"""


import os
import bs4
import time
import string
import requests
import argparse
from bs4 import BeautifulSoup


def read_pmid_info(input_file: str):

    pmid_set = set()
    pmc_set = set()
    with open(input_file) as f:
        f.readline()
        for line in f:
            l = line.strip().split('\t')
            _id, source = l[1], l[2]
            if source == 'PMID':
                pmid_set.add(_id)
            elif source == 'PMC':
                pmc_set.add(_id)
            else:
                raise TypeError(line)
    return pmid_set, pmc_set


def get_HTMLText(url):
    headers = {'User-Agent':'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36', 'Cookie':'ncbi_sid=47EF8993E4BE3193_0587SID; _ga=GA1.2.780797648.1582031800; pmc.article.report=; books.article.report=; _gid=GA1.2.288894097.1585885708; QSI_HistorySession=https%3A%2F%2Fwww.ncbi.nlm.nih.gov%2F~1585922167314; WebEnv=1zmWDqnmAX_v2YHx4rlkrq3Yhg3ZCIGss-UrAFg-SZPikri1ywXU5zjN2MwUgcrtonBWnvUs1EJyzzVzB2wC14pFkl6eh-708Vl%4047EF8993E4BE3193_0587SID; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgCIAYBC2ArAMIDMRAHGdmQCwCcAbEbm7mbgwOxEBiDWvzoA6AIwiAtnEogANCACuAOwA2AewCGqZVAAeAF0ygATJhABzAI6KoEAJ7yQZc5tWqndcwGcomiADGiE5E5hCKqlAAvIj2qBCaAD6oAEZRYIopklCoid7qioHRJMgGmgbI6soAylDK+RB5galRAAqZALI5iQb2YNH+FQGRiU5iXli+/kFOJrjmeISkFNS0jCzsHFy8AkJ8ohLSsgomYubWtg4YbqoYU4GIGOGRMXEJyWkZWd35hQHFpXKlRqdQaTQCLXaKS6uV6/Sig2QwygoxOZiwAHcsSJlAEUsgcapJDjkIgRBZ1DBZgxzGIGHMnJxabhKPMFGQzlg6Qz2eiQGJcEQXOyXFgDOEoIyJiBxbZGbIsIyaVgiELBTSFHR5lgmDwGJRQprRSBcCITJQRMKQHRpSoNNpdIZPKEsGyQELaawQtKGFqQkxaUwOCFuLSvAomJz+dxuLIAL5xoA'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def page_parser(url):
    html = get_HTMLText(url)
    return html

def id_to_pubtator(id_list: list, id_type: str= 'pmid', batch_size:int=950):

    if not isinstance(id_list, list):
        try:
            id_list = list(id_list)
        except:
            raise TypeError(id_list)

    total_annotation = set()

    if id_type == 'pmid':
        base_url = f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids='
    elif id_type == 'pmc':
        base_url = f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmcids='
    else:
        raise TypeError(id_tpye)

    start = 0
    while True:
        end = start + batch_size
        batch_id = id_list[start: end]
        # get annotation
        identifiers = ','.join(batch_id)
        # print(identifiers)
        url = f'{base_url}{identifiers}'
        # print(url)
        html = get_HTMLText(url)
        total_annotation.update(html.split('\n'))
        print(f'{id_type} Annotation count: {len(total_annotation):,}/{len(id_list):,}.')

        start = end
        if end >= len(id_list):
            break
    if '' in total_annotation:
        total_annotation.remove('')

    return total_annotation


def get_annotation(input_path: str, save_path: str, batch_size:int=10):

    id_file_list = os.listdir(input_path)


    for _file in id_file_list:
        file_prefix = _file.split('.')[0]
        save_file = f'{save_path}/{file_prefix}.pubtator.txt'

        file_path = f'{input_path}/{_file}'
        pmid_set, pmc_set = read_pmid_info(file_path)
        print(f'Start File: {_file}, PMID: {len(pmid_set):,}, PMC: {len(pmc_set):,}.')

        pmid_annotation = id_to_pubtator(pmid_set, 'pmid', batch_size)
        print(f'{file_prefix} PMID-PubTator: {len(pmid_annotation):,}/{len(pmid_set)}.')
        pmc_annotation = id_to_pubtator(pmc_set, 'pmc', batch_size)
        print(f'{file_prefix} PMC-PubTator: {len(pmc_annotation):,}/{pmc_set}.')

        with open(save_file, 'w', encoding='utf-8') as wf:
            for ann in pmid_annotation|pmc_annotation:
                wf.write(f'{ann}\n')
        print(f'{save_file} save done,'
              f' PubTator Count: {len(pmid_annotation|pmc_annotation):,}/{len(pmid_set|pmc_set):,}')



if __name__ == '__main__':
    pmid_info_path = '../data/pmid_info'
    pubtator_save_path = '../data/pubtator_info'
    id_batch_size = 100

    if os.path.exists(pubtator_save_path):
        os.mkdir(pubtator_save_path)

    get_annotation(pmid_info_path, pubtator_save_path, id_batch_size)