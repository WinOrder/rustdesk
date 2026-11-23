import pathlib
import re
import shutil
import sys

from PIL import Image

APP_NAME = sys.argv[1]
root = pathlib.Path(__file__).resolve().parents[2]
src = Image.open(root / "res/winorder/icon-1024.png").convert("RGBA")


def png(path, size):
    src.resize((size, size), Image.LANCZOS).save(root / path)


def ico(path):
    src.save(root / path, sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])


png("res/icon.png", 512)
png("res/32x32.png", 32)
png("res/64x64.png", 64)
png("res/128x128.png", 128)
png("res/128x128@2x.png", 256)
ico("res/icon.ico")
ico("res/tray-icon.ico")
ico("flutter/windows/runner/resources/app_icon.ico")
shutil.copy(root / "res/winorder/icon.svg", root / "flutter/assets/icon.svg")


def replace_once(path, pattern, repl):
    p = root / path
    text = p.read_text(encoding="utf-8")
    new, n = re.subn(pattern, lambda _: repl, text, count=1)
    if n != 1:
        sys.exit(f"pattern not found in {path}: {pattern}")
    p.write_text(new, encoding="utf-8")


replace_once(
    "libs/hbb_common/src/config.rs",
    r'APP_NAME: RwLock<String> = RwLock::new\("RustDesk"\.to_owned\(\)\)',
    f'APP_NAME: RwLock<String> = RwLock::new("{APP_NAME}".to_owned())',
)
replace_once(
    "flutter/windows/runner/Runner.rc",
    r'VALUE "FileDescription", "RustDesk Remote Desktop"',
    f'VALUE "FileDescription", "{APP_NAME}"',
)
replace_once(
    "flutter/windows/runner/Runner.rc",
    r'VALUE "ProductName", "RustDesk"',
    f'VALUE "ProductName", "{APP_NAME}"',
)
