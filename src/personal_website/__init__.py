import sys

from hugo.cli import __call as hugo_cli_entrypoint

__all__ = ["hugo_cli_entrypoint"]


def preview():
    preview_cli = ["server", "--disableFastRender"]
    sys.argv = sys.argv[:1] + preview_cli + [k for k in sys.argv[1:] if k not in preview_cli]
    hugo_cli_entrypoint()
