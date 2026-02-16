import json
import sys
import tty
import termios
import uuid
from google.cloud import pubsub_v1

# Google Cloud Project Configuration
PROJECT_ID = "sunny-studio-484813-q7"
COMMAND_TOPIC = "game-commands"

# Key mappings
KEY_TO_DIRECTION = {
    "w": "UP",
    "a": "LEFT",
    "s": "DOWN",
    "d": "RIGHT"
}

# Direction opposites - cannot move in opposite direction
OPPOSITES = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}


def getch():
    """Read a single character from stdin without waiting for Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def is_valid_move(direction, last_direction):
    """Check if the move is valid (not opposite of last move)."""
    if last_direction is None:
        return True
    return direction != OPPOSITES.get(last_direction)


def create_join_message(player_id, player_name):
    """Creates a join_game message."""
    return {
        "type": "join_game",
        "name": player_name,
        "player_id": player_id
    }


def create_move_message(player_id, direction):
    """Creates a move message."""
    return {
        "type": "move",
        "player_id": player_id,
        "direction": direction
    }


def publish_message(publisher, topic_path, message):
    """Publishes a message to Pub/Sub."""
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published: {message}")
    return future.result()


def main():
    # Ask for player name
    player_name = input("Enter your player name: ").strip()
    if not player_name:
        player_name = "Player"
    
    # Generate unique player ID
    player_id = str(uuid.uuid4())
    
    # Initialize publisher
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, COMMAND_TOPIC)
    
    print(f"Starting game generator for player: {player_name}")
    print(f"Player ID: {player_id}")
    print(f"Publishing to topic: {topic_path}")
    print("-" * 50)
    print("Controls: W=UP, A=LEFT, S=DOWN, D=RIGHT, Q=QUIT")
    print("-" * 50)
    
    # Send join message
    join_msg = create_join_message(player_id, player_name)
    publish_message(publisher, topic_path, join_msg)
    
    # Track last direction
    last_direction = None
    
    try:
        while True:
            key = getch().lower()
            
            # Quit on 'q' or Ctrl+C
            if key == 'q' or key == '\x03':
                break
            
            # Check if key is a valid direction key
            if key not in KEY_TO_DIRECTION:
                continue
            
            direction = KEY_TO_DIRECTION[key]
            
            # Check if move is valid (not opposite of last)
            if not is_valid_move(direction, last_direction):
                print(f"Invalid move: cannot go {direction} after {last_direction}")
                continue
            
            last_direction = direction
            
            # Create and send move message
            move_msg = create_move_message(player_id, direction)
            publish_message(publisher, topic_path, move_msg)
            
    except KeyboardInterrupt:
        pass
    
    print("\nStopping generator...")


if __name__ == "__main__":
    main()
