from head import *

class BagParser:
    def __init__(self,file_path,record_time):
        self.list = file_path
        self.bag_index = []
        for one_file in self.list:
            self.bag_index.append(self.get_bag_index(one_file))
        self.index = self.set_index(record_time)

    
    def set_index(self,record_time):
        '''
        二分查找设置index的值
        '''
        l,r = 0,len(self.bag_index[0].units)-1
        print('index length:', r)
        while l < r:
            mid = (l+r)//2
            send_time = self.bag_index[0].units[mid].data_header.send_time_ns / 1e9
            if send_time < record_time-LOC_MIN_DELTA_TIME:  #此处可能需要用近似代替
                l = mid+1
            elif send_time > record_time-LOC_MIN_DELTA_TIME:
                r = mid-1
            else:
                return mid
        return l


    def get_bag_index(self,file_path):
        '''
        用来给self.bag_index初始化
        '''
        t_s = time.mktime(time.localtime())
        f = open(self.list[0],'rb')
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


    def process_units(self,record_list):
        t_s = time.mktime(time.localtime())
        record_time = record_list.timestamp_sec
        for i in range(len(self.list)):

            while self.index < len(self.bag_index[i].units):
                send_time = self.bag_index[i].units[self.index].data_header.send_time_ns / 1e9
                min_delta_time = 1e-1
                if abs(record_time -send_time) < min_delta_time:
                    message_type = self.bag_index[i].units[self.index].data_header.message_type
                    if message_type == adapter_config.AdapterConfig.LOCALIZATION:
                        loc = Localization()
                        f = open(self.list[i],'rb')
                        p = self.bag_index[i].units[self.index].message_data_offset
                        f.seek(p)
                        l = self.bag_index[i].units[self.index].message_data_length
                        data = f.read(l)
                        f.close()
                        loc.ParseFromString(data)
                        print('process')
                        #这里把循环放到外面，每次返回一个data，再处理会不会好一点
                        update_record_list(record_list,loc)
                self.index += 1

            self.index = 0

        t_e = time.mktime(time.localtime())
        print('process_units cost: %f ns' % ((t_e - t_s)*1e6))
