import struct
from modules.common.message.tools.proto import message_bag_pb2 as message_bag
import modules_common_driving_record_proto_record_pb2 as driving_record
from modules.common.adapters.proto import adapter_config_pb2 as adapter_config
from modules.msgs.localization.proto.localization_pb2 import Localization
path = '/onboard_data/bags/meishangang/howo40/20220101/0940/howo40_2022_01_01_11_13_01_92.msg'
#get header
bag_header = message_bag.BagHeader()
fin = open(path,"rb")
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
count = 0
for unit in bag_index.units:
    fin.seek(unit.chunk_offset)
    bag_chunk = message_bag.BagDataChunk()
    l, = struct.unpack('L',fin.read(8))
    data = fin.read(l)
    bag_chunk.ParseFromString(data)
    message_type = bag_chunk.data_header.message_type
    if message_type == adapter_config.AdapterConfig.LOCALIZATION:
        loc = Localization()
        loc.ParseFromString(bag_chunk.message_data)
        print("loc_message %d:" % count)
        count +=1
        print(loc)


'''
batch_record = driving_record.BatchRecord()
record = batch_record.records.add()
record.ParseFromString(d.message_data)
json_string = json_format.MessageToJson(batch_record,preserving_proto_field_name=True)
print(json_string)
new_batch = driving_record.BatchRecord()
json_format.Parse(json_string,new_batch)
print(new_batch)
'''

