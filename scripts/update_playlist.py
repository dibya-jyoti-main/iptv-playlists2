import os
import requests

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

HEADER = """#EXTM3U
# Dibya TV
# IPTV Playlist 2
# Auto Updated Every 3 Hours

"""

for env_name, output_file in PLAYLISTS.items():
    url = os.getenv(env_name)

    if not url:
        print(f"Missing secret: {env_name}")
        continue

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    content = r.text

    if content.startswith("#EXTM3U"):
        lines = content.splitlines()
        content = "\n".join(lines[1:])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(HEADER + content)

    print(f"Updated {output_file}")
