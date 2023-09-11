from kafka import KafkaProducer
import json
import argparse
import logging

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--appId', type=str, default='', help='topic ID')
    parser.add_argument('--brokers', type=str, default='localhost:9092', help='ip:port')
    parser.add_argument('--metas', type=str, default='None', help='Additional data is required')
    parser.add_argument('--serializer', type=bool, default=False, help='Whether to use a serializer')
    parser.add_argument('--text', type=bool, default=False, help='Data type is text, Otherwise, the data type is binary')
    parser.add_argument('--value', type=str, default='', help='content you want to send')
    parser.add_argument('--key', type=str, default=None,help='The key that needs to be sent')  # byte,bytearray,memoryview
    parser.add_argument('--filePath', type=str, default=None, help='The address of binary data')
    parser.add_argument('--decodeType', type=str, default=None, help="None, 'gzip', 'lz4', 'snappy'")
    return parser.parse_known_args()[0] if known else parser.parse_args()

class BusSender:
    def __init__(self,opt):
        self.brokers = opt.brokers
        self.appId = opt.appId
        self.metas = opt.metas
        self.serializer = opt.serializer
        self.key = opt.key
        self.value = opt.value
        self.filePath = opt.filePath
        self.decodeType = opt.decodeType

    def getBusTextSender(self):
        # print('brokers:', self.brokers)
        Bus_Text_Sender = []
        # 0 add appId
        Bus_Text_Sender.append(self.appId)

        # 1 add metas
        metas = self.metas
        in_metas = metas.split(',')
        # print('len:',len(self.metas.split(',')))
        metas_dict = {}
        if len(in_metas) > 1:
            if len(in_metas) % 2:
                logging.warning('The metas input should be even')
                for i in range(0, len(self.metas.split(',')) - 1, 2):
                    metas_dict[in_metas[i]] = in_metas[i + 1]
            else:
                for i in range(0, len(self.metas.split(',')), 2):
                    metas_dict[in_metas[i]] = in_metas[i + 1]
        # print(metas_dict)
        if 'compression_type' in in_metas:
            if metas_dict['compression_type'] == 'None':
                metas_dict['compression_type'] = None
        else:
            metas_dict['compression_type'] = None
        print('compression_type:',metas_dict['compression_type'])
        Bus_Text_Sender.append(metas_dict)

        # 2 add serializer
        if self.serializer:
            Bus_Text_Sender.append(lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8'))
        else:
            Bus_Text_Sender.append('')

        # 3 add producer
        producer = KafkaProducer(value_serializer=Bus_Text_Sender[2],  # 'localhost:9092'
                                bootstrap_servers=self.brokers,
                                api_version=(0, 10, 2),
                                compression_type=Bus_Text_Sender[1]['compression_type']
                                )
        Bus_Text_Sender.append(producer)

        return Bus_Text_Sender

    def getBusStreamSender(self):
        Bus_Stream_Sender = []
        # 0 add appId
        Bus_Stream_Sender.append(self.appId)

        # 1 add metas
        metas = self.metas
        in_metas = metas.split(',')
        metas_dict = {}
        if len(in_metas) > 1:
            if len(in_metas) % 2:
                logging.warning('The metas input should be even')
                for i in range(0, len(self.metas.split(',')) - 1, 2):
                    metas_dict[in_metas[i]] = in_metas[i + 1]
            else:
                for i in range(0, len(self.metas.split(',')), 2):
                    metas_dict[in_metas[i]] = in_metas[i + 1]
        # print(metas_dict)
        if 'compression_type' in in_metas:
            if metas_dict['compression_type'] == 'None':
                metas_dict['compression_type'] = None
        else:
            metas_dict['compression_type'] = None
        print('compression_type:',metas_dict['compression_type'])
        Bus_Stream_Sender.append(metas_dict)

        # 2 add serializer
        if self.serializer:
            Bus_Stream_Sender.append(lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8'))
        else:
            Bus_Stream_Sender.append('')

        # 3 add filePath
        Bus_Stream_Sender.append(self.filePath)

        # 4 add producer
        producer = KafkaProducer(value_serializer=Bus_Stream_Sender[2],  # 'localhost:9092'
                                 bootstrap_servers=self.brokers,
                                 api_version=(0, 10, 2),
                                 compression_type=Bus_Stream_Sender[1]['compression_type']
                                 )
        Bus_Stream_Sender.append(producer)

        return Bus_Stream_Sender


class BusTextSender:
    def __init__(self, opt):
        self.serializer = opt.serializer
        self.value = opt.value
        self.metas = opt.metas
        self.appId = opt.appId
        self.key = opt.key
    #
    def send(self, producer):
        send_key = None
        if self.key:
            send_key = bytes(self.key, encoding='utf-8')
        if self.serializer:
            future = producer.send(self.appId, value=self.value, key=send_key)
        else:
            future = producer.send(self.appId, value=bytes(self.value, encoding='utf-8'), key=send_key)
        record_metadata = future.get(timeout=10)  #
        partition = record_metadata.partition  #
        offset = record_metadata.offset  #
        print('save success, partition: {}, offset: {}'.format(partition, offset))
    #
    def close(self, producer):
        try:
            producer.close()
        except KeyboardInterrupt:
            pass

#
class BusStreamSender:
    def __init__(self, opt):
        self.appIp = opt.appIp
        self.appId = opt.appId
        self.metas = opt.metas
        self.serializer = opt.serializer
        self.key = opt.key
        self.value = opt.value
        self.filePath = opt.filePath
        self.decodeType = opt.decodeType
    #
    def send(self,producer):
        send_key = None
        if self.key:
            send_key = bytes(self.key, encoding='utf-8')

        if self.filePath is None:
            future = producer.send(self.appId, value=bytes(self.value, encoding='utf-8'), key=send_key)
        else:
            with open(self.filePath, 'rb') as f:
                file_content = f.read()
            future = producer.send(self.appId, value=file_content, key=send_key)
        record_metadata = future.get(timeout=10)  #
        partition = record_metadata.partition  #
        offset = record_metadata.offset  #
        print('save success, partition: {}, offset: {}'.format(partition, offset))

    #
    def close(self,producer):
        try:
            producer.close()
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    opt = parse_opt(True)

    if opt.text:
        Text = BusSender.getBusTextSender(opt)
        BusTextSender.send(opt, Text[-1])
        BusTextSender.close(opt, Text[-1])
    else:
        Stream = BusSender.getBusStreamSender(opt)
        BusStreamSender.send(opt, Stream[-1])
        BusStreamSender.close(opt, Stream[-1])

