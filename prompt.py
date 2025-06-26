from models.ModelConfigs import MODEL_CONFIGURATIONS

class Prompt:
    def __init__(self, json):
        self._json = json

        self._request_id = json['id']
        self._model_number = int(json['modelNumber'])
        self._model_config = MODEL_CONFIGURATIONS[self._model_number]
        self._model_path = self._model_config.model
        self._seed = json['seed']
        self._inference_steps = json['inferenceSteps']
        self._guidance_scale = json['guidanceScale']
        self._negative_prompt = json['negative-prompt']
        self._generation_prompt = json['generation-prompt']
        self._resolution_key = int(json['resolution'])
        self._high_contrast = bool(json['high-contrast'])
        self._water_color = bool(json['water-color'])
        self._photo_realistic = bool(json['photo-realistic'])
        self._anime = bool(json['anime'])
        self._sketch = bool(json['sketch'])
        self._charcoal = bool(json['charcoal'])
        self._impressionist = bool(json['impressionist'])
        self._use_recommended = bool(json['recommended'])
        self._upscale_small_images = bool(json['upscale-small-images'] if 'upscale-small-images' in json else False)

        self._use_memory_efficient = False


    def to_json(self):
        return {
            'id': self._request_id,
            'modelNumber': self._model_number,
            'seed': self._seed,
            'inferenceSteps': self._inference_steps,
            'guidanceScale': self._guidance_scale,
            'negative-prompt': self._negative_prompt,
            'generation-prompt': self._generation_prompt,
            'resolution': self._resolution_key,
            'high-contrast': self._high_contrast,
            'water-color': self._water_color,
            'photo-realistic': self._photo_realistic,
            'anime': self._anime,
            'sketch': self._sketch,
            'charcoal': self._charcoal,
            'impressionist': self._impressionist,
            'recommended': self._use_recommended,
            'upscale-small-images': self._upscale_small_images
        }

    @property
    def use_memory_efficient(self):
        return self._use_memory_efficient

    @property
    def request_id(self):
        return self._request_id
    
    @property
    def model_number(self):
        return self._model_number
    
    @property
    def model_config(self):
        return self._model_config
    
    @property
    def model_path(self):
        return self._model_path
    
    @property
    def seed(self):
        return self._seed
    
    @property
    def inference_steps(self):
        return self._inference_steps
    
    @property
    def guidance_scale(self):
        return self._guidance_scale
    
    @property
    def negative_prompt(self):
        return self._negative_prompt
    
    @property
    def generation_prompt(self):
        return self._generation_prompt
    
    @property
    def resolution_key(self):
        return self._resolution_key

    @property
    def resolution(self):
        return self.model_config.resolutions[self._resolution_key]
    
    @property
    def high_contrast(self):
        return self._high_contrast
    
    @property
    def water_color(self):
        return self._water_color
    
    @property
    def photo_realistic(self):
        return self._photo_realistic
    
    @property
    def anime(self):
        return self._anime
    
    @property
    def sketch(self):
        return self._sketch
    
    @property
    def charcoal(self):
        return self._charcoal
    
    @property
    def impressionist(self):
        return self._impressionist
    
    @property
    def use_recommended(self):
        return self._use_recommended

    @property
    def upscale_small_images(self):
        return self._upscale_small_images


    def get_prompt_text(self):
        prompt = self.generation_prompt
        if self.use_recommended:
            prompt = self.model_config.prompt_tip.replace("{SUBJECT}", prompt)
        else:
            if self.charcoal:
                prompt = "(charcoal):2.0, " + prompt

            if self.sketch:
                prompt = "(sketch, pencil, drawing):2.1," + prompt

            if self.water_color:
                prompt = "(water color):2.2," + prompt

            if self.high_contrast:
                prompt = "(high contrast):1.8, " + prompt

            if self.anime:
                prompt = "(anime:2.1, cgi, cartoon:1.5)," + prompt

            if self.photo_realistic:
                prompt = "(realistic, 8K, photo-realistic:1.4)," + prompt
            if self.impressionist:
                prompt = "(impressionist):2.1," + prompt

        return prompt
