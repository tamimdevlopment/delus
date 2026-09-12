from .c.delus_main_file_py_to_c import Mylang as C
from .asm.delus_main_file_py_to_asm import mylang as ASM
from .docker.delus_main_file_py_to_docker import Docker as Docker
from .html.delus_main_file_py_to_html import Html as HTML


__all__ = ["C", "ASM", "Docker", "HTML"]
