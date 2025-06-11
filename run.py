import os
import json
import emoji
import subprocess

SVG_DIR = "assets/svg/"
PNG_DIR = "assets/png/"
OUTPUT_JSON = "index.json"
PNG_SIZE = 13

os.makedirs(PNG_DIR, exist_ok=True)

emoji_map = {}
emoji_map["names"] = {}

for filename in os.listdir(SOURCE_DIR):
    if not filename.endswith(".png"):
        continue

    codepoint = filename[:-4].lower()  # remove .png extension
    source_path = os.path.join(SOURCE_DIR, filename)
    png_path = os.path.join(PNG_DIR, f"{codepoint}.png")

    try:
        char = chr(int(codepoint, 16))
        name = emoji.demojize(char)
        name = name[1:-1].lower()
        name = name.replace("’", "")

        if not name:
            continue

        # remove opacity and scale to 13x13
        subprocess.run([
            "magick",
            "convert",
            f"{source_path}",
            "-resize", f"{PNG_SIZE}x{PNG_SIZE}",
            "-filter", "Box",
            "-colors", "256",
            "-channel", "A",
            "-threshold", "50%",
            f"{png_path}"
        ])

        os.unlink("out.png")

        emoji_map["names"][name] = codepoint

    except Exception as e:
        print(f"Skipping {filename}: {e}")

result = subprocess.run(["./pack-assets.sh"], capture_output=True, text=True)
hash_  = result.stdout.split(' ')[0]

emoji_map["assets_hash"] = hash_

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(emoji_map, f, ensure_ascii=False, indent=2)
