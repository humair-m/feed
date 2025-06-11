import os
import json
import hashlib

# Paths
jsonl_path = 'output_images/new_data.jsonl'
images_dir = 'output_images'
output_jsonl_path = 'output_images/deduped_data.jsonl'

# Map: hash -> canonical image path
hash_to_path = {}
# Map: original image path -> new image path (after deduplication)
path_replacements = {}

def compute_image_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# 1. Scan image files and compute hashes
print("🔍 Scanning image files for duplicates...\n")
for filename in os.listdir(images_dir):
    filepath = os.path.join(images_dir, filename)
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')):  # skip non-images
        continue

    img_hash = compute_image_hash(filepath)
    
    if img_hash not in hash_to_path:
        hash_to_path[img_hash] = filepath  # keep this one
        print(f"✅ Unique image: {filename}")
    else:
        # Duplicate found
        original = hash_to_path[img_hash]
        path_replacements[filepath] = original
        os.remove(filepath)  # delete duplicate
        print(f"🗑️  Duplicate image removed: {filename} (same as {os.path.basename(original)})")

print("\n📁 All duplicates removed.\n")

# 2. Update JSONL with deduplicated image paths
print("✍️ Updating JSONL entries...")

with open(jsonl_path, 'r', encoding='utf-8') as fin, \
     open(output_jsonl_path, 'w', encoding='utf-8') as fout:

    for line in fin:
        entry = json.loads(line)
        if 'img_path' in entry:
            old_path = entry['img_path']
            new_path = path_replacements.get(old_path, old_path)
            entry['img_path'] = new_path
        fout.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"\n🎉 All done! Duplicates cleaned and JSONL updated at '{output_jsonl_path}'")
