from kafka import KafkaProducer
import json
import argparse
import logging


class opt:
    appId = ''
    serializer = False
    text = False
    value = ''
    key = None
    filePath = None
    yaml = 'config.yaml'
    brokers = ''


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--appId', type=str, default='', help='topic ID')
    parser.add_argument('--brokers', type=str, default='localhost:9092', help='ip:port')
    parser.add_argument('--metas', type=str, default='', help='Additional data is required')
    parser.add_argument('--serializer', type=bool, default=False, help='Whether to use a serializer')
    parser.add_argument('--text', type=bool, default=False, help='Data type is text, Otherwise, the data type is binary')
    parser.add_argument('--value', type=str, default='', help='content you want to send')
    parser.add_argument('--key', type=str, default=None, help='The key that needs to be sent')# byte,bytearray,memoryview
    parser.add_argument('--filePath', type=str, default='', help='The address of binary data')
    parser.add_argument('--decodeType', type=str, default=None, help='How to decode binary files')
    return parser.parse_known_args()[0] if known else parser.parse_args()


class BusSender:
    def __init__(self):
        self.brokers = opt.brokers
        self.appId = opt.appId
        self.appId = 'test'
        self.metas = opt.metas
        self.serializer = opt.serializer
        print('opts.serializer:', opt.serializer)
        opt.serializer = True
        self.key = opt.key
        self.value = opt.value
        self.filePath = opt.filePath
        self.decodeType = opt.decodeType

    def getBusTextSender(self):
        BusTextSender = {}
        BusTextSender['appId'] = self.appId

        metas = self.metas
        in_metas = metas.split(',')
        metas_dict = {}
        if len(self.metas.split(',')) % 2:
            logging.warning('The metas input should be even')
            for i in range(0, len(self.metas.split(',')) - 1, 2):
                metas_dict[in_metas[i]] = in_metas[i + 1]
        else:
            for i in range(0, len(self.metas.split(',')), 2):
                metas_dict[in_metas[i]] = in_metas[i + 1]
        print('metas_dict:',metas_dict)
        if 'compression_type' in in_metas:
            if metas_dict['compression_type'] == 'None':
                metas_dict['compression_type'] = None
        else:
            metas_dict['compression_type'] = None
        BusTextSender['metas'] = self.metas

        if self.serializer:
            BusTextSender['serializer'] = lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8')
        else:
            BusTextSender['serializer'] = ''

        BusTextSender['produce'] = KafkaProducer(value_serializer=BusTextSender['serializer'],  #'localhost:9092'
                                                 bootstrap_servers=self.brokers,
                                                 api_version=(0, 10, 2)
                                                 # compression_type=BusTextSender['metas']['compression_type']
                                                 )
        #BusTextSender.append(produce)

        return BusTextSender


opt = parse_opt()
BusSender.__init__(opt)
BusTextSender = BusSender.getBusTextSender(opt)
# print('compression_type:', BusTextSender[1]['compression_type'])
print("BusTextSender['produce']:", BusTextSender['produce'])
print("BusTextSender['serializer']:", BusTextSender['serializer'])
print(type(opt))
# BusTextSender[-1].send(BusTextSender[0], value = BusTextSender[1])
# produce.close()
'''opt = parse_opt()
print(opt.appId)
assert opt.appId is not None,"appId is empty, you can try python XXX.py --appId='test'"
print('text:',opt.text)
in_metas = opt.metas.split(',')
print('metas:',len(opt.metas.split(',')))

metas_dict = {}
if len(opt.metas.split(',')) % 2:
    logging.warning('The metas input should be even,')
    for i in range(0, len(opt.metas.split(','))-1, 2):
        metas_dict[in_metas[i]] = in_metas[i + 1]
else:
    for i in range(0,len(opt.metas.split(',')),2):
        metas_dict[in_metas[i]] = in_metas[i+1]
print(metas_dict)'''
