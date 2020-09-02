import os
import time

from classes.KafkaPC import KafkaPC

print("start 1p_count_up")

env_vars = {
    "config_path": os.getenv("config_path"),
    "config_section": os.getenv("config_section"),
}

new_p = KafkaPC(**env_vars)

for i in range(10):

    message = {"count": i}
    new_p.send_msg(message)
    print(f"Sent message {i} with count={i}")
    time.sleep(1)
