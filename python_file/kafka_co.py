from kafka import KafkaConsumer

consumer = KafkaConsumer('test',
                         group_id="group2",
                         bootstrap_servers=["10.63.20.68:9092"])

for msg in consumer:
    print(msg.value)