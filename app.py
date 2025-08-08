import os, shutil, json
from flask import Flask, render_template, jsonify, request
from flask_executor import Executor
from transformers import CLIPTokenizer

# Custom imports
from gallery import (
    IMAGES_FOLDER,
    PROMPTS_FOLDER,
    setup as gallery_setup,
    get_all as get_all_gallery_images,
    delete_all as delete_all_gallery_images,
    delete_image as delete_gallery_image,
    get_image_filename as get_gallery_image_filename,
)
import image_generator
from prompt import Prompt
from models.ModelConfigs import MODEL_CONFIGURATIONS

clip_tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")

app = Flask(__name__)
executor = Executor(app)


###
### Page methods
###


@app.route('/')
def index():

    # Ensure data directories exist
    image_generator.setup()
    gallery_setup()

    models_data = []

    for index, model in enumerate(MODEL_CONFIGURATIONS):
        model_data = {
            "index": index,
            "display_name": model.display_name,
        }
        models_data.append(model_data)

    # Clean temp image files every time the page is hit
    folder = 'static/temp-images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    prompt_id: str | None = request.args.get('prompt_id')
    if prompt_id is not None:
        filename = PROMPTS_FOLDER + prompt_id + '.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                prompt_data = json.load(f)
        else:
            prompt_data = None
        if prompt_data is not None:
            prompt_json = Prompt(prompt_data).to_json()
            return render_template('index.html', models=models_data, prompt=prompt_json)

    return render_template('index.html', models=models_data)


@app.route('/gallery')
def gallery():
    images = get_all_gallery_images()
    return render_template('gallery.html', images=images)


@app.route('/image-viewer/<request_id>')
def image_viewer(request_id):
    image_filename = get_gallery_image_filename(request_id)
    return render_template('image-viewer.html', image_url='/' + image_filename)


##
## API Methods
##
@app.route("/api/token-count", methods=[ 'POST' ])
def get_token_count():
    prompt = Prompt(request.json)
    prompt_text = prompt.get_prompt_text()
    
    if not prompt_text:
        return jsonify({"token_count": 0 })

    # Tokenize using CLIPTokenizer
    tokens = clip_tokenizer.encode(prompt_text)
    token_count = len(tokens)
    return jsonify({"token_count": token_count})

@app.route("/api/models/<index>", methods=[ 'GET' ])
def get_model_options(index):
    model_config = MODEL_CONFIGURATIONS[int(index)]
    return jsonify({
        'inferenceStepsMin': model_config.inference_step_min,
        'inferenceStepsMax': model_config.inference_step_max,
        'inferenceStepsDefault': model_config.inference_step_default,
        'guidanceScaleMin': model_config.guidance_scale_min,
        'guidanceScaleMax': model_config.guidance_scale_max,
        'guidanceScaleDefault': model_config.guidance_scale_default,
        'resolutions': model_config.resolutions,
        'resolutionsDefaultIndex': model_config.resolutions_default_index,
        'url': model_config.url,
        'negativePrompt': model_config.negative_prompt_tip,
        'prompt': model_config.prompt_tip,
    })


@app.route('/api/keep-image', methods=['POST'])
def keep_image():
    request_id = request.json['requestid']
    os.rename(image_generator.TEMP_PATH + 'image-' + request_id + '.png', IMAGES_FOLDER + 'image-' + request_id + '.png')
    os.rename(image_generator.TEMP_PATH + request_id + '.json', PROMPTS_FOLDER + request_id + '.json')
    return jsonify({'message': 'Image saved to Gallery'})


@app.route('/api/start_generation', methods=['POST'])
def start_generation():
    prompt = Prompt(request.json)

    executor.submit(image_generator.generate, prompt)
    image_generator.save_temp_prompt(prompt)

    return jsonify({'id': prompt.request_id, 'message': 'Generating image'})


@app.route('/api/check_generation/<request_id>', methods=[ 'GET' ])
def check_generation(request_id):
    # Check if the image file exists
    if image_generator.is_generated(request_id):
        return jsonify({'finished': True,
                        'message': 'generation complete',
                        'image': image_generator.TEMP_PATH + 'image-' + request_id + '.png'})
    else:
        return jsonify({'id': request_id, 'finished': False, 'message': 'generation running'})


@app.route('/api/images', methods=['DELETE'])
def delete_all_images():
    delete_all_gallery_images()
    return '', 204


@app.route('/api/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    delete_gallery_image(image_id)
    return '', 204


@app.route('/api/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    filename = PROMPTS_FOLDER + prompt_id + '.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            prompt_data = json.load(f)
        return jsonify(prompt_data)
    else:
        return jsonify({'error': 'Prompt not found'}), 404


if __name__ == '__main__': app.run(debug=False)