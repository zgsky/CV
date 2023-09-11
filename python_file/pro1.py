from kafka import KafkaProducer
import json
import argparse
import logging
import yaml


class opt:
    appId = ''
    serializer = False
    text = False
    value = ''
    key = None
    filePath = None
    yaml = 'config.yaml'
    metas = 'None'


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--appId', type=str, default='', help='topic ID')
    parser.add_argument('--brokers', type=str, default='localhost:9092', help='ip:port')
    parser.add_argument('--metas', type=str, default='None', help='Additional data is required')
    parser.add_argument('--serializer', type=bool, default=False, help='Whether to use a serializer')
    parser.add_argument('--text', type=bool, default=False, help='Data type is text, Otherwise, the data type is binary')
    parser.add_argument('--value', type=str, default='', help='content you want to send')
    parser.add_argument('--key', type=str, default=None, help='The key that needs to be sent')  # byte,bytearray,memoryview
    parser.add_argument('--filePath', type=str, default=None, help='The address of binary data')
    parser.add_argument('--decodeType', type=str, default=None, help="None, 'gzip', 'lz4', 'snappy'")
    parser.add_argument('--yaml', type=str, default='config.yaml', help="yaml path")
    return parser.parse_known_args()[0] if known else parser.parse_args()


class BusSender:
    def __init__(self):
        with open(opt.yaml, 'r') as file:
            properties = yaml.safe_load(file)
        self.brokers = properties['bootstrap_servers'].split(',')
        self.compression_type = properties['compression_type']
        if self.compression_type == 'None' or self.compression_type == 'none':
            self.compression_type = None
        self.serializer = properties['serializer']
        opt.serializer = properties['serializer']
        self.acks = properties['acks']
        self.buffer_memory = properties['buffer_memory']
        self.request_timeout_ms = properties['request_timeout_ms']
        self.batch_size = properties['batch_size']
        self.max_request_size = properties['max_request_size']
        self.linger_ms = properties['linger_ms']

        self.appId = opt.appId
        self.metas = opt.metas
        self.key = opt.key
        self.value = opt.value
        self.filePath = opt.filePath
        # self.decodeType = opt.decodeType

    def getBusTextSender(self):
        # print('brokers:', self.brokers)
        Bus_Text_Sender = []
        # 0 add appId
        Bus_Text_Sender.append(self.appId)

        # 1 add metas
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
        # print(metas_dict)
        if 'compression_type' in in_metas:
            if metas_dict['compression_type'] == 'None':
                metas_dict['compression_type'] = None
        else:
            metas_dict['compression_type'] = None
        Bus_Text_Sender.append(metas_dict)

        # 2 add serializer
        if self.serializer:
            Bus_Text_Sender.append(lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8'))
        else:
            Bus_Text_Sender.append('')

        # 3 add producer
        producer = KafkaProducer(value_serializer=Bus_Text_Sender[2],
                                 bootstrap_servers=self.brokers,       # 'localhost:9092'
                                 api_version=(0, 10, 2),
                                 compression_type=self.compression_type,
                                 acks=self.acks,
                                 batch_size=self.batch_size,
                                 buffer_memory=self.buffer_memory,
                                 request_timeout_ms=self.request_timeout_ms,
                                 max_request_size=self.max_request_size,
                                 linger_ms=self.linger_ms
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
        if len(self.metas.split(',')) % 2:
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
        Bus_Stream_Sender.append(metas_dict)

        # 2 add serializer
        if self.serializer:
            Bus_Stream_Sender.append(lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8'))
        else:
            Bus_Stream_Sender.append('')

        # 3 add filePath
        Bus_Stream_Sender.append(self.filePath)

        # 4 add producer
        producer = KafkaProducer(value_serializer=Bus_Stream_Sender[2],
                                 bootstrap_servers=self.brokers,  # 'localhost:9092'
                                 api_version=(0, 10, 2),
                                 compression_type=self.compression_type,
                                 acks=self.acks,
                                 batch_size=self.batch_size,
                                 buffer_memory=self.buffer_memory,
                                 request_timeout_ms=self.request_timeout_ms,
                                 max_request_size=self.max_request_size,
                                 linger_ms=self.linger_ms
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

    def close(self, producer):
        try:
            producer.close()
        except KeyboardInterrupt:
            pass


class BusStreamSender:
    def __init__(self, opt):
        self.appId = opt.appId
        self.key = opt.key
        self.value = opt.value
        self.filePath = opt.filePath
        self.decodeType = opt.decodeType

    def send(self, producer):
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

    def close(self, producer):
        try:
            producer.close()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    opt = parse_opt(True)

    BusSender.__init__(opt)
    if opt.text:
        Text = BusSender.getBusTextSender(opt)
        BusTextSender.send(opt, Text[-1])
        BusTextSender.close(opt, Text[-1])
    else:
        Stream = BusSender.getBusStreamSender(opt)
        BusStreamSender.send(opt, Stream[-1])
        BusStreamSender.close(opt, Stream[-1])