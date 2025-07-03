import os, shutil, re

DATA_FOLDER = 'static/gallery/'
IMAGES_FOLDER = DATA_FOLDER + 'images/'
PROMPTS_FOLDER = DATA_FOLDER + 'prompts/'

def setup():
    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
    if not os.path.exists(PROMPTS_FOLDER):
        os.makedirs(PROMPTS_FOLDER)
    return


def get_all():
    images = []
    
    for file in os.listdir(IMAGES_FOLDER):
        if file.endswith('.png') and file.startswith('image-'):
            guid_pattern = r'image-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.png'
            match = re.match(guid_pattern, file)
            image_id = match.group(1) if match else file.replace('.png', '').replace('image-', '')
            filepath = os.path.join(IMAGES_FOLDER, file)
            created_time = os.path.getctime(filepath)
            images.append({
                'url': IMAGES_FOLDER + file,
                'id': image_id,
                'created': created_time
            })
        else:
            continue

    images.sort(key=lambda x: x['created'], reverse=True)
    return images


def get_image_filename(image_id):
    prompt_file = IMAGES_FOLDER + 'image-' + image_id + '.png'
    return prompt_file


def get_prompt(image_id):
    prompt_file = PROMPTS_FOLDER + image_id + '.json'
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r') as f:
            return f.read()
    return None


def delete_all():
    for filename in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    return


def delete_image(image_id):
    prompt_file = PROMPTS_FOLDER + image_id + '.json'
    if os.path.exists(prompt_file):
        os.remove(prompt_file)
    image_file = IMAGES_FOLDER + 'image-' + image_id + '.png'
    if os.path.exists(image_file):
        os.remove(image_file)


def save_prompt(image_id, prompt_json):
    prompt_file = PROMPTS_FOLDER + image_id + '.json'
    with open(prompt_file, 'w') as f:
        f.write(str(prompt_json))
