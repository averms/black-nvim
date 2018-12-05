if !has('nvim')
    echo 'This plugin requires neovim'
    finish
endif

if exists("g:load_black")
   finish
endif
let g:load_black = 1

if !exists("g:black_virtualenv")
  let g:black_virtualenv = g:python3_host_prog
endif
if !exists("g:black_fast")
  let g:black_fast = 0
endif
if !exists("g:black_linelength")
  let g:black_linelength = 88
endif
if !exists("g:black_skip_string_normalization")
  let g:black_skip_string_normalization = 0
endif

command! Black call Black()
