import pika, json, time, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"));
    channel = connection.channel();

    channel.queue_declare(queue="rolling_result");

    def callback(ch, method, properties, body):
        
        body = json.loads(body); 

        print(f"Receiving dice roll result = {body}");

        connection.close();

    channel.basic_consume(queue="rolling_result",
                            auto_ack=True,
                            on_message_callback=callback);

    print(" [*] Waiting for messages from dice_roll. Press Ctrl + C to exit");
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main();
    except KeyboardInterrupt:
        print("Keyboard Interrupted");
        try:
            sys.exit(0);
        except SystemExit:
            os._exit(0);