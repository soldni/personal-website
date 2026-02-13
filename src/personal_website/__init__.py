import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from hugo.cli import __call as hugo_cli_entrypoint

__all__ = ["hugo_cli_entrypoint", "preview", "preview_png"]


def preview():
    preview_cli = ["server", "--disableFastRender", "-D"]
    sys.argv = sys.argv[:1] + preview_cli + [k for k in sys.argv[1:] if k not in preview_cli]
    hugo_cli_entrypoint()


def preview_png():
    args = [a for a in sys.argv[1:] if a != "--"]
    if len(args) != 1:
        print("Usage: uv run preview-png -- <page path>", file=sys.stderr)
        raise SystemExit(2)

    page_path = args[0].strip()
    normalized = "/" + page_path.strip("/")

    output_dir = Path(".artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = normalized.strip("/").replace("/", "-") or "home"
    screenshot_path = output_dir / f"preview-{slug}.png"

    server_cmd = ["hugo", "server", "--disableFastRender", "-D", "--bind", "127.0.0.1", "--port", "1313"]
    server = subprocess.Popen(server_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        url = f"http://127.0.0.1:1313{normalized}"
        for _ in range(30):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.5)

        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            print("Warning: playwright install failed; attempting with existing browser", file=sys.stderr)

        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=[
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--single-process",
                ],
            )
            page = browser.new_page(viewport={"width": 1440, "height": 1800})
            page.goto(url, wait_until="networkidle")
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)

    print(screenshot_path)
