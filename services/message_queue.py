import pika
import json
import uuid

def setup_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='social_media_data')
    return channel

def send_message(channel, message):
    message_id = str(uuid.uuid4())
    channel.basic_publish(exchange='',
                          routing_key='social_media_data',
                          body=json.dumps({'id': message_id, 'content': message}),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

def receive_message(channel, callback):
    channel.basic_consume(queue='social_media_data',
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()