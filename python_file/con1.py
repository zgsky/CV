from kafka import KafkaConsumer
import json
import argparse


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--appId', type=str, default='', help='topic ID')
    parser.add_argument('--appIp', type=str, default='localhost:9092', help='IP')
    parser.add_argument('--deserializer', type=bool, default=False, help='Whether to use a serializer')
    # parser.add_argument('--filePath', type=str, default='', help='The address of binary data')
    return parser.parse_known_args()[0] if known else parser.parse_args()

# opt = parse_opt(True)
# print(opt.appId)
'''
class BusConsumer:
    def __init__(self,opt):
        self.appId = opt.appId
        self.metas = opt.metas
        self.serializer = opt.serializer
        self.key = opt.key
        self.filePath = opt.filePath
        self.decodeType = opt.decodeType

    def getBusTextConsumer(self):
        return

    def getBusStreamConsumer(self):
        return'''


# 文本数据
class BusTextConsumer:
    def __init__(self,opt):
        self.appIp = opt.appIp
        self.deserializer = opt.deserializer
        self.value = opt.value
        self.appId = opt.appId
        self.consumer = KafkaConsumer(bootstrap_servers=opt.appIp,
                                     group_id='my_group',
                                    api_version=(0, 10, 2)
                                     )
    # 发送数据
    def receive(self):
        text_msg = ''
        self.consumer.subscribe(topics=[self.appId])

        for message in self.consumer:
            if self.deserializer:
                text_msg = message.value().decode()
            else:
                text_msg = message.value()

        return text_msg

    # 关闭生产者
    def close(self):
        try:
            self.consumer.close()
        except KeyboardInterrupt:
            pass


class BusStreamConsumer:
    def __init__(self,opt):
        self.appIp = opt.appIp
        self.deserializer = opt.deserializer
        self.appId = opt.appId
        self.consumer = KafkaConsumer(bootstrap_servers=self.appIp,
                                     group_ip='my_group',
                                     )
    # 发送数据
    def receive(self):
        binary_msg = b''
        self.consumer.subscribe(self.appId)
        for message in self.consumer:
            binary_msg = message.value()

        return binary_msg
    # 关闭生产者
    def close(self):
        try:
            self.consumer.close()
        except KeyboardInterrupt:
            pass


