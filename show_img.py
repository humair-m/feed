import json
import os
from PIL import Image

# Path to the JSONL file
jsonl_path = 'output_images/deduped_data.jsonl'

# Number of entries to show (set to None to show all)
max_entries = 5

print("📄 Showing prompts and opening image files:\n")

with open(jsonl_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        entry = json.loads(line)

        # Extract prompt
        prompt = None
        if 'parameters' in entry and 'messages' in entry['parameters']:
            for msg in entry['parameters']['messages']:
                if isinstance(msg, dict) and 'content' in msg:
                    if isinstance(msg['content'], list):
                        for item in msg['content']:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                prompt = item.get('text')
                                break
                    elif isinstance(msg['content'], str):
                        prompt = msg['content']
                if prompt:
                    break
        
        prompt = prompt or "[No prompt found]"

        # Image path
        image_path = entry.get('img_path', None)

        # Display prompt and image
        print(f"🔹 Entry {idx + 1}")
        print(f"📝 Prompt: {prompt}")
        print(f"🖼️ Image Path: {image_path}\n")

        # Open the image if it exists
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.show()
            except Exception as e:
                print(f"⚠️ Failed to open image: {e}")

        if max_entries and idx + 1 >= max_entries:
            break
