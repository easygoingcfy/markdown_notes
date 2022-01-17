import os
import modules_common_driving_record_proto_record_pb2
# import google.protobuf.text_format as text_format
# import google.protobuf.json_format as json_format
from google.protobuf import text_format,json_format
def recordB_to_proto(path):
    record = modules_common_driving_record_proto_record_pb2.Record()
    f = open(path,"rb")
    text_format.Parse(f.read(), record)
    f.close()
    #message to Json
    json_string = json_format.MessageToJson(record)
    return json_string
    print("message to json done")
if __name__ == '__main__':
    path = 'recordB'
    recordB_to_proto(path)
