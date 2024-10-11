import time
import json
import random
from datetime import datetime
from confluent_kafka import Producer

# Define constants for Kafka topic and broker address
KAFKA_TOPIC = 'stock_data'
BROKER = 'kafka:9092'

# Generate a list of stock symbols (NIFTY50_1 to NIFTY50_50)
SYMBOLS = ['NIFTY50_' + str(i) for i in range(1, 51)]

def delivery_report(err, msg):
    """
    Callback function to report the delivery status of messages sent to Kafka.
    
    Parameters:
    err (Exception): An error that occurred during message delivery, if any.
    msg (Message): The message object that was attempted to be delivered.
    """
    if err is not None:
        print(f"Delivery failed for message {msg.key()}: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def generate_stock_data():
    """
    Generate a random stock data record.
    
    The stock data includes:
    - date: The current UTC date and time.
    - symbol_name: A randomly selected stock symbol from SYMBOLS.
    - open: The opening price, a random float between 1000 and 15000.
    - high: The highest price, slightly above the opening price.
    - low: The lowest price, slightly below the opening price.
    - close: The closing price, randomly chosen between low and high.
    
    Returns:
    dict: A dictionary containing the stock data.
    """
    symbol = random.choice(SYMBOLS)
    open_price = round(random.uniform(1000, 15000), 2)
    high = round(open_price + random.uniform(0, 100), 2)
    low = round(open_price - random.uniform(0, 100), 2)
    close = round(random.uniform(low, high), 2)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'date': timestamp,
        'symbol_name': symbol,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close
    }

def main():
    """
    Main function to produce stock data messages to a Kafka topic.
    
    This function initializes the Kafka producer and continuously generates 
    random stock data. Each generated stock data message is sent to the 
    Kafka topic specified by KAFKA_TOPIC. The function also implements a 
    delivery report callback to track the status of each message sent.
    
    The loop runs indefinitely, generating a new stock data record every 
    second until the process is terminated.
    """
    p = Producer({'bootstrap.servers': BROKER})

    while True:
        # Generate a random stock data record
        data = generate_stock_data()
        
        # Produce the message to the Kafka topic
        p.produce(KAFKA_TOPIC, key=data['symbol_name'], value=json.dumps(data), callback=delivery_report)
        
        # Wait for any outstanding messages to be delivered
        p.poll(0)
        
        # Sleep for 1 second before generating the next record
        time.sleep(1)

    # Ensure all messages are sent before exiting (although this code will never reach here)
    p.flush()

if __name__ == '__main__':
    main()

