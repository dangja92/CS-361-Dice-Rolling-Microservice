import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"));
channel = connection.channel();

channel.queue_declare(queue="rolling");

input_array = [2, 0, 1, 2, 0, 2]
channel.basic_publish(exchange  = '',
                    routing_key = "rolling",
                    body        = json.dumps(input_array));

print(" [x] Sent an input array!");

connection.close();