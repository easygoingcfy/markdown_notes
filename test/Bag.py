from head import * 


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
            if record_time-LOC_MIN_DELTA_TIME < self.file_time_dict[vehicle_name][i]:
                index = i - 1
                break
        if index < 0 or record_time + LOC_MIN_DELTA_TIME < self.file_time_dict[vehicle_name][index]:
            print('no time match file')
            return
        else:
            t_e = time.mktime(time.localtime())
            print('select_file cost: %f ns' % ((t_e - t_s)*1e9) )
            res_list = [self.file_dict[vehicle_name][index]]
            index += 1
            while index < len(self.file_time_dict[vehicle_name]):
                if record_time + LOC_MIN_DELTA_TIME > self.file_time_dict[vehicle_name][index]:
                    res_list.append(self.file_dict[vehicle_name][index])
                    index += 1
                else:
                    break
            return res_list


def get_time(time_str):
    time_tuple = time.strptime(time_str,"%Y_%m_%d_%H_%M_%S")
    return time.mktime(time_tuple)
