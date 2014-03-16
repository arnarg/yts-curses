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
    curses.raw()
    curses.nonl()

    screen.keypad(1)

    global ui
    ui = UI(screen)
    make_connection()

    main_loop(screen)


def main_loop(screen):

    while True:
        key = screen.getch()
        if key == 113:  # q key
            break
        elif key == 47:  # / key
            did_search, user_input = search_loop(SearchDialog(screen))
            if did_search:
                search(ui, user_input, "", settings["quality"], settings["sort"])
            else:
                ui.refresh()
        elif key == curses.KEY_RESIZE:  # Terminal was resized
            ui.refresh()
        elif key == curses.KEY_UP:  # Up key
            ui.move(1)
        elif key == curses.KEY_DOWN:  # Down key
            ui.move(-1)
        elif key == 13:  # Enter key
            if ui.main_content.has_searched:
                try:
                    result = add_movie(tc, ui.get_current(), settings["movie_dir"])
                except NameError:
                    result = "Can't connect to Transmission"
                ui.bottom_bar.update_content("", result)
                ui.refresh()
        elif key == 114:  # r key
            make_connection()
        elif key == curses.KEY_RIGHT:
            if ui.main_content.has_searched:
                details = get_details(int(ui.get_current()["MovieID"]))
                details_loop(screen, DetailsDialog(screen, details))
            ui.refresh()


def search_loop(dialog):
    curses.curs_set(1)
    user_input = ""
    while True:
        key = dialog.input_field.getch()
        if key == 27:  # ESC key
            curses.curs_set(0)
            del dialog
            return False, user_input
        elif key == 13:  # Enter key
            curses.curs_set(0)
            del dialog
            return True, user_input
        elif key == 127:  # Backspace key
            user_input = user_input[:-1]
            dialog.redraw_input(user_input)
        elif 64 < key < 91 or 96 < key < 124 or 47 < key < 58 or key == 32:
            # If a character or space was pressed, add it to the input
            user_input += chr(key)
            dialog.input_field.addch(key)


def details_loop(screen, dialog):
    while True:
        key = screen.getch()
        if key == 27:  # ESC key
            del dialog
            break
        elif key == 113:  # q key
            exit()

if __name__ == "__main__":
    curses.wrapper(main)