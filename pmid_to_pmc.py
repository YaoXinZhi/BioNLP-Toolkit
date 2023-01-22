# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 13/01/2023 14:10
@Author: yao, chatGPT
"""
import re

"""
该代码用于输入pmid文件，批量转换为pmc
转换成功的保存为pmcid，转换失败的保留pmid
"""

import os
import argparse
import requests
# from xml.etree import ElementTree

def read_pmid(pmid_file: str):
    pmid_list = list()
    with open(pmid_file) as f:
        for line in f:
            pmid = line.strip()
            pmid_list.append(pmid)
    print(f'{len(pmid_list):,} pmids.')
    return pmid_list

def read_existed_result(id_file: str):

    id_set = set()
    with open(id_file) as f:
        for line in f:
            id_set.add(line.strip())
    return id_set


def main(pmid_file: str, save_path: str):

    # pmids = ["11305955", "11857003", "11927016",
    #          '10190503', '10210642']

    pmid_list = read_pmid(pmid_file)

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    pmc_id_save_file = f'{save_path}/pmc.txt'
    pmid_save_file = f'{save_path}/pmid.txt'

    # todo: break process
    exist_pmc_set = set()
    exist_pmid_set = set()
    if os.path.exists(pmc_id_save_file):
        exist_pmc_set = read_existed_result(pmc_id_save_file)
        print(f'PMC save file existed, {len(exist_pmc_set):,} pmc id processed.')
    if os.path.exists(pmid_save_file):
        exist_pmid_set = read_existed_result(pmid_save_file)
        print(f'PMID save file existed, {len(exist_pmid_set):,} pmc id processed.')

    original_pmid_count = len(pmid_list)
    pmid_list = pmid_list[len(exist_pmid_set)+len(exist_pmc_set):]
    print(f'{original_pmid_count:,} total pmid, {len(pmid_list):,} wait to process.')
    # input()

    processed_count = 0
    pmc_count = 0
    with open(pmc_id_save_file, 'w') as wf_pmc, open(pmid_save_file, 'w') as wf_pmid:
        for pmc in exist_pmc_set:
            wf_pmc.write(f'{pmc}\n')
        for pmid in exist_pmid_set:
            wf_pmid.write(f'{pmid}\n')
        for pmid in pmid_list:
            processed_count += 1
            if processed_count % 1000 == 0:
                print(f'{processed_count:,} pmids processed.')
            # already pmcid
            if re.findall('PMC\d+', pmid):
                pmc_count += 1
                wf_pmc.write(f'{pmid}\n')
                continue

            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=xml"
            response = requests.get(url)
            xml_data = response.text
            # root = ElementTree.fromstring(xml_data)

            try:
                pmcid = re.findall(r'<Item Name="pmc" Type="String">(PMC\d+)</Item>', xml_data)[0]
                wf_pmc.write(f'{pmcid}\n')
                pmc_count += 1
            except:
                wf_pmid.write(f'{pmid}\n')

    print(f'{pmc_count:,}/{len(pmid_list):,} pmc id, {len(pmid_list)-pmc_count:,}/{len(pmid_list):,} pmid.')
    print(f'{pmc_id_save_file} and {pmid_save_file} saved.')
    return ''


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-pf', dest='pmid_file', required=True)
    parser.add_argument('-sp', dest='save_path', required=True)

    parser.add_argument('-ln', dest='retry_num', default=1, type=int,
                        help='retry num, default=1')
    args = parser.parse_args()


    for i in range(args.retry_num):
        print(f'Retry: {i+1}')
        try:
            main(args.pmid_file, args.save_path)
        except:
            continue



