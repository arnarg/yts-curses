yts-curses
===

A simple curses program written in python 3 to search for and download movies from http://yts.re/

It's necessary to have Transmission and the python module transmissionrpc installed.

[YTS API](https://yts.re/api) was used.

Screenshot
---
![Usage](https://raw.github.com/arnarg/yts-curses/master/screenshots/yts.gif)

Settings
---
The settings are stored in settings.json.

**movie_dir:** Where you want your movies to go.

**tc_ip:** The ip address to your transmission daemon. If you are on the same computer as your transmission daemon, localhost will do.

**tc_port:** The port of your transmission daemon.

**quality:** In what quality your results will be. (720p, 1080p, 3D or empty for all)

**sort:** In what order your results should be displayed. (date, seeds, peers, size, alphabet, rating, downloaded, year)
