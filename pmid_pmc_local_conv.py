# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 22/01/2023 13:32
@Author: yao
"""

"""
该代码利用从 https://ftp.ncbi.nlm.nih.gov/pub/pmc/ 下载
PMC-ids.csv 2021-01-23 文件
进行PMID-PMCid的转换。

该文件包含
Journal Title,ISSN,eISSN,Year,Volume,Issue,Page,DOI,
PMCID,PMID,Manuscript Id,Release Date
"""

import os
import gzip
import argparse

def read_mapping(mapping_file):

    pmid_to_pmc = {}
    with gzip.open(mapping_file) as f:
        f.readline()
        for line in f:
            l = line.decode('utf-8').strip().split(',')

            pmid = l[9]
            pmcid = l[8]

            pmid_to_pmc[pmid] = pmcid
    print(f'{len(pmid_to_pmc):,} pmid-pmc mapping.')
    return pmid_to_pmc

def main(id_file, save_path, mapping_file):

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    prefix = os.path.basename(id_file).split('.')[0]

    pmcid_save_file = f'{save_path}/{prefix}.pmc.txt'
    pmid_save_file = f'{save_path}/{prefix}.pmid.txt'

    pmid_to_pmc = read_mapping(mapping_file)

    pmc_num = 0
    pmid_num = 0
    with open(id_file) as f, open(pmcid_save_file, 'w') as wf_pmc,\
        open(pmid_save_file, 'w') as wf_pmid:
        for line in f:
            pmid = line.strip()

            if pmid_to_pmc.get(pmid):
                wf_pmc.write(f'{pmid_to_pmc[pmid]}\n')
                pmc_num += 1
            elif pmid.startswith('PMC'):
                wf_pmc.write(f'{pmid}\n')
                pmc_num += 1
            else:
                wf_pmid.write(f'{pmid}\n')
                pmid_num += 1

    total_id_num = pmc_num + pmid_num
    print(f'{pmc_num:,}/{total_id_num:,} pmcid, '
          f'{pmid_num:,}/{total_id_num:,} pmid saved.')
    print(f'Save path: {os.path.abspath(save_path)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # /home/kyzhou/xzyao/PubTator-2022-12-17-version/tmVar3.PubMed_PMC.result.txt
    parser.add_argument('-if', dest='id_file', required=True,
                        help='one clo id file, include PMID/PMC id.')
    parser.add_argument('-sp', dest='save_path', required=True)

    parser.add_argument('-mf', dest='mapping_file',
                        default='/home/kyzhou/xzyao/PubTator-2022-12-17-version/PMC-ids.csv.gz',
                        help='default: /home/kyzhou/xzyao/PubTator-2022-12-17-version/PMC-ids.csv.gz')
    args = parser.parse_args()

    main(args.id_file, args.save_path, args.mapping_file)


