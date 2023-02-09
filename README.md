# CS-361-Dice-Rolling-Microservice
A microservice that will generate an array containing arrays of random integers representing dice roll.

## Overview
This microservice will take in an input parameter, which is an array of integers. It will then return an array of arrays containing random integers, with each array representing a random die roll. The number of rolls is determined by the value of the input array's integers.

### Communication
The communication pipeline is hosted on `localhost`. Sending/Receiving data is done via queues on [RabbitMQ](https://www.rabbitmq.com/getstarted.html).

### Sending Data
The data is send by first establishing a channel on `localhost`. The user will then declare a queue by referening the queue's name, and send the data via `channel.basic_publish()` function (See example below).

```
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
```

Here, the user opens the channel on `localhost`, and sets up the queue named `rolling`. The user then sends the input data, which is an array containing six integers via `channel.basic_publish()` function. `exchange` is left blank since `localhost` is being used, while the `routing_key` argument must match the queue's name for verification purpose. The `body` argument contains the input data that is being send out. 

### Receiving Data
Receiving data is pretty much the same as sending data. To get the actual data, however, the user must provide a callback function when receiving in order to convert the body message into a usable format, which is JSON in this case. See the example below.

```
import pika, json, time, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"));
    channel = connection.channel();

    channel.queue_declare(queue="rolling");

    def callback(ch, method, properties, body):
        
        body = json.loads(body); 

        print(f"Receiving dice roll result = {body}");

        connection.close();

    channel.basic_consume(queue="rolling",
                            auto_ack=True,
                            on_message_callback=callback);

    print(" [*] Waiting for messages from dice_roll. Press Ctrl + C to exit");
    channel.start_consuming()
```

Here, the user provides the callback function that converts the `body` into JSON format, since RabbitMQ transfers data using bytes format. The `channel.basic_consume()` handles the receiving function by providing the queue's name that matches the `routing_key` in the previous Send program. It also contains a `callback` function that handles formating the `body`, which contains the data in bytes format, and converts that into JSON.

### UML Sequence Diagram

![uml_diagram](./image/uml_diagram.jpg?raw=True "UML Diagram")


### Testing
To test the microservice, first make sure you have RabbitMQ installed, along with the Python pika package, and do the following

1. Open up three separate terminals
2. The first terminal should be at the current directory that contains the `dice_roll_send_receive.py` file
3. On the other terminals, type `cd CS-361-Dice-Rolling-Microservice/test/` to navigate to the test directory
4. Run the `dice_roll_send_receive.py` on the first terminal, and the `test_receive.py` and `test_send.py` in the other terminals
5. The terminals should display messages that tell the users the data is being sent, with `test_receive.py` displaying the result array

The `test_send.py` contains a sample input array of six integers, along with the channelt set up on localhost and the queue `rolling` declared. This queue will send the input array to `dice_roll_send_receive.py` microservice. This microservice will then generate an array containing random dice rolls. It also declares another queue `rolling_result`, which it will send the result to. Finally, the data is received on `test_receive.py` program and is printed to the terminal.