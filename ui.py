import curses
import curses.panel
import curses.textpad


class UI:
    def __init__(self, screen):
        # Get screen dimensions
        y, x = screen.getmaxyx()
        self.screen = screen
        self.top_bar = _Bar(y, x, "YTS", "/ Search | o Options | q Quit")
        self.main_content = _MainContent(y, x)
        self.bottom_bar = _Bar(y, x, "Transmission", "", True)
        self.update()

    def refresh(self):
        # Get new screen dimensions
        y, x = self.screen.getmaxyx()
        # Clear the screen
        self.screen.erase()
        # Refresh TopBar
        self.top_bar.refresh(y, x)
        self.main_content.refresh(y, x)
        self.bottom_bar.refresh(y, x)
        # Update
        self.update()

    def move(self, step):
        if self.main_content.has_searched:
            self.main_content.selected = (self.main_content.selected + (step * -1)) % len(self.main_content.list)
            self.refresh()

    @staticmethod
    def update():
        curses.panel.update_panels()
        curses.doupdate()

    def get_current(self):
        return self.main_content.list[self.main_content.selected]


class _Bar:
    def __init__(self, y, x, left, right, bottom=False):
        self.left = left
        self.right = right
        self.bottom = bottom
        # Placement
        if bottom:
            line = y - 1
        else:
            line = 0
        # Build the bar
        self.window = curses.newwin(1, x, line, 0)
        self.window.bkgd(" ", curses.A_REVERSE)
        self.window.addstr(0, 0, self.left)
        self.window.addstr(0, x - len(self.right) - 1, self.right)
        self.panel = curses.panel.new_panel(self.window)

    def refresh(self, y, x):
        # Clear the TopBar window
        self.window.erase()
        # Placement
        if self.bottom:
            self.panel.move(y - 1, 0)
        # Add text again
        self.window.addstr(0, 0, self.left)
        self.window.addstr(0, x - len(self.right) - 1, self.right)


    def update_content(self, left, right):
        if left:
            self.left = left
        if right:
            self.right = right


class _MainContent:
    def __init__(self, y, x):
        # Select first item
        self.selected = 0
        self.has_searched = False
        self.list = {}
        # Build the content box
        self.window = curses.newwin(y - 2, x, 1, 0)
        self.window.addstr(int((y - 1) / 2), int((x / 2) - 8), "Press / to search")
        self.panel = curses.panel.new_panel(self.window)

    def refresh(self, y, x):
        # Clear the MainContent window
        self.window.erase()
        self.window.resize(y - 1, x)
        # Rebuild content
        if self.has_searched:
            self.print_list(y - 2, x)
        else:
            self.window.addstr(int((y - 1) / 2), int((x / 2) - 8), "Press / to search")

    def print_list(self, y, x):
        # Printing results
        for i, item in enumerate(self.list):
            # Constructing strings
            left = "{0} ({1})".format(item["MovieTitleClean"], item["MovieYear"])
            right = "Quality: {0}  Size: {1}  Rating: {2}".format(item["Quality"], item["Size"], item["MovieRating"])
            # Make white background for selected item
            if i == self.selected:
                self.window.attron(curses.A_REVERSE)
            # Print left side
            self.window.addstr(left)
            # Print space between sides
            for i in range(x - len(left) - len(right)):
                self.window.addch(" ")
            # Print right side
            self.window.addstr(right)
            # Turn off white background
            self.window.attroff(curses.A_REVERSE)


class Dialog:
    def __init__(self, y, x, begin_y, begin_x, title, close):
        self.window = curses.newwin(y, x, begin_y, begin_x)
        self.window.bkgd(curses.A_REVERSE)
        self.window.box()
        self.window.addstr(0, 1, "| {0} |".format(title))
        self.window.addstr(y - 1, (x - 1) - (len(close) + 4), "| {0} |".format(close))
        self.panel = curses.panel.new_panel(self.window)

class SearchDialog(Dialog):
    def __init__(self, screen):
        y, x = screen.getmaxyx()
        Dialog.__init__(self, 5, 40, int((y / 2) - 3), int((x / 2) - 20), "Search", "ENTER to search")
        self.search_box = self.window.derwin(1, 20, 2, 2)
        curses.panel.update_panels()
        curses.doupdate()
