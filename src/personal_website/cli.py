import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from hugo.cli import HUGO_EXECUTABLE
from hugo.cli import __call as _hugo_cli_entrypoint

from .publications import generate_publications_data


def hugo_cli_entrypoint() -> None:
    generate_publications_data()
    _hugo_cli_entrypoint()


def preview() -> None:
    generate_publications_data()
    preview_cli = ["server", "--disableFastRender"]
    sys.argv = sys.argv[:1] + preview_cli + [arg for arg in sys.argv[1:] if arg not in preview_cli]
    _hugo_cli_entrypoint()


def preview_png() -> None:
    generate_publications_data()
    args = [arg for arg in sys.argv[1:] if arg != "--"]
    if len(args) != 1:
        print("Usage: uv run preview-png -- <page path>", file=sys.stderr)
        raise SystemExit(2)

    page_path = args[0].strip()
    normalized = "/" + page_path.strip("/")

    output_dir = Path(".artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = normalized.strip("/").replace("/", "-") or "home"
    screenshot_path = output_dir / f"preview-{slug}.png"

    server_cmd = [str(HUGO_EXECUTABLE), "server", "--disableFastRender", "-D", "--bind", "127.0.0.1", "--port", "1313"]
    server = subprocess.Popen(server_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        url = f"http://127.0.0.1:1313{normalized}"
        for _ in range(30):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.5)

        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1800})
            page.goto(url, wait_until="networkidle")
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)

    print(screenshot_path)


def hugo_build() -> None:
    generate_publications_data()
    result = subprocess.run([str(HUGO_EXECUTABLE), "--minify", *sys.argv[1:]])
    raise SystemExit(result.returncode)
