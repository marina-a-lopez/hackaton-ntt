import json
import time
import random
import uuid
from google.cloud import pubsub_v1

# Google Cloud Project Configuration
PROJECT_ID = "sunny-studio-484813-q7"
COMMAND_TOPIC = "game-commands"

# Player configuration
PLAYER_ID = "PAU_AISHA"
PLAYER_NAME = "PAU_AISHA"

# Direction opposites - cannot move in opposite direction
OPPOSITES = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


def get_valid_directions(last_direction):
    """Returns valid directions based on the last move."""
    if last_direction is None:
        return DIRECTIONS
    
    opposite = OPPOSITES.get(last_direction)
    return [d for d in DIRECTIONS if d != opposite]


def create_join_message():
    """Creates a join_game message."""
    return {
        "type": "join_game",
        "name": PLAYER_NAME,
        "player_id": PLAYER_ID
    }


def create_move_message(direction):
    """Creates a move message."""
    return {
        "type": "move",
        "player_id": PLAYER_ID,
        "direction": direction
    }


def publish_message(publisher, topic_path, message):
    """Publishes a message to Pub/Sub."""
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published: {message}")
    return future.result()


def main():
    # Initialize publisher
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, COMMAND_TOPIC)
    
    print(f"Starting game generator for player: {PLAYER_NAME}")
    print(f"Player ID: {PLAYER_ID}")
    print(f"Publishing to topic: {topic_path}")
    print("-" * 50)
    
    # Send join message
    join_msg = create_join_message()
    publish_message(publisher, topic_path, join_msg)
    
    # Track last direction
    last_direction = None
    
    try:
        while True:
            time.sleep(3)
            
            # Get valid directions based on last move
            valid_directions = get_valid_directions(last_direction)
            
            # Pick a random valid direction
            direction = random.choice(valid_directions)
            last_direction = direction
            
            # Create and send move message
            move_msg = create_move_message(direction)
            publish_message(publisher, topic_path, move_msg)
            
    except KeyboardInterrupt:
        print("\nStopping generator...")


if __name__ == "__main__":
    main()
import json
import time
import random
import uuid
from google.cloud import pubsub_v1

# Google Cloud Project Configuration
PROJECT_ID = "sunny-studio-484813-q7"
COMMAND_TOPIC = "game-commands"

# Player configuration
PLAYER_ID = str(uuid.uuid4())
PLAYER_NAME = "Player_" + PLAYER_ID[:8]

# Direction opposites - cannot move in opposite direction
OPPOSITES = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


def get_valid_directions(last_direction):
    """Returns valid directions based on the last move."""
    if last_direction is None:
        return DIRECTIONS
    
    opposite = OPPOSITES.get(last_direction)
    return [d for d in DIRECTIONS if d != opposite]


def create_join_message():
    """Creates a join_game message."""
    return {
        "type": "join_game",
        "name": PLAYER_NAME,
        "player_id": PLAYER_ID
    }


def create_move_message(direction):
    """Creates a move message."""
    return {
        "type": "move",
        "player_id": PLAYER_ID,
        "direction": direction
    }


def publish_message(publisher, topic_path, message):
    """Publishes a message to Pub/Sub."""
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published: {message}")
    return future.result()


def main():
    # Initialize publisher
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, COMMAND_TOPIC)
    
    print(f"Starting game generator for player: {PLAYER_NAME}")
    print(f"Player ID: {PLAYER_ID}")
    print(f"Publishing to topic: {topic_path}")
    print("-" * 50)
    
    # Send join message
    join_msg = create_join_message()
    publish_message(publisher, topic_path, join_msg)
    
    # Track last direction
    last_direction = None
    
    try:
        while True:
            time.sleep(3)
            
            # Get valid directions based on last move
            valid_directions = get_valid_directions(last_direction)
            
            # Pick a random valid direction
            direction = random.choice(valid_directions)
            last_direction = direction
            
            # Create and send move message
            move_msg = create_move_message(direction)
            publish_message(publisher, topic_path, move_msg)
            
    except KeyboardInterrupt:
        print("\nStopping generator...")


if __name__ == "__main__":
    main()
