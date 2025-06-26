# image-generation
learning python with text to image

Models are downloaded as `.safetensor` files, mostly from [Civitai.com](https://civitai.com).

When downloaded, use `models/import_sd_model.py` to convert the safetensor files for use:
```
python import_sd_model.py --checkpoint_path
  <file>.safetensors --dump_path <an identifying folder>/ 
  --from_safetensors
```
e.g.

```
python import_sd_model.py --checkpoint_path
  realisticVisionV60B1_v51HyperVAE.safetensors --dump_path realistic/ 
  --from_safetensors
```

I've abstracted the settings for each different model in ModelConfig. 
This provides settings for the UI that are best suited for the particular model, 
as suggested from the model page on Civitai.com. 
I've left some range either side of the recommended settings so they can be played with a bit.

To get going, make use Python `3.12` and run `main.py` which will start a Flask web api and basic jquery UI. 

## Getting going
Getting going can be a PITA.
Assuming CUDA is available here...
see https://pytorch.org/get-started/locally/ to get your version of CUDA. I have a 4070ti SUPER and installed CUDA SDK 12.8.

```aiignore
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```