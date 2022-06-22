# © 2019-2020 Aman Verma <https://aman.raoverma.com/contact.html>
# Distributed under the MIT license, see LICENSE.md file for details.

import time
import sys
from typing import List, Dict, Union

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
class Blacken:
    def __init__(self, nvim: pynvim.api.Nvim):
        self.n = nvim

    @pynvim.function("Black")
    # args is not used but needs to be there to avoid an error.
    def black(self, args: List[str]) -> None:
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return

        start = time.perf_counter()
        options = self.get_opts()
        buf_str = "\n".join(self.n.current.buffer) + "\n"
        self.format_buff(buf_str, options, start)

    @pynvim.function("BlackSync", sync=True)
    def blacksync(self, args: List[str]) -> None:
        return self.black(args)

    def get_opts(self) -> Dict[str, Union[int, bool]]:
        options = {
            "fast": False,
            "line_length": 88,
            "is_pyi": self.n.current.buffer.name.endswith(".pyi"),
        }
        user_options = self.n.vars.get("black#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def format_buff(
        self, to_format: str, opts: Dict[str, Union[int, bool]], start: float
    ) -> None:
        mode = black.FileMode(line_length=opts["line_length"], is_pyi=opts["is_pyi"])
        try:
            new_buffer = black.format_file_contents(
                to_format, fast=bool(opts["fast"]), mode=mode
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

            self.n.out_write(f"Reformatted in {time.perf_counter() - start:.2f}s.\n")
