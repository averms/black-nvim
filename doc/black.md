## Introduction

black-nvim formats your Python buffer asynchronously using [Black]. Its interface is
simple: it defines a function, `Black()`, that formats the entire buffer.

[black]: https://github.com/psf/black

## Usage

You can set `Black()` to a command, key mapping, or just call it directly.
I set it like this so that alt-shift-f formats the buffer
(in after/ftplugin/python.vim):

```vim
if has("mac")
    nnoremap <buffer> <silent> Ï :Black<cr>
    inoremap <buffer> <silent> Ï <c-o>:Black<cr>
elseif has("unix")
    nnoremap <buffer> <silent> <m-F> :Black<cr>
    inoremap <buffer> <silent> <m-F> <c-o>:Black<cr>
endif
```

## Configuration

Use `black#settings`. For example:

```vim
let g:black#settings = {
    \ 'fast': 1,
    \ 'line_length': 100
\}
```

- `fast` (default: 0)
  Set to a non-zero number to skip the AST check. This makes formatting a lot faster.
- `line_length` (default: 88)
  Set to an integer to tell black where to wrap lines.
