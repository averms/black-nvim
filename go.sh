#!/bin/bash
set -euo pipefail

check() {
    nvim -u dev.vim mistune.py
}

build-doc() {
    ./md2vim -notoc -desc 'Format your code using Black' doc/black.md doc/black.txt
    printf '\nvim:ft=help:tw=80:ts=4:et:\n' >> doc/black.txt
    # I still need to edit manually: wrap at 80 chars, add tag to first line, reduce
    # list indent.
    nvim doc/black.txt
}


help() { h; }
h() {
    echo "$0 <task> [args]"
    echo "Tasks:"
    compgen -A function | cat -n
}

default() {
    check "$@"
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-default}
