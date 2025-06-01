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

for filename in os.listdir(SVG_DIR):
    if not filename.endswith(".svg"):
        continue

    codepoint = filename[:-4].lower()  # remove .svg extension
    svg_path = os.path.join(SVG_DIR, filename)
    png_path = os.path.join(PNG_DIR, f"{codepoint}.png")

    try:
        char = chr(int(codepoint, 16))
        name = emoji.demojize(char)
        name = name[1:-1].lower()
        name = name.replace("’", "")

        if not name:
            continue

        subprocess.run([
            "inkscape",
            svg_path,
            "--export-type=png",
            f"--export-filename=out.png",
            f"--export-width={PNG_SIZE}",
            f"--export-height={PNG_SIZE}"
            #"--export-background=#000000",
            #"--export-background-opacity=1.0"
        ], check=True)

        # remove opacity
        subprocess.run([
            "convert",
            "out.png",
            "(", "+clone", "-alpha", "extract", "-threshold", "50%", ")",
            "-compose",
            "CopyOpacity",
            "-composite",
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
