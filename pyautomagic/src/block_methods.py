from typing import List
import logging
import numpy as np
import os
import re

logger = logging.getLogger(__name__)

def extract_unique_filename(data_path,data_name,subject_name):
    if not subject_name in data_path:
        raise ValueError('Data path not associated with subject.')
    else:
        path_split = os.path.split(data_path)
        potential_base,remaining_path  = path_split[1], path_split[0]
        relative_path_additions = list()
        while not potential_base == subject_name:
            relative_path_additions.append(potential_base)
            path_split = os.path.split(remaining_path)
            potential_base,remaining_path  = path_split[1], path_split[0]
        path = os.path.join(subject_name,relative_path_additions,data_name)
        path.replace(os.sep,'_')
        unique_name = path.replace(os.sep,'_')
    return unique_name

def potential_result_path(data_path,data_name,subject_name,subject_result_folder):
    if not subject_name in data_path:
        raise ValueError('Data path not associated with subject.')
    else:
        path_split = os.path.split(data_path)
        potential_base,remaining_path  = path_split[1], path_split[0]
        relative_path_additions = list()
        while not potential_base == subject_name:
            relative_path_additions.append(potential_base)
            path_split = os.path.split(remaining_path)
            potential_base,remaining_path  = path_split[1], path_split[0]
        path = os.path.join(subject_result_folder,relative_path_additions)
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        filematch = [f for f in onlyfiles if data_name in onlyfiles(f)]
        if not filematch:
            return ''
        else:
            return filematch

def has_info(prefix: str):
    if not isinstance(has_info,str):
        #raise(TypeError,'Incorrect prefix input type.')
        return
    else:
        has_information = True
        if len(prefix) < 3 or prefix == '' or prefix[0] == 'n':
            has_information = False
    return has_information

def extract_rate_from_prefix(prefix: str):
    if not isinstance(has_info,str):
        #raise(TypeError,'Incorrect prefix input type.')
        return
    else:
        if prefix == '' or prefix[0] == 'n':
            rating = 'not_rated'
        elif prefix[0] == 'i':
            rating = 'interpolated'
        elif prefix[0] == 'g':
            rating = 'good'
        elif prefix[0] == 'b':
            rating = 'bad'
        elif prefix[0] == 'o':
            rating = 'ok'
    return rating

def extract_prefix(result_path: str):
    if not isinstance(result_path,str):
        return
    else:
        result_file = os.path.basename(result_path)
        result_file = os.path.splitext(result_file)[0]
        prefix = result_file.split('_')[0]
        if prefix == '':
            return prefix
        else:
            prefix_regex = re.compile(r'[nigbo]+i?p$')
            valid_prefix = prefix_regex.search(prefix)
            if valid_prefix:
                return prefix
            else:
                raise ValueError('Prefix of path is not valid')

def update_prefix(is_interpolated: bool,rate: str,prefix,commitedN: float):
    if not isinstance(is_interpolated,bool) or not isinstance(rate,str) or not isinstance(commitedN,float):
        raise(Exception)
        part3 = 'p'
        if is_interpolated:
            part2 = 'i'
        else:
            part2 = ''
        part1 = rate[0].lower()
        if not prefix or commitedN <=1:
            updated_prefix = part1+part2+part3
        else:
            updated_prefix = part1+prefix[:-1]+part2+part3
        return updated_prefix