import os
import requests
import compatible_record_pb2  #自己增加了旧字段的兼容版本
# import modules_common_driving_record_proto_record_pb2
from google.protobuf import text_format,json_format
def get_path(date):
    headpath = "/onboard_data/bags/meishangang"
    lst_meishangang = os.listdir(headpath)
    res = []
    file_size = 0
    for x in lst_meishangang:                       #检索meishangang目录
       date_file = headpath +"/" + x +"/" + date
       if os.path.exists(date_file):
           lst_date = os.listdir(date_file)
           for y in lst_date:
               path = date_file + '/' + y + '/recordB'   #读取目标msg文件
               if os.path.exists(path):
                   size = os.path.getsize(path)
                   print(path+"size:%d"% size)
                   file_size +=size
                   res.append(path)
               else:
                   print(path+": not exist")
    print("文件总大小:%d" % file_size)
    return res
#--------------------------------------------------------
def post_message(path_list):
    url = "http://192.168.10.78:8070/api/records"
    # batch_record = modules_common_driving_record_proto_record_pb2.BatchRecord()
    batch_record = compatible_record_pb2.BatchRecord()
    # record = batch_record.records.add()
    for msg_file in path_list:
        f = open(msg_file,"rb")
        text_format.Parse(f.read(),batch_record.records.add() )#Parse 
        # text_format.Parse(f.read(),batch_record.records.add(),allow_unknown_field=True)  #仅测试用
        f.close()
    json_string = json_format.MessageToJson(batch_record,preserving_proto_field_name=True)
    print("msg to json done")
    res = requests.post(url=url,data=json_string)
    print(res.text)
#--------------------------------------------------------        
if __name__== '__main__':
    date = '20211231'
    path_list = get_path(date)
    print(path_list)
    print("文件数: %d" %  len(path_list))
    post_message(path_list)
