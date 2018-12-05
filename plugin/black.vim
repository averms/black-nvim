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

command! Black call Black()
