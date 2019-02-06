# ------------------------------------------------------------------------------
# A port of the black.vim plugin to the remote python provider
# By Aman Verma
# ------------------------------------------------------------------------------
import time
import sys
from typing import List, Dict, Union

# doesn't work?
# import logging
import pynvim

try:
    import black
except ImportError:
    print(
        "[*] Black is not installed in your g:python3_host_prog, "
        "please install it with pip and try again",
        file=sys.stderr,
    )
    sys.exit(1)


@pynvim.plugin
class Main:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.n = nvim

    @pynvim.function("Black")
    def black(self, args: List[str]) -> None:
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return

        start = time.perf_counter()
        options = self._get_opts()
        buf_str = "\n".join(self.n.current.buffer) + "\n"
        self._format_buff(buf_str, options, start)

    def _get_opts(self) -> Dict[str, int]:
        options = {"fast": 0, "line_length": 88}
        user_options = self.n.vars.get("black#settings")
        if user_options:
            options.update(user_options)
        return options

    def _format_buff(self, to_format: str, opts: Dict[str, int], start: float) -> None:
        try:
            new_buffer_str = black.format_file_contents(to_format, **opts)
        except black.NothingChanged:
            self.n.out_write(
                "Already well formatted, good job "
                f"(took {time.perf_counter() - start:.4f}s).\n"
            )
        except black.InvalidInput:
            self.n.err_write(
                "Black could not parse the input. "
                "Make sure your code is syntactically correct before running.\n"
            )
        else:
            # update buffer, remembering the location of the cursor
            cursor = self.n.current.window.cursor
            self.n.current.buffer[:] = new_buffer_str.split("\n")[:-1]
            self.n.current.window.cursor = cursor
            self.n.out_write(f"Reformatted in {time.perf_counter() - start:.4f}s.\n")
