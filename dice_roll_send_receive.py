import pika, sys, os, json
from dice_roll import dice_roll

def main():
    '''
    The main module is in charge of setting up rabbitMQ channel and declaring queue. 
    There are two queues use here:
        - "rolling" : used for receiving the input dice from main user's program
        - "rolling_result" : used for sending the dice roll result back to main user's program
    
    The imported function dice_roll is used for generating randomized roll result
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"));
    channel = connection.channel();

    channel.queue_declare(queue="rolling");
    channel.queue_declare(queue="rolling_result");

    def callback(ch, method, properties, body):
        '''
        callback function used to take in the body from basic_consume and converted that into JSON.
        This function also handles calling dice_roll to generate randomized roll result.
        It will then send the roll result to the queue "rolling_result" back to the main user's program.
        '''
        
        body = json.loads(body);
        # call dice_roll(body) to get the randomized roll_result
        roll_result = dice_roll(body);
        # send roll_result to queue "rolling_result"
        channel.basic_publish(exchange='',
                              routing_key="rolling_result",
                              body = json.dumps(roll_result));

        # close connection for clean exit
        connection.close();

    channel.basic_consume(queue="rolling",
                            auto_ack=True,
                            on_message_callback=callback);

    channel.start_consuming();


if __name__ == '__main__':
    try:
        main();
    except KeyboardInterrupt:
        print("Keyboard Interrupted");
        try:
            sys.exit(0);
        except SystemExit:
            os._exit(0);

