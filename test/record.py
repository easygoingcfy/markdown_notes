# coding=utf-8
import os
import re
import sys
import time
import struct
import requests
import argparse
#import msg_define
from modules.common.message.tools.proto import message_bag_pb2 as message_bag
import modules_common_driving_record_proto_record_pb2 as driving_record
from modules.common.adapters.proto import adapter_config_pb2 as adapter_config
from modules.msgs.localization.proto.localization_pb2 import Localization
from google.protobuf import text_format,json_format

LOC_MIN_DELTA_TIME = 1e-1
type_dict = {
        adapter_config.AdapterConfig.LOCALIZATION:LOC_MIN_DELTA_TIME
        }
class Record:
    def __init__(self,root_path,date):
        #self.date = date
        self.file_dict = get_path(root_path,date,'recordB')
        if self.file_dict != None:
            self.is_valid = True
            total = 0
            print('total vehicle:%d'%len(self.file_dict))
            for key,values in self.file_dict.items():
                print('vehicle:'+key)
                total += len(values)
                for value in values:
                    print(value)
            print('total:%d'%total)
        else:
            self.is_valid = False


    def parse(self,path):            
        '''
        解析文件
        '''
        if os.path.isfile(path):
            t_s = time.mktime(time.localtime())
            f = open(path,'rb')
            print('open file:'+path)
            try:
                record = driving_record.Record()
                text_format.Parse(f.read(),record)
                f.close()
                t_e = time.mktime(time.localtime())
                print('parse recordB cost: %f ns'% ((t_e-t_s)*1e9))
                return record
            except text_format.ParseError as e:
                print(path+'Parse error!!!!!!!!')
                print(e)
                f.close()
                return
        else:
            print('recordB dont exist')
            return


    def update_record(self,record,field):      
        '''
        提取需要的record_list,放到新的msg_record中
        '''
        t_s = time.mktime(time.localtime())
        new_record = driving_record.Record()
        for record_list in record.record_list:
            if eval('record_list.'+field):
                new_record_list = new_record.record_list.add()
                new_record_list.CopyFrom(record_list)
        t_e = time.mktime(time.localtime())
        print('update_record cost:%f ns' % ((t_e - t_s)*1e9) )
        return new_record


class Bag:
    def __init__(self,root_path,date):
        self.file_dict = get_path(root_path,date,'msg')
        self.file_time_dict = dict()
        if self.file_dict != None:
            self.is_valid = True
            self.get_time_dict(self.file_dict)
            total = 0
            for key,values in self.file_dict.items():
                print(key+':')
                print(len(values))
                total += len(values)
                for value in values:
                    print(value)
            print('total file:%d' % total)
        else:
            self.is_valid = False

    def get_time_dict(self,file_dict):
        t_s = time.mktime(time.localtime())
        for vehicle_name in file_dict:
            for file_name in file_dict[vehicle_name]:
                time_str = get_time(file_name.split(vehicle_name)[2][1:20])
                if vehicle_name in self.file_time_dict:
                    self.file_time_dict[vehicle_name].append(time_str)
                else:
                    self.file_time_dict[vehicle_name] = [time_str]
        t_e = time.mktime(time.localtime())
        print('get_time_dict cost: %f ns' % ((t_e - t_s)*1e9) )

    
    def select_file(self,vehicle_name,record_time):  
        '''
        根据时间筛选文件
        '''
        index = -1
        t_s = time.mktime(time.localtime())
        for i in range(0,len(self.file_time_dict[vehicle_name])):
            if record_time < self.file_time_dict[vehicle_name][i]:
                index = i - 1
                break
        if index < 0 or record_time < self.file_time_dict[vehicle_name][index]:
            print('no time match file')
            return  
        else:
            t_e = time.mktime(time.localtime())
            print('select_file cost: %f ns' % ((t_e - t_s)*1e9) )
            return self.file_dict[vehicle_name][index]


class BagParser:
    def __init__(self,file_path):
        self.path = file_path
        #self.msg_file = self.get_msg_file(self.path)
        self.bag_index = self.get_bag_index(self.path)
        self.index = 0

    def get_msg_file(self,file_path):
        t_s = time.mktime(time.localtime())
        f = open(file_path,'rb')
        msg_file = f.read()
        f.close()
        t_e = time.mktime(time.localtime())
        print('get_msg_file cost: %f ns' % ((t_e - t_s)*1e9))
        return msg_file


    def get_bag_index(self,file_path):  
        '''
        用来给self.bag_index初始化
        '''
        t_s = time.mktime(time.localtime())
        f = open(self.path,'rb')
        bag_header = message_bag.BagHeader()
        #l, = struct.unpack('L',self.msg_file[0:8])
        l, = struct.unpack('L',f.read(8))
        #data = self.msg_file[8:l+8]
        data = f.read(l)
        bag_header.ParseFromString(data)
        #get index
        p = bag_header.index_offset
        f.seek(p)
        bag_index = message_bag.BagIndex()
        #l, = struct.unpack('L',self.msg_file[p:p+8])
        l,  = struct.unpack('L',f.read(8))
        #data = self.msg_file[p+8:p+8+l]
        data = f.read(l)
        f.close()
        bag_index.ParseFromString(data)
        t_e = time.mktime(time.localtime())
        print('get_bag_index cost:%f ns' % ((t_e-t_s)*1e9))
        return bag_index
    
    '''
    def process_units(self,record_time):
        t_s = time.mktime(time.localtime())
        while self.index < len(self.bag_index.units):
            send_time = self.bag_index.units[self.index].data_header.send_time_ns / 1e9
            min_delta_time = 1e-1
            if record_time > send_time and record_time -send_time < min_delta_time:
                message_type = self.bag_index.units[self.index].data_header.message_type
                if message_type == adapter_config.AdapterConfig.LOCALIZATION:
                    loc = Localization()
                    p = self.bag_index.units[self.index].message_data_offset
                    data_lenth = self.bag_index.units[self.index].message_data_length
                    data = self.msg_file[p:p+data_lenth]
                    loc.ParseFromString(data)
                    print('process')
            self.index += 1
        t_e = time.mktime(time.localtime())
        print('process_units cost: %f ns' % ((t_e - t_s)*1e6))
    '''

    def process_units(self,record_time):
        t_s = time.mktime(time.localtime())
        while self.index < len(self.bag_index.units):
            send_time = self.bag_index.units[self.index].data_header.send_time_ns / 1e9
            min_delta_time = 1e-1
            if record_time > send_time and record_time -send_time < min_delta_time:
                message_type = self.bag_index.units[self.index].data_header.message_type
                if message_type == adapter_config.AdapterConfig.LOCALIZATION:
                    loc = Localization()
                    f = open(self.path,'rb')
                    p = self.bag_index.units[self.index].message_data_offset
                    f.seek(p)
                    l = self.bag_index.units[self.index].message_data_length
                    data = f.read(l)
                    f.close()
                    loc.ParseFromString(data)
                    print('process')
            self.index += 1
        t_e = time.mktime(time.localtime())
        print('process_units cost: %f ns' % ((t_e - t_s)*1e6))


def get_time(time_str):
    time_tuple = time.strptime(time_str,"%Y_%m_%d_%H_%M_%S")
    return time.mktime(time_tuple)


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


def process_data(record_list,loc):
    pass
    #time_str = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())


def process(root_path,date):
    record = Record(root_path,date)
    bag = Bag(root_path,date)
    total_msg = 0
    if not record.is_valid or not bag.is_valid:
        print('error:no match file')
        exit(0)
    for vehicle in record.file_dict:
        for record_file in record.file_dict[vehicle]:
            print('read recordB file')
            msg_record = record.update_record(record.parse(record_file),'take_over')
            for record_list in msg_record.record_list:
                #根据时间筛选文件
                record_time = record_list.timestamp_sec
                file_path = bag.select_file(vehicle,record_time)
                if file_path != None:
                    print('read file:'+ file_path)
                    total_msg += 1
                    parser = BagParser(file_path)
                    #bag_chunk = message_bag.BagDataChunk()
                    parser.process_units(record_time)
                else:
                    continue
    print('total processed msg file: %d' % total_msg)
            

if __name__ == '__main__':
    if (len(sys.argv)) < 2:
            print('usage: python record.py root_path')
    parser = argparse.ArgumentParser(
        description='for test')

    parser.add_argument(
        '-p','--path',action='store',type=str,required=True,
        help='provide the root_path')

    parser.add_argument(
        '-d','--date',action='store',type=str,required=True,
        help='provide the date')

    args = parser.parse_args()

    root_path = args.path
    date = args.date

    time_start = time.mktime(time.localtime())
    process(root_path,date)
    time_end = time.mktime(time.localtime())
    print('total time:%d s' % (time_end - time_start))

    '''
    parser = BagParser('/onboard_data/bags/meishangang/howo40/20220101/1405/howo40_2022_01_01_14_08_04_2.msg')
    bag_chunk = message_bag.BagDataChunk()
    while(parser.next_chunk(bag_chunk)):
        print(bag_chunk)
    '''
