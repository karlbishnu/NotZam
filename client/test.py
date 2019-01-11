from common.mq.kafka import consumer

if __name__ == '__main__':
    consumer = consumer('yumyeonhanuiMBP:9092', 'UPLOADS')
    for msg in consumer:
        print(msg)
