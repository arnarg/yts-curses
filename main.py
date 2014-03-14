import curses
import json
import transmissionrpc
import transmissionrpc.error
from ui import *
from functions import *

# Get settings
with open('settings.json', 'r') as f:
    settings = json.load(f)


def make_connection():
    # Connect to transmission
    try:
        global tc
        tc = transmissionrpc.Client(settings["tc_ip"], settings["tc_port"])
        tc_string = "Transmission {0}.{1} - {2}:{3}".format(tc.server_version[0],
                                                            tc.server_version[1],
                                                            settings["tc_ip"],
                                                            settings["tc_port"])
    except transmissionrpc.error.TransmissionError as error:
        tc_string = "Transmission: {0} Press r to refresh.".format(error.message)

    ui.bottom_bar.update_content(tc_string, "")
    ui.refresh()


def main(screen):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

    screen.keypad(1)

    global ui
    ui = UI(screen)
    make_connection()

    main_loop(screen)


def main_loop(screen):

    while True:
        key = screen.getch()
        if key == 113: # q key
            break
        elif key == 111: # o key
            dialog_loop(screen, SearchDialog(screen))
        elif key == 47: # / key
            search(ui, "", "", "1080p", "")
        elif key == curses.KEY_RESIZE: # Terminal was resized
            ui.refresh()
        elif key == curses.KEY_UP: # Up key
            ui.move(1)
        elif key == curses.KEY_DOWN: # Down key
            ui.move(-1)
        elif key == 100: # d key
            if ui.main_content.has_searched:
                try:
                    result = add_movie(tc, ui.get_current(), settings["movie_dir"])
                except NameError:
                    result = "Can't connect to Transmission"
                ui.bottom_bar.update_content("", result)
                ui.refresh()
        elif key == 114: # r key
            make_connection()
        #elif key == curses.KEY_RIGHT:




if __name__ == "__main__":
    curses.wrapper(main)