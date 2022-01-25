# coding=utf-8
import os
import sys
import time
import struct
import requests
from modules.common.message.tools.proto import message_bag_pb2 as message_bag
import modules_common_driving_record_proto_record_pb2 as driving_record
from modules.common.adapters.proto import adapter_config_pb2 as adapter_config
from modules.msgs.localization.proto.localization_pb2 import Localization 

from google.protobuf import text_format,json_format
def get_time(time_str):
    time_tuple = time.strptime(time_str,"%Y_%m_%d_%H_%M_%S")
    return time.mktime(time_tuple)
#-----------------------------------------------------
class TakeOver:                         #take_over对象用来存储一个record_list以及对应的message（localization）数据
    def __init__(self,vehicle,record_record_list):
        self.vehicle_name = vehicle
        self.record = record_record_list
        self.messages = []
#------------------------------------------
print(adapter_config.AdapterConfig.LOCALIZATION)
take_over_list = dict(howo40=[])
path_list = {'howo40':['/onboard_data/bags/meishangang/howo40/20220101/0940']}
for vehicle,paths in path_list.items():
    for path in paths:                  #对每个路径中的record和msg进行处理
        fullpath = path + '/' + 'recordB'
        #读recordB
        if os.path.isfile(fullpath):
            f = open(fullpath,'rb')
            print('open file:'+fullpath)
        else:
            print('recordB dont exist')
            continue
        try:
            record = driving_record.Record() 
            text_format.Parse(f.read(),record)
            print('record parse done')
        except text_format.ParseError as e:
            print(msg_file + ":Parse error!!!!!!!!")
            print(e)
        f.close()
        #处理一下Msg文件（提取时间信息并排序）
        file_list = os.listdir(path)
        msg_file_time = []      #存放排序好后的文件名
        msg_file_list = []      #存放文件名对应的时间
        for one_file in file_list:
            if one_file[:len(vehicle)] == vehicle:
                msg_file_list.append(one_file)
                msg_file_time.append(get_time(one_file[len(vehicle)+1:len(vehicle)+20]))
        msg_file_list.sort()
        msg_file_time.sort()    #此处可能可以优化
        print("排序数据:")
        print(msg_file_list)
        print(len(msg_file_list))
        print(msg_file_time)
        #在msg文件中匹配record_list
        for record_list in record.record_list:
            record_time = record_list.timestamp_sec
            take_over = TakeOver(vehicle,record_list)   #take_over对象用来存储一个record_list以及对应的message（localization）数据
            #根据时间筛选文件
            index = -1
            for i in range(0,len(msg_file_time)):
                if record_time < msg_file_time[i]:
                    index = i-1
                    break
            if index < 0 or record_time < msg_file_time[index]:
                print('no time match msg file')
                continue
            print('read msg file:' + path + '/' + msg_file_list[index])
            #在匹配的msg文件中提取数据
            fin = open(path + '/' + msg_file_list[index],'rb')
            bag_header = message_bag.BagHeader()
            l, = struct.unpack('L',fin.read(8))
            data = fin.read(l)
            bag_header.ParseFromString(data)
            #get index
            fin.seek(bag_header.index_offset)
            bag_index = message_bag.BagIndex()
            l, = struct.unpack('L',fin.read(8))
            data = fin.read(l)
            bag_index.ParseFromString(data)
            #get BagDataChunk
            for unit in bag_index.units:
                fin.seek(unit.chunk_offset)
                bag_chunk = message_bag.BagDataChunk()
                l, = struct.unpack('L',fin.read(8))
                data = fin.read(l)
                bag_chunk.ParseFromString(data)
                message_type = bag_chunk.data_header.message_type
                #判断类型
                if message_type == adapter_config.AdapterConfig.LOCALIZATION:
                    loc = Localization()
                    loc.ParseFromString(bag_chunk.message_data)
                    #Match
                    min_delta_time = 1e-1
                    #print(loc.header.timestamp_sec)
                    if record_time > loc.header.timestamp_sec and record_time - loc.header.timestamp_sec < min_delta_time:
                        take_over.messages.append(loc)      #处理数据，现在是全部放到take_over中
            fin.close()
            take_over_list[vehicle].append(take_over)
            print('finish one record list')
#print部分
print('process done')
if len(take_over_list) == 0:
    print('no take over list')
    exit(0)
count_list = []
for _,take_overs in take_over_list.items():
    for take_over in take_overs:
        print('record_list:')
        print(take_over.record)
        print('matching message:')
        count = 0
        for loc in take_over.messages:
            count +=1
            print("no:%d" % count)
            print(loc)
        count_list.append(count)
print(count_list)
print(len(count_list))

