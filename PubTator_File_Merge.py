# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 30/12/2020 21:07
@Author: XINZHI YAO
"""

import argparse

def PubTator_Merge(pubtator_a: str, pubtator_b: str, save_file: str):

    wf = open(save_file, 'w')

    save_flag = False
    saved_pmid_set = set()
    with open(pubtator_a) as f:
        for line in f:
            l = line.strip().split('|')
            if l == ['']:
                wf.write('\n')
            else:
                if len(l) > 2:
                    if l[1] == 't':
                        save_flag = True
                        pmid = l[0]
                        if pmid in saved_pmid_set:
                            save_flag = False
                        saved_pmid_set.add(pmid)
                        if save_flag:
                            wf.write(line)
                    elif l[1] == 'a':
                        if save_flag:
                            wf.write(line)
                else:
                    if save_flag:
                        wf.write(line)
    print(f'{len(saved_pmid_set):,} PubTator in {pubtator_a}')

    with open(pubtator_b) as f:
        for line in f:
            l = line.strip().split('|')
            if l == [ '' ]:
                wf.write('\n')
            else:
                if len(l) > 2:
                    if l[ 1 ] == 't':
                        save_flag = True
                        pmid = l[ 0 ]
                        if pmid in saved_pmid_set:
                            save_flag = False
                        saved_pmid_set.add(pmid)
                        if save_flag:
                            wf.write(line)
                    elif l[ 1 ] == 'a':
                        if save_flag:
                            wf.write(line)
                else:
                    if save_flag:
                        wf.write(line)
    wf.close()
    print(f'{save_file} save done, {len(saved_pmid_set):,} PubTator..')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PubTator file Merge.')
    parser.add_argument('-pa', dest='pubtator_a', type=str, required=True)
    parser.add_argument('-pb', dest='pubtator_b', type=str, required=True)
    parser.add_argument('-sf', dest='save_file', type=str, required=True)
    args = parser.parse_args()

    PubTator_Merge(args.pubtator_a, args.pubtator_b, args.save_file)



