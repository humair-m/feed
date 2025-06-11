import os
import json
import base64
import re

input_file = '/home/humair/pollinations_v00.jsonl'
output_dir = 'output_images'
output_file = os.path.join(output_dir, 'new_data.jsonl')

os.makedirs(output_dir, exist_ok=True)

def extract_and_replace_b64(obj, image_index):
    """
    Recursively find and replace base64 image strings in nested dict/list.
    Returns updated object and new image index.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if (
                k == "url" and
                isinstance(v, str) and
                v.startswith("data:image/") and
                "base64," in v
            ):
                header, b64data = v.split('base64,', 1)
                match = re.search(r'data:image/(\w+);', header)
                if match:
                    ext = match.group(1)
                    img_filename = f'image_{image_index:05d}.{ext}'
                    img_path = os.path.join(output_dir, img_filename)

                    with open(img_path, 'wb') as f:
                        f.write(base64.b64decode(b64data))

                    print(f"✅ Replaced base64 with: {img_path}")
                    new_dict[k] = img_path
                    image_index += 1
                else:
                    new_dict[k] = v
            else:
                new_dict[k], image_index = extract_and_replace_b64(v, image_index)
        return new_dict, image_index

    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            new_item, image_index = extract_and_replace_b64(item, image_index)
            new_list.append(new_item)
        return new_list, image_index

    else:
        return obj, image_index


image_index = 1
with open(input_file, 'r', encoding='utf-8') as fin, \
     open(output_file, 'w', encoding='utf-8') as fout:

    for line_num, line in enumerate(fin, 1):
        try:
            data = json.loads(line)
            new_data, image_index = extract_and_replace_b64(data, image_index)
            fout.write(json.dumps(new_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"❌ Error on line {line_num}: {e}")

print(f"\n🎉 All done! Extracted images saved in '{output_dir}/', updated JSONL at '{output_file}'")
