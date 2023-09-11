from kafka import KafkaConsumer
import yaml
import argparse
import time


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--appId', type=str, default='', help='topic ID')
    parser.add_argument('--appIp', type=str, default='localhost:9092', help='IP')
    # parser.add_argument('--deserializer', type=bool, default=False, help='Whether to use a serializer')
    parser.add_argument('--text', type=bool, default=False,
                        help='Data type is text, Otherwise, the data type is binary')
    # parser.add_argument('--filePath', type=str, default='', help='The address of binary data')
    parser.add_argument('--yaml', type=str, default='config.yaml', help="yaml path")
    return parser.parse_known_args()[0] if known else parser.parse_args()


# opt = parse_opt(True)
# print(opt.appId)
#
class BusTextConsumer:
    def __init__(self):
        self.appIp = opt.appIp
        # self.deserializer = opt.deserializer
        # self.value = opt.value
        self.appId = opt.appId

    #
    def receive(self, consumer):
        text_msg = ''
        consumer.subscribe(topics=[self.appId])

        for message in consumer:
            print(message)
            print(f"topic = {message.topic}")
            print(f"value = {message.value.decode()}")
            text_msg = message.value.decode()
        return text_msg

    #
    def close(self, consumer):
        try:
            consumer.close()
        except KeyboardInterrupt:
            pass


class BusStreamConsumer:
    def __init__(self):
        self.appIp = opt.appIp
        # self.deserializer = opt.deserializer
        self.appId = opt.appId

    #
    def receive(self, consumer):
        binary_msg = b''
        consumer.subscribe(topics=[self.appId])
        for message in consumer:
            print(message)
            print(f"topic = {message.topic}")
            print(f"value = {message.value}")
            binary_msg = message.value
        return binary_msg

    #
    def close(self, consumer):
        try:
            consumer.close()
        except KeyboardInterrupt:
            pass


def consumer_init(opt):
    with open(opt.yaml, 'r') as file:
        properties = yaml.safe_load(file)

    consumer = KafkaConsumer(bootstrap_servers=properties['bootstrap_servers'],
                             group_id='my_group',
                             api_version=(0, 10, 2)
                             )
    return consumer


if __name__ == '__main__':
    try:
        opt = parse_opt(True)

        assert opt.appId != '', "appId is empty, you can try python consumer.py --appId='test_topic'"

        consumer = consumer_init(opt)
        if opt.text:
            BusStreamConsumer.receive(opt, consumer)
            BusStreamConsumer.close(opt, consumer)
        else:
            BusTextConsumer.receive(opt, consumer)
            BusTextConsumer.close(opt, consumer)
    except KeyboardInterrupt:
        pass
