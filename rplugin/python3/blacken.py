# ------------------------------------------------------------------------------
# A port of the black.vim plugin to the remote python provider
# By Aman Verma
# ------------------------------------------------------------------------------
import time
import sys
import logging

import pynvim
try:
    import black
except ImportError:
    print(
        "Black is not installed in your g:python3_host_prog, please install it with pip and try again",
        file=sys.stderr,
    )
    sys.exit(1)


@pynvim.plugin
class Main:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("Black")
    def black(self, args):
        start = time.time()
        black_opts = {
            "fast": self.get_var("g:black_fast"),
            "line_length": self.get_var("g:black_linelength"),
            "mode": black.FileMode.AUTO_DETECT,
        }
        if self.get_var("g:black_skip_string_normalization"):
            black_opts["mode"] |= black.FileMode.NO_STRING_NORMALIZATION

        buf_str = "\n".join(self.nvim.current.buffer) + "\n"

        self.format(buf_str, black_opts, start)


    def format(self, to_format, opts, start):
        try:
            new_buffer_str = black.format_file_contents(to_format, **opts)
        except black.NothingChanged:
            self.nvim.out_write(f"Already well formatted, good job. (took {time.time() - start:.4f}s)\n")
        else:
            cursor = self.nvim.current.window.cursor
            self.nvim.current.buffer[:] = new_buffer_str.split("\n")[:-1]
            self.nvim.current.window.cursor = cursor
            self.nvim.out_write(f"Reformatted in {time.time() - start:.4f}s.\n")


    def get_var(self, vimscript_exp):
        # try:
            return self.nvim.eval(vimscript_exp)
        # except pynvim.api.nvim.NvimError:
        #     return 0
