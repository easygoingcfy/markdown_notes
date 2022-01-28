from head import*

from Bag import Bag
from Record import Record
from BagParser import BagParser

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
                file_list = bag.select_file(vehicle,record_time)
                if file_list != None:
                    parser = BagParser(file_list,record_time)
                    print('index: %d' % parser.index)
                    parser.process_units(record_list)
                else:
                    continue
    print('total processed msg file: %d' % total_msg)
    #print(record.batch_record)
    print('post batch_record')
    url = "http://192.168.10.78:8070/api/records"
    #record.post_batch(url)
    print('done')


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
