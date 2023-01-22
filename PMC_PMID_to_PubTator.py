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
# import bs4
# import time
# import string
import requests
import argparse
# from bs4 import BeautifulSoup


def read_pmid_info(input_file: str):

    pmid_set = set()
    pmc_set = set()
    with open(input_file) as f:
        f.readline()
        for line in f:
            l = line.strip().split('\t')
            if l[0] == 'Term':
                continue
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

def id_to_pubtator(id_list: list, save_file: str, id_type: str= 'pmid', batch_size:int=950):

    if not isinstance(id_list, list):
        try:
            id_list = list(id_list)
        except:
            raise TypeError(id_list)

    if id_type == 'pmid':
        base_url = f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids='
    elif id_type == 'pmc':
        base_url = f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmcids='
    else:
        raise TypeError(id_type)

    start = 0
    batch_count = 0
    save_count = 0
    wf = open(save_file, 'w')
    while True:
        batch_count += 1
        end = start + batch_size
        batch_id = id_list[start: end]
        # get annotation
        identifiers = ','.join(batch_id)
        url = f'{base_url}{identifiers}'

        # print(url)
        # input()
        html = get_HTMLText(url)
        batch_annotation = html.split('\n')
        # print(f'batch_annotation: {len(batch_annotation)}')

        for annotation in batch_annotation:
            if annotation:
                save_count += 1
                wf.write(f'{annotation}\n')
        # print(f'save count: {save_count:,}')
        print(f'Batch: {batch_count}, {id_type} ID Saved: {save_count:,}.')
        start = end
        if end >= len(id_list):
            break

    wf.close()
    print(f'{save_file} save done, Save Count: {save_count:,}/{len(id_list):,}')
    return save_count

def read_pmc_pmid_file(pmc_pmid_file: str):

    pmid_set = set()
    pmc_set = set()
    with open(pmc_pmid_file) as f:
        for line in f:
            l = line.strip()
            if l.startswith('PMC'):
                pmc_set.add(l)
            else:
                pmid_set.add(l)
    print(f'{len(pmid_set):,} pmid, {len(pmc_set):,} pmc.')
    return pmid_set, pmc_set


def get_annotation(pmc_pmid_file: str, save_path: str,
                   _save_type:set, batch_size:int=100,
                   prefix:str='pubtator-download'):

    pmid_set, pmc_set = read_pmc_pmid_file(pmc_pmid_file)

    print(pmid_set)
    print(pmc_set)
    if _save_type == 'pmid':
        save_type = {'pmid'}
    elif _save_type == 'pmc':
        save_type = {'pmc'}
    elif _save_type == 'both':
        save_type = {'pmc', 'pmid'}
    else:
        raise ValueError(f'save_type-{_save_type} wrong.')

    pmid_save_file = f'{save_path}/{prefix}.pubtator.pmid.txt'
    pmc_save_file = f'{save_path}/{prefix}.pubtator.pmc.txt'

    if 'pmid' in save_type:
        # if not os.path.exists(pmid_save_file):
        pmid_save_count = id_to_pubtator(pmid_set, pmid_save_file, 'pmid', batch_size)
        print(f'{prefix} PMID-PubTator: {pmid_save_count:,}/{len(pmid_set)}.')
    if 'pmc' in save_type:
        # if not os.path.exists(pmc_save_file):
            # pmcid_set = {f'PMC{_id}' for _id in pmc_set}
        pmc_save_count = id_to_pubtator(pmc_set, pmc_save_file, 'pmc', batch_size)
        print(f'{prefix} PMC-PubTator: {pmc_save_count:,}/{len(pmc_set)}.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Lit-GWAS Bayes model.')

    parser.add_argument('-ip', dest='pmc_pmid_file',
                        default='../data/APOE_dir/APOE_id_info',
                        help='default: ../data/APOE_dir/APOE_id_info')

    parser.add_argument('-sp', dest='pubtator_save_path',
                        default='../data/APOE_dir/APOE_bioc',
                        help='default: ../data/APOE_dir/APOE_bioc')

    parser.add_argument('-it', dest='id_type',
                        default='both', choices=['pmid', 'pmc', 'both'],
                        help='default: both')

    parser.add_argument('-pr', dest='prefix',
                        default='pubtator-download')

    parser.add_argument('-bs', dest='batch_size', type=int,
                        default=3,
                        help='default: 3')

    args = parser.parse_args()


    if not os.path.exists(args.pubtator_save_path):
        os.mkdir(args.pubtator_save_path)

    get_annotation(args.pmc_pmid_file, args.pubtator_save_path,
                   args.id_type, args.batch_size, args.prefix)
