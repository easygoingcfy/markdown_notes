# coding=utf-8
import os
import re
import sys
import time
import struct
import requests
import argparse

from modules.common.message.tools.proto import message_bag_pb2 as message_bag
import modules_common_driving_record_proto_record_pb2 as driving_record
from modules.common.adapters.proto import adapter_config_pb2 as adapter_config
from modules.msgs.localization.proto.localization_pb2 import Localization
from google.protobuf import text_format,json_format

LOC_MIN_DELTA_TIME = 1e-1

def get_path(root_path,date,file_str):
    '''
    输入根目录，时间，和文件名，使用正则表达式匹配，返回所有匹配文件的完整路径
    '''
    if not os.path.exists(root_path):
        print('root_dir dont exist')
        return
    t_s = time.mktime(time.localtime())
    vehicle_list = os.listdir(root_path)
    vehicle_list.sort()
    path_dict = dict()
    for vehicle_name in vehicle_list:
        if vehicle_name[:4] != 'howo':
            continue
        print(vehicle_name)
        root = root_path + vehicle_name + '/' + date
        if os.path.exists(root):
            file_dirs = os.listdir(root)
            file_dirs.sort()
            for file_dir in file_dirs:
                file_list = os.listdir(root + '/' + file_dir)
                file_list.sort()
                for file_name in file_list:
                    if re.match(".*%s"%file_str,file_name)!= None:
                        fullpath = root + '/' + file_dir + '/' + file_name
                        if vehicle_name in path_dict:
                            path_dict[vehicle_name].append(fullpath)
                        else:
                            path_dict[vehicle_name] = [fullpath]
        else:
            print('path dont exist')
            continue
    t_e = time.mktime(time.localtime())
    print(type(t_e))
    print(type(1e6))
    print('get_path cost: %f ns' % ((t_e - t_s)*1e9))
    return path_dict


def update_record_list(record_list,data):
    if data.header.module_name == "localization":
        record_list.utm_x.append(data.utm_x)
