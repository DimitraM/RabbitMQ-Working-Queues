import pika
import sys, os
from datetime import datetime

def callback(ch, method, properties, body):
    message_id = properties.message_id
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f" [x] Received message ID: {message_id}, Received time: {timestamp}, Body: {body.decode()}")

def consumer():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')

    # Declare a queue with a random name (RabbitMQ will generate a unique queue name)
    result = channel.queue_declare(queue='queue_2')
    queue_name = result.method.queue

    # Specify the binding key
    bindingKey = 'key1'
    # Bind the queue to the exchange
    channel.queue_bind(exchange='direct_exchange', queue=queue_name,routing_key=bindingKey)

    # Set up a consumer callback function
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)