#!/bin/bash
set -euo pipefail

test_() {
    nvim -u dev.vim
}

build_doc() {
    ./md2vim -notoc -desc 'Format your code using Black' doc/black.md doc/black.txt
    printf 'vim:ft=help:tw=80:ts=4:et:' >> doc/black.txt
    nvim doc/black.txt
}


h() {
    echo "$0 <task> [args]"
    echo "Tasks:"
    compgen -A function | cat -n
}

default() {
    test_ "$@"
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-default}
