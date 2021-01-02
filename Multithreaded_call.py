# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 02/01/2021 19:17
@Author: XINZHI YAO
"""

import os
import argparse
from multiprocessing import Process


def Multithreaded_call(temp_path: str, function: str,
                       save_path: str):

    file_list = os.listdir(temp_path)

    pool_list = []
    for process_idx, file in enumerate(file_list):
        pubtator_file = f'{temp_path}/{file}'

        pool_list.append(f'process_{process_idx}')
        exec(f'process_{process_idx}=Process(target={function}, '
             f'args=("{pubtator_file}", "{save_path}", {process_idx}))')

    for pool in pool_list:
        exec(f'{pool}.start()')
        print(f'{pool} running.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded call.')
    parser.add_argument('-ip', dest='iteration_path', type=str,
                        help='Contains the directory of split files that need to be processed iteratively.')
    parser.add_argument('-sp', dest='save_path', type=str,
                        help='Directory for storing multi-process results.')
    parser.add_argument('-fc', dest='target_function', type=str,
                        help='The target function needs to accept three parameters:'
                             'split_file: str, save_path: str, process_id: str.')
    args = parser.parse_args()

    Multithreaded_call(args.iteration_path, args.target_function, args.save_path)

