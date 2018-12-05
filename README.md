black-nvim
==========

A port of the [official black plugin][1] to use neovim's remote provider interface.
It runs asynchronously, so it won't block neovim while formatting the buffer.
This doesn't have all the features of the official one yet
(you can't upgrade black from within neovim).

`mistune.py` is used as a test file.

[1]: https://github.com/ambv/black/tree/master/plugin/
