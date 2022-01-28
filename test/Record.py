from head import*

class Record:
    def __init__(self,root_path,date):
        #self.date = date
        self.batch_record = driving_record.BatchRecord()
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


    def post_batch(self,url):
        '''
        post batch_record
        '''
        #url = "http://192.168.10.78:8070/api/records"
        t_s = time.mktime(time.localtime())
        json_string = json_format.MessageToJson(self.batch_record,preserving_proto_field_name=True)
        print("msg to json done")
        res = requests.post(url=url,data=json_string)
        print(res.text)
        t_e = time.mktime(time.localtime())
        print('post_batch cost:%f s' % (t_e - t_s) )


    def update_record(self,record,field):
        '''
        提取需要的record_list,放到新的msg_record中
        '''
        t_s = time.mktime(time.localtime())
        count_record_list = 0
        new_record = self.batch_record.records.add()
        for record_list in record.record_list:
            if eval('record_list.'+field):
                new_record_list = new_record.record_list.add()
                new_record_list.CopyFrom(record_list)
                count_record_list += 1
        t_e = time.mktime(time.localtime())
        print('update_record cost:%f ns' % ((t_e - t_s)*1e9) )
        print('record_list amount: %d' % count_record_list)
        return new_record
