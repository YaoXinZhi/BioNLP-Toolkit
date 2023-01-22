# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 21/01/2023 12:39
@Author: yao
"""
import time

"""
该代码利用idconv工具转换pmid为pmcid
看看会不会快一点
"""

import os
import requests
import argparse

def read_pmid_file(pmid_file: str):
    pmid_set = set()
    with open(pmid_file) as f:
        for line in f:
            l = line.strip()
            pmid_set.add(l)
    return pmid_set


def main(pmid_file: str, save_file: str,
         multi_process: bool=False, process_num: int=3):

    pmid_set = read_pmid_file(pmid_file)

    """
    http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=23840460&format=json&idtype=pmcid
    {
 "status": "ok",
 "responseDate": "2023-01-20 23:39:45",
 "request": "ids=23840460;format=json;idtype=pmcid",
 "warning": "no e-mail provided; no tool provided",
 "records": [
   {
    "pmcid": "PMC23840460",
    "live": "false",
    "status": "error",
    "errmsg": "invalid article id"
   }
 ]
}
    
    """
    start_time = time.time()
    process_count = 0
    success_count = 0
    err_count = 0
    with open(save_file, 'w') as wf:
        for pmid in pmid_set:
            process_count += 1
            if process_count % 1000 == 0:
                end_time = time.time()
                print(f'{process_count:,}/{len(pmid_set):,} pmid processed.')
                print(f'{success_count:,} success, {err_count:,} error.')
                print(f'time cost: {end_time-start_time:.2f}')
            try:
                url = f"http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json&idtype=pmcid"
                response = requests.get(url)
                json_data = eval(response.text)
                pmcid = json_data['records'][0]['pmcid']
                # print(pmid)
                # print(pmcid)
                wf.write(f'{pmid}\t{pmcid}\n')
                success_count += 1
            except:
                err_count += 1
                continue

    end_time = time.time()
    print(f'{process_count:,}/{len(pmid_set):,} pmid processed.')
    print(f'{success_count:,} success, {err_count:,} error.')
    print(f'time cost: {end_time - start_time:.2f}')
    print(f'{save_file} saved.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # home/kyzhou/xzyao/PubTator-2022-12-17-version/tmVar3.pmid-pmc.txt
    parser.add_argument('-pf', dest='pmid_file', required=True)

    # /home/kyzhou/xzyao/PubTator-2022-12-17-version/tmVar3.pmcid.txt
    parser.add_argument('-sf', dest='save_file', required=True)

    # parser.add_argument('-mp', dest='multi_process', default=False,
    #                     action='store_ture')
    # parser.add_argument('-pn', dest='process_num', default=3,
    #                     type=int)
    args = parser.parse_args()

    # main(args.pmid_file, args.save_file, args.multi_process, args.process_num)
    main(args.pmid_file, args.save_file)





