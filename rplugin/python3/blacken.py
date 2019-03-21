# ------------------------------------------------------------------------------
# A port of the black.vim plugin to the remote python provider
# By Aman Verma
# ------------------------------------------------------------------------------
import time
import sys
from typing import List, Dict, Union

# import logging (doesn't work?)
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
        # args is not used but needs to be their to avoid an error.
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return

        start = time.perf_counter()
        options = self._get_opts()
        buf_str = "\n".join(self.n.current.buffer) + "\n"
        self._format_buff(buf_str, options, start)

    def _get_opts(self) -> Dict[str, Union[int, bool]]:
        options = {
            "fast": False,
            "line_length": 88,
            "is_pyi": self.n.current.buffer.name.endswith(".pyi"),
        }
        user_options = self.n.vars.get("black#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def _format_buff(
        self, to_format: str, opts: Dict[str, Union[int, bool]], start: float
    ) -> None:
        mode = black.FileMode(line_length=opts["line_length"], is_pyi=opts["is_pyi"])
        try:
            new_buffer = black.format_file_contents(
                to_format, fast=opts["fast"], mode=mode
            )
        except black.NothingChanged:
            self.n.out_write("Already well formatted, good job.\n")
        except black.InvalidInput:
            self.n.err_write(
                "Black could not parse the input. "
                "Make sure your code is syntactically correct before running.\n"
            )
        else:
            # update buffer, remembering the location of the cursor
            cursor = self.n.current.window.cursor

            self.n.current.buffer[:] = new_buffer.split("\n")[:-1]
            try:
                self.n.current.window.cursor = cursor
            except pynvim.api.NvimError:
                # if cursor is outside buffer, set it to last line.
                self.n.current.window.cursor = (len(self.n.current.buffer), 0)

            self.n.out_write(f"Reformatted in {time.perf_counter() - start:.4f}s.\n")
