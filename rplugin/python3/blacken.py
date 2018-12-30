# ------------------------------------------------------------------------------
# A port of the black.vim plugin to the remote python provider
# By Aman Verma
# ------------------------------------------------------------------------------
import time
import sys

# doesn't work?
# import logging

import pynvim

try:
    import black
except ImportError:
    print(
        "[**] Black is not installed in your g:python3_host_prog, please install it with pip and try again",
        file=sys.stderr,
    )
    sys.exit(1)


@pynvim.plugin
class Main:
    def __init__(self, nvim):
        self.vi = nvim

    @pynvim.function("Black")
    def black(self, args):
        if self.vi.current.buffer.options.get("filetype") != "python":
            self.vi.out_write("Not in a python file.\n")
            return

        start = time.time()
        black_opts = {
            "fast": bool(self.vi.vars.get("black_fast", False)),
            "line_length": self.vi.vars.get("black_linelength", 88),
            "mode": black.FileMode.AUTO_DETECT,
        }
        if self.vi.vars.get("black_skip_string_normalization"):
            black_opts["mode"] |= black.FileMode.NO_STRING_NORMALIZATION

        buf_str = "\n".join(self.vi.current.buffer) + "\n"
        self.format_buff(buf_str, black_opts, start)

    def format_buff(self, to_format, opts, start):
        try:
            new_buffer_str = black.format_file_contents(to_format, **opts)
        except black.NothingChanged:
            self.vi.out_write(
                f"Already well formatted, good job (took {time.time() - start:.4f}s).\n"
            )
        except black.InvalidInput:
            self.vi.err_write(
                "Black could not parse the input. "
                "Make sure your code is syntactically correct before running.\n"
            )
        else:
            cursor = self.vi.current.window.cursor
            self.vi.current.buffer[:] = new_buffer_str.split("\n")[:-1]
            self.vi.current.window.cursor = cursor
            self.vi.out_write(f"Reformatted in {time.time() - start:.4f}s.\n")
