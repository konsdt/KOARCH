import os

from Big_Data_Platform.Kubernetes.Kafka_Client.Confluent_Kafka_Python.src.classes.CKafkaPC import KafkaPC


env_vars = {
    "config_path": os.getenv("config_path"),
    "config_section": os.getenv("config_section"),
}


new_pc = KafkaPC(**env_vars)

try:
    while True:
        msg = new_pc.consumer.poll(0.1)

        if msg is None:
            continue

        elif msg.error() is not None:
            print(f"Error occured: {str(msg.error())}")

        else:
            """
            "name": "Data",
            "fields": [
                {"name": "phase", "type": ["string"]},
                {"name": "id_x", "type": ["int"]},
                {"name": "x", "type": ["float"]},
                {"name": "y", "type": ["float"]}
                ]
            """
            print("Trying to decode new message")
            new_data = new_pc.decode_msg(msg)
            topic = msg.topic()

            print(f"Message on Topic {topic}:")
            print(new_data)
            """
            "name": "Data",
            "fields": [
                {"name": "phase", "type": ["string"]},
                {"name": "id_x", "type": ["int"]},
                {"name": "x", "type": ["float"]},
                {"name": "y", "type": ["float"]}
                ]
            """

            new_data_point = {
                "phase": "observation",
                "id": new_data["cycle"],
                "x": new_data["x"]["conveyorRuntime"],
                "y": new_data["y_agg_norm"],
            }
            print("Sending new message:")
            print(new_data_point)

            new_pc.send_msg(new_data_point)

except KeyboardInterrupt:
    pass

except Exception as e:
    print(f"Exception: {repr(e)}")

finally:
    new_pc.consumer.close()
