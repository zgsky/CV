import yaml
# from pro1 import *
from pro1 import BusSender
from pro1 import opt

'''class opt:
    appId = ''
    serializer = False
    metas = 'None'
    text = False
    value = ''
    key = None
    filePath = None
    yaml = 'config.yaml'''


BusSender.__init__(opt)


# 读取YAML文件
with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)


# 打印字典数据
print(data['bootstrap_servers'].split(',')[0])
print(len(data['bootstrap_servers'].split(',')))
print(type(data))
print(opt.metas)