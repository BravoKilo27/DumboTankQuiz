import os
import json
import re

IMG_DIR = 'img'
DIFFS = ['leicht', 'mittel', 'schwer']
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.avif'}

baked = {}

for vehicle_folder in sorted(os.listdir(IMG_DIR)):
    vehicle_path = os.path.join(IMG_DIR, vehicle_folder)
    if not os.path.isdir(vehicle_path):
        continue

    match = re.match(r'^([a-z][0-9]+)_', vehicle_folder)
    if not match:
        continue

    vehicle_id = match.group(1)
    images = []

    for diff in DIFFS:
        diff_path = os.path.join(vehicle_path, diff)
        if not os.path.isdir(diff_path):
            continue
        for filename in sorted(os.listdir(diff_path)):
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                images.append({
                    'src': f'{IMG_DIR}/{vehicle_folder}/{diff}/{filename}',
                    'diff': diff
                })

    if images:
        baked[vehicle_id] = images

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

baked_json = json.dumps(baked, ensure_ascii=False, separators=(',', ':'))
content = re.sub(
    r'const BAKED_IMAGES = \{[\s\S]*?\};',
    f'const BAKED_IMAGES = {baked_json};',
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

total = sum(len(v) for v in baked.values())
print(f"BAKED_IMAGES updated: {len(baked)} vehicles, {total} images total.")
