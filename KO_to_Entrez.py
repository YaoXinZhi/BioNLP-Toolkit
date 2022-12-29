# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 18/11/2021 22:24
@Author: XINZHI YAO
"""


import os
import shutil
import time

from tqdm import tqdm

from collections import defaultdict

import argparse

# map file download page: https://www.kegg.jp/pathway/ko05010

def read_ko_file(ko_file: str):
    # entire KO term related to a KEGG map
    # wget -c http://rest.kegg.jp/link/ko/map05010

    ko_set = set()
    with open(ko_file) as f:
        f.readline()
        for line in f:
            l = line.strip().split('\t')
            ko = l[1][3:]

            ko_set.add(ko)
    print(f'KO count: {len(ko_set)}')
    return ko_set

def run_conv(ko_set: set, ko_save_path: str):

    if os.path.exists(ko_save_path):
        shutil.rmtree(ko_save_path)

    os.mkdir(ko_save_path)

    for term in ko_set:
        commend_line = f'wget -c http://rest.kegg.jp/link/genes/{term} -P {ko_save_path}'

        os.system(commend_line)
        # time.sleep(3)


    print(f'Save_count/Term_count: {len(os.listdir(ko_save_path))}/{len(ko_set)}')


def save_ko_map_file(ko_save_path: str, save_file: str):

    print('reading conv result.')
    file_list = os.listdir(ko_save_path)
    ko_to_entrez = defaultdict(set)
    for _file in tqdm(file_list):
        with open(f'{ko_save_path}/{_file}') as f:
            for line in f:
                l = line.strip().split('\t')

                ko = l[0][3:]

                if l[1].startswith('hsa:'):
                    entrez = l[1][4:]
                    ko_to_entrez[ko].add(entrez)

    with open(save_file, 'w') as wf:
        for ko, entrez_set in ko_to_entrez.items():
            entrez_wf = ';'.join(entrez_set)
            wf.write(f'{ko}\t{entrez_wf}\n')
    print(f'{save_file} save done.')

def main():
    parser = argparse.ArgumentParser(description='Ko To Entrez.')
    parser.add_argument('-k', dest='related_ko_file',
                        default='../data/map05010.ko',
                        help='default: ../data/map05010.ko')
    parser.add_argument('-p', dest='conv_save_path',
                        default='../data/ko_conv_dir',
                        help='default: ../data/ko_conv_dir')
    parser.add_argument('-s', dest='conv_map_file',
                        default='../data/ko2entrez.txt',
                        help='default: ../data/ko2entrez.txt')
    args = parser.parse_args()

    ko_set = read_ko_file(args.related_ko_file)
    input('KO read done. type anything for continue.')
    run_conv(ko_set, args.conv_save_path)
    input('KO conv done. type anything for continue')
    save_ko_map_file(args.conv_save_path, args.conv_map_file)


if __name__ == '__main__':
    main()

