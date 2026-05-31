import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

PLAYLISTS = {
    "SRC_KIDS": "Kids.m3u",
    "SRC_OTT": "OTT.m3u",
    "SRC_MIX": "Mix.m3u",
    "SRC_SPORTS": "Sports.m3u",
    "SRC_TVZONE": "TVZone.m3u",
    "SRC_ALLTV": "AllTV.m3u",
    "SRC_ISP": "ISP.m3u",
    "SRC_TOFFEE": "Toffee.m3u",
}

KEEP_PREFIXES = (
    "#EXTINF",
    "#EXTGRP",
    "#EXTVLCOPT",
    "#KODIPROP",
    "#EXT-X-",
)

def clean_playlist(content):
    content = content.replace("\r\n", "\n")

    lines = content.splitlines()

    if lines and lines[0].strip().upper() == "#EXTM3U":
        lines = lines[1:]

    cleaned = []

    for line in lines:
        line = line.rstrip()

        if not line:
            continue

        if line.startswith("#"):
            if line.startswith(KEEP_PREFIXES):
                cleaned.append(line)
            else:
                # Remove normal comments
                continue
        else:
            cleaned.append(line)

    return "\n".join(cleaned)


def make_header(channel_count):
    bd_time = datetime.now(ZoneInfo("Asia/Dhaka"))

    return f"""#=================================
# 🖥️ Developed by: Dibya Jyoti
# 🕒 Last Updated: {bd_time.strftime('%Y-%m-%d %H:%M:%S')} (BD Time)
# 📺 Channels Count: {channel_count}
# 🔒 Usage: Personal / Educational
#=================================
#EXTM3U

"""


for env_name, output_file in PLAYLISTS.items():
    url = os.getenv(env_name)

    if not url:
        print(f"[SKIP] Missing secret: {env_name}")
        continue

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        cleaned_content = clean_playlist(response.text)

        channel_count = cleaned_content.count("#EXTINF:")

        final_content = (
            make_header(channel_count)
            + cleaned_content
            + "\n"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"[OK] {output_file} updated ({channel_count} channels)")

    except Exception as e:
        print(f"[ERROR] {output_file}: {e}")
