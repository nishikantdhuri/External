import pika
import time
import os
conn=None
import requests

def connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('sender_queue'),durable=True)
    return channel


if __name__=='__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'),durable=True)


    def sleep():
        time.sleep(120)

    def callback(ch, method, properties, body):
        print('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        requests.post('http://'+str(os.environ.get('tracer_ip'))+':'+str(5000)+'/soc', json=dictToSend)
        sleep()
        global conn
        if conn == None:
            conn=connect()
        conn.basic_publish(body=os.environ.get('src_system'), exchange='', routing_key=os.environ.get('sender_queue'))

    channel.basic_consume(queue =os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()