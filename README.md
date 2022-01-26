# black-nvim

A port of the [official black plugin] to Neovim's remote Python plugin interface.

Differences:

- It runs asynchronously, so it won't block scrolling while formatting the buffer.
- Checks if filetype is "python" before formatting.
- More robust error handling and better error messages.
- Missing some features (Upgrading the black package automatically, respecting
  pyproject.toml).
- Don't have to clone the entire source repo just to get the plugin.
- Zero lines of Vimscript.

[official black plugin]: https://github.com/ambv/black/tree/master/plugin/black.vim

## Installation

The 'master' branch is stable. You can see what is coming up by looking at 'devel' but
I wouldn't recommend using it.

| Plugin manager | How to install                                             |
|----------------|------------------------------------------------------------|
| minpac         | `call minpac#add('averms/black-nvim')`                     |
| dein.vim       | `call dein#add('averms/black-nvim')`                       |
| vim-plug       | `Plug 'averms/black-nvim', {'do': ':UpdateRemotePlugins'}` |

If you don't already have a system for managing python environments on your computer
I would recommend the following:

- Make sure you have at least version 3.6.
- Set up a virtual environment for use with neovim.
  ```sh
  mkdir -p ~/.local/venv && cd ~/.local/venv
  python3 -m venv nvim
  cd nvim
  . ./bin/activate
  pip install pynvim black
  ```
- Tell neovim about that environment like so:
  ```vim
  let g:python3_host_prog = $HOME . '/.local/venv/nvim/bin/python'
  ```
  If you're using vim-plug, this line needs to be before your `Plug` statement.
- Run `:checkhealth`. The python3 provider section should be not-red.

## Documentation

See [black.md](doc/black.md) or type `:h black.txt`.

## License

black-nvim is distributed under the MIT/Expat license.
See LICENSE file for details.
