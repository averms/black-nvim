black-nvim
==========

A port of the [official black plugin][1] to use neovim's remote provider interface.

Differences:
- It runs asynchronously, so it won't block neovim while formatting the buffer.
- Checks if filetype is "python" before formatting.
- This doesn't have all the features of the official one yet
  (you can't upgrade black from within neovim).
- Only command implemented right now is `Black`.

`mistune.py` is used as a test file.

[1]: https://github.com/ambv/black/tree/master/plugin/black.vim
