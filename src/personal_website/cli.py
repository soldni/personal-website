import argparse
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
    parser = argparse.ArgumentParser(prog="preview-png")
    parser.add_argument("paths", nargs="+", help="Page paths to capture, e.g. /publications/")
    parser.add_argument("--scheme", choices=["light", "dark"], default="light", help="Preferred color scheme")
    parser.add_argument("--label", help="Optional label to include in screenshot filenames")
    parser.add_argument("--output-dir", default=".artifacts", help="Directory for generated screenshots")
    parser.add_argument("--width", type=int, default=1440, help="Viewport width in pixels")
    parser.add_argument("--height", type=int, default=1800, help="Viewport height in pixels")
    args = parser.parse_args([arg for arg in sys.argv[1:] if arg != "--"])

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    server_cmd = [str(HUGO_EXECUTABLE), "server", "--disableFastRender", "-D", "--bind", "127.0.0.1", "--port", "1313"]
    server = subprocess.Popen(server_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    screenshot_paths = []

    try:
        base_url = "http://127.0.0.1:1313"
        home_url = f"{base_url}/"
        for _ in range(30):
            try:
                urllib.request.urlopen(home_url, timeout=1)
                break
            except Exception:
                time.sleep(0.5)

        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": args.width, "height": args.height})
            page.emulate_media(color_scheme=args.scheme)
            screenshot_paths = []
            for page_path in args.paths:
                normalized = "/" + page_path.strip().strip("/")
                slug = normalized.strip("/").replace("/", "-") or "home"
                label = f"{args.label}-" if args.label else ""
                screenshot_path = output_dir / f"preview-{label}{slug}-{args.scheme}.png"
                page.goto(f"{base_url}{normalized}", wait_until="networkidle")
                page.screenshot(path=str(screenshot_path), full_page=True)
                screenshot_paths.append(screenshot_path)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)

    for screenshot_path in screenshot_paths:
        print(screenshot_path)


def hugo_build() -> None:
    generate_publications_data()
    result = subprocess.run([str(HUGO_EXECUTABLE), "--minify", *sys.argv[1:]])
    raise SystemExit(result.returncode)
