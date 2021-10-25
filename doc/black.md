## Introduction

black-nvim formats your Python buffer asynchronously using [Black]. Its interface is
simple: it defines a function, |Black()|, that formats the entire buffer.

[Black]: https://github.com/psf/black

## Usage

You can set \*Black()\* to a command, key mapping, or just call it directly.
For example, you can put the following commands in after/ftplugin/python.vim to
make CTRL-Q format the buffer:

```vim
nnoremap <buffer><silent> <c-q> <cmd>call Black()<cr>
inoremap <buffer><silent> <c-q> <cmd>call Black()<cr>
```

You can also use \*BlackSync()\* to format your buffer synchronously. This can
be used in the |BufWritePre| autocmd to format your buffer on save.

## Configuration

Use \*g:black#settings\*
For example:

```vim
let g:black#settings = {
    \ 'fast': 1,
    \ 'line_length': 100
\}
```

- `fast` (default: 0)
  Set to a non-zero number to skip the AST check. This makes formatting a lot faster.
- `line_length` (default: 88)
  Set to an integer to tell Black where to wrap lines.
