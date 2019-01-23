black-nvim
==========
A port of the [official black plugin][1] to use neovim's remote provider interface.

Differences:
- It runs asynchronously, so it won't block scrolling while formatting the buffer.
- Checks if filetype is "python" before formatting.
- More robust error handling and better error messages.
- Only vital features (Upgrading the black package is left to the user).
- Choose your own commands, only a function is exported.

`mistune.py` is used as a test file.

[1]: https://github.com/ambv/black/tree/master/plugin/black.vim

Installation
------------
| Plugin manager | How to install                                             |
|----------------|------------------------------------------------------------|
| minpac         | `call minpac#add('a-vrma/black-nvim')`                     |
| dein.vim       | `call dein#add('a-vrma/black-nvim')`                       |
| vim-plug       | `Plug 'a-vrma/black-nvim', {'do': ':UpdateRemotePlugins'}` |

Options
-------
- `g:black_fast`
  Set to `1` to skip the AST check.
- `g:black_skip_string_normalization`
  Set to `1` to skip normalizing all strings to double quotes.
- `g:black_linelength`
  Set to an integer to tell black where to wrap around.

Setup
-----
You can set `Black()` to a command, keymapping, or just call it directly.
I set it like this so that alt-shift-f formats the buffer
(in after/ftplugin/python.vim):

```vim
if has('mac')
    nnoremap <buffer> Ï :call Black()<cr>
elseif has('unix')
    nnoremap <buffer> <m-F> :call Black()<cr>
endif
```

License
-------
black-nvim is distributed under the MIT/Expat license.
See LICENSE file for details.
