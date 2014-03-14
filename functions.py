import requests
import curses


def search(ui, keyword, genre, quality, sort):
    # Get window dimensions
    y, x = ui.main_content.window.getmaxyx()
    # Clear window
    ui.main_content.window.erase()
    # Get movie list
    ui.main_content.list = get_search(keyword, genre, quality, sort, y - 1)
    ui.main_content.has_searched = True
    ui.main_content.selected = 0
    ui.top_bar.update_content("", "d Download | left Details | / Search | o Options | q Quit")
    ui.refresh()


def get_search(keyword, genre, quality, sort, limit):
    url = "http://yts.re/api/list.json?keywords={0}".format(keyword)
    if genre:
        url += "&genre={0}".format(genre)
    if quality:
        url += "&quality={0}".format(quality)
    if sort:
        url += "&sort={0}".format(sort)
    if limit:
        url += "&limit={0}".format(limit)

    return requests.get(url).json()["MovieList"]


def add_movie(tc, movie, movie_dir):
    tc.add_torrent(movie["TorrentMagnetUrl"], None, download_dir=movie_dir)
    return "{0} has been added".format(movie["MovieTitleClean"])