# COMP3234 Programming Assignment

> A Simple Game House Application
>
> This is an individual submition


### Usage

* Start the server with `./src/GameServer.py <server_port> </path/to/userinfo.txt>`.

* Start the client with `./src/GameClinet.py <server_addr> <server_port>`.

* Please start the server before starting any clients.

* Please keep all the python files in the same directory to avoid import error.

* According to [Python Docs](https://docs.python.org/3/library/select.html),
  Module `select` **does not work on Windows**.
  Please conduct the testing on Linux or BSD.

* Any guess other than `true`, `t` or `1` (case insensitive) will be considered as `False`.

* The total number of game rooms is 6 by default, and can be changed by `Server.TOTAL_ROOMS` in `GameServer.py`.

