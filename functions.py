import requests


def search(ui, keyword, genre, quality, sort):
    # Get window dimensions
    y, x = ui.main_content.window.getmaxyx()
    # Clear window
    ui.main_content.window.erase()
    # Get movie list
    ui.main_content.list = get_search(keyword, genre, quality, sort, y - 1)
    ui.main_content.has_searched = True
    ui.main_content.selected = 0
    ui.main_content.message = "Nothing was found"
    if ui.main_content.list is not -1:
        ui.top_bar.update_content("", "left Details | / Search | q Quit")
    else:
        ui.top_bar.update_content("", "/ Search | q Quit")
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

    try:
        return requests.get(url).json()["MovieList"]
    except KeyError:
        return -1


def add_movie(tc, movie, movie_dir):
    tc.add_torrent(movie["TorrentMagnetUrl"], None, download_dir=movie_dir)
    return "{0} has been added".format(movie["MovieTitleClean"])


def get_details(movie_id):
    return requests.get("https://yts.re/api/movie.json?id={0}".format(movie_id)).json()