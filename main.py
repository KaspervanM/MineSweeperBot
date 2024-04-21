# This is a Python script that will be used to run the main program
from environment import Environment
from screen_interaction import ScreenInterface
import numpy as np
from time import sleep
from pynput import keyboard
import threading

should_exit = False

def on_press(key):
    global should_exit
    try:
        if key == keyboard.Key.space:
            should_exit = not should_exit
    except AttributeError:
        pass


# Function to start the listener in a separate thread
def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def random_coordinate(coordinates):
    return coordinates[np.random.choice(len(coordinates))]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    field_width = 30
    field_height = 16
    num_mines = 99

    # Start the listener in a separate thread
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True  # Daemonize the thread to exit with the main program
    listener_thread.start()

    print("Press SPACE to exit the program.")

    screen_interface = ScreenInterface(field_width, field_height)
    print(
        f"Top-left: {(screen_interface.x1, screen_interface.y1)}, Bottom-right: {(screen_interface.x2, screen_interface.y2)}")

    while True:
        env = Environment(field_width, field_height, num_mines)
        while not should_exit:
            knowns = screen_interface.get_field_knowns()
            print(knowns)
            print()

            env.update_field(knowns)
            print(env)

            best_choices, probability = env.get_best_choices()
            if probability > 0.:
                best_choices = np.array([random_coordinate(best_choices)])
            print(best_choices)

            for x, y in best_choices:
                screen_interface.click_cell(x, y)
                sleep(0.05)
            sleep(0.5)
        sleep(1)
