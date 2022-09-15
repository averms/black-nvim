# © 2019-2020 Aman Verma <https://aman.raoverma.com/contact.html>
# Distributed under the MIT license, see LICENSE.md file for details.

import time
import sys
from typing import List, Dict, Union, Set

import pynvim

try:
    import black
    from black import TargetVersion
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
    def black_(self, args: List[str]) -> None:
        if self.n.current.buffer.options.get("filetype") != "python":
            self.n.err_write("Not in a python file.\n")
            return

        start = time.perf_counter()
        options = self.get_opts()
        buf_str = "\n".join(self.n.current.buffer) + "\n"
        self.format_buff(buf_str, options, start)

    @pynvim.function("BlackSync", sync=True)
    def blacksync(self, args: List[str]) -> None:
        return self.black_(args)

    def get_opts(self) -> Dict[str, Union[int, bool, str]]:
        options = {
            "fast": False,
            "line_length": 88,
            "is_pyi": self.n.current.buffer.name.endswith(".pyi"),
            "target_version": "",
        }
        user_options = self.n.vars.get("black#settings")
        if user_options is not None:
            options.update(user_options)
        return options

    def parse_target_version(self, target_version: str) -> Set[black.TargetVersion]:
        self.n.err_write(repr(black))
        if target_version.lower() == "":
            return set()
        elif target_version.lower() == "py33":
            return {black.TargetVersion.PY33}
        elif target_version.lower() == "py34":
            return {black.TargetVersion.PY34}
        elif target_version.lower() == "py35":
            return {black.TargetVersion.PY35}
        elif target_version.lower() == "py36":
            return {black.TargetVersion.PY36}
        elif target_version.lower() == "py37":
            return {black.TargetVersion.PY37}
        elif target_version.lower() == "py38":
            return {black.TargetVersion.PY38}
        elif target_version.lower() == "py39":
            return {black.TargetVersion.PY39}
        elif target_version.lower() == "py310":
            return {black.TargetVersion.PY310}
        elif target_version.lower() == "py311":
            return {black.TargetVersion.PY311}
        else:
            self.n.err_write(
                f"{target_version!r} is an invalid target_version. "
                "Use 'py38' for python 3.8 for example.\n"
            )
            return set()

    def format_buff(
        self,
        to_format: str,
        opts: Dict[str, Union[int, bool, str]],
        start: float,
    ) -> None:
        mode = black.FileMode(
            line_length=opts["line_length"],
            is_pyi=opts["is_pyi"],
            target_versions=self.parse_target_version(opts["target_version"]),
        )
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
