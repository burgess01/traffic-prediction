from kafka import KafkaConsumer, KafkaProducer
import pickle
import io
import scipy.io
import time

topic = 'proj_topic'

# Initialize the Kafka producer
# - 'bootstrap_servers' defines Kafka server(s)
# - 'value_serializer' converts data to JSON and encodes it to bytes
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: x)

# Initialize the Kafka consumer
# - topic is the topic to subscribe to
# - 'bootstrap_servers' defines the Kafka server(s) to connect to
# - 'auto_offset_reset' controls where to start reading (earliest or latest)
# - 'enable_auto_commit' automatically commits the offset after consuming
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start reading from the beginning of the topic if no offset is stored
    enable_auto_commit=True,  # Automatically commit the message offset after it's read
    value_deserializer=lambda x: pickle.loads(x), # Deserialize JSON messages
)

# Function to send messages to the Kafka topic
def send_message():
    load_and_prepare_data("traffic_dataset.mat")

    with open("tra_X_tr.pkl", "rb") as file:
        pklXData = file.read()
    with open("tra_Y_tr.pkl", "rb") as file:
        pklYData = file.read()

    producer.send(topic, pklXData) # Send the message to the topic
    producer.flush()
    time.sleep(1)
    producer.send(topic, pklYData)
    producer.flush()
    print(f"Sent pickle files.")

def load_and_prepare_data(mat_file_path):
    # Load the .mat file
    mat = scipy.io.loadmat(mat_file_path)
    # Extract training and testing data
    tra_X_tr = mat['tra_X_tr']
    tra_Y_tr = mat['tra_Y_tr']
    tra_X_te = mat['tra_X_te']
    tra_Y_te = mat['tra_Y_te']
    tra_adj_mat = mat['tra_adj_mat']
    # Save the data using pickle for later use
    with open('tra_X_tr.pkl', 'wb') as f:
        pickle.dump(tra_X_tr, f)
    with open('tra_Y_tr.pkl', 'wb') as f:
        pickle.dump(tra_Y_tr, f)
    print("Data preparation complete. Data saved as pickle files.")

# Function to consume messages from the topic
def consume_message():
    print("Starting consumer...")
    # Infinite loop to read and print messages from the topic
    for message in consumer:
        print(message.value)
        print("got data")

if __name__ == '__main__':
    send_message()
    # Flush ensures all buffered messages are sent to Kafka before continuing
    producer.flush()
    # Close the producer to free resources, ensures flush is called
    producer.close()

    data = consume_message()  # Start consuming messages