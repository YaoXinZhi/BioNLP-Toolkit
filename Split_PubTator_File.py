# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 28/12/2020 9:16
@Author: XINZHI YAO
"""

import os
import argparse


def pubtator_split(pubtator_file: str, num_per_file: int,
                   save_path: str):

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    split_file_idx = 0
    file_save_num = 0

    base_prefix = os.path.basename(pubtator_file).split('.')[0]

    save_file = f'{save_path}/{base_prefix}.{split_file_idx}.txt'
    wf = open(save_file, 'w')

    with open(pubtator_file) as f:
        for line in f:
            l = line.strip().split('|')
            if l == ['']:
                pass
                # wf.write('\n')

            if len(l) > 2:
                if l[1] == 't':

                    file_save_num += 1
                    if file_save_num % num_per_file == 0:
                        print(f'{base_prefix}.{split_file_idx}.txt save done.')
                        wf.close()
                        split_file_idx += 1
                        save_file = f'{save_path}/{base_prefix}.{split_file_idx}.txt'
                        wf = open(save_file, 'w')

                    wf.write(f'{line.strip()}\n')

                elif l[1] == 'a':
                    wf.write(f'{line.strip()}\n')
            else:
                wf.write(f'{line.strip()}\n')

    print(f'{base_prefix}.{split_file_idx}.txt save done.')
    wf.close()

if __name__  == '__main__':
    parser = argparse.ArgumentParser(description='PubTator Split.')
    parser.add_argument('-pf', dest='pubtator_file', type=str, required=True)
    parser.add_argument('-pn', dest='pubtator_num_per_file', type=int,
                        default=2000, help='default: 2000')
    parser.add_argument('-sp', dest='split_path', type=str, required=True)
    args = parser.parse_args()


    pubtator_split(args.pubtator_file, args.pubtator_num_per_file, args.split_path)

