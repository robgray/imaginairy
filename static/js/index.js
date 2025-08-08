function loadPrompt(prompt) {
    // upscale-small-images is not in earlier versions of the prompt
    const upscaleSmallImages = prompt['upscale-small-images'] ?? false;

    $('#generation-prompt').val(prompt["generation-prompt"]);
    $('#negative-prompt').val(prompt["negative-prompt"]);
    $('#resolution').val(prompt.resolution).change();
    $('#seed').val(prompt.seed).trigger('change');
    $('#model').val(prompt.modelNumber).trigger('change');
    $('#guidance-scale').val(prompt.guidanceScale);
    $('#inference-steps').val(prompt.inferenceSteps);
    $('#recommended').prop('checked', prompt.recommended);
    $('#high-contrast').prop('checked', prompt['high-contrast']);
    $('#photo-realistic').prop('checked', prompt['photo-realistic']);
    $('#water-color').prop('checked', prompt['water-color']);
    $('#sketch').prop('checked', prompt.sketch);
    $('#anime').prop('checked', prompt.anime);
    $('#charcoal').prop('checked', prompt.charcoal);
    $('#impressionist').prop('checked', prompt.impressionist);
    $('#upscale-small-images').prop('checked', upscaleSmallImages);

    updateWordCount(prompt);

    window.history.pushState({}, '', '/');
}

function onModelLoaded(data) {
    const inferenceSteps = $('#inference-steps');
    const guidanceScale = $('#guidance-scale');
    const resolution = $('#resolution');
    const helpLink = $('#help-link');
    const negativePrompt = $('#negative-prompt');

    $('#recommended-prompt').html(data.prompt)

    negativePrompt.val(data.negativePrompt);
    negativePrompt.data('text', data.negativePrompt);

    helpLink.attr('href', data.url);

    inferenceSteps
        .attr('min', data.inferenceStepsMin)
        .attr('max', data.inferenceStepsMax)
        .val(data.inferenceStepsDefault)
        .trigger('change');

    guidanceScale
        .attr('min', data.guidanceScaleMin)
        .attr('max', data.guidanceScaleMax)
        .val(data.guidanceScaleDefault)
        .trigger('change');

    resolution.empty();
    data.resolutions.forEach(function (res, index) {
        const option = $(`<option value=${index}>${res[0]} x ${res[1]}</option>`);
        if (index === data.resolutionsDefaultIndex)
        {
            option.attr('selected', 'selected');
        }
        resolution.append(option);
    })

    // once the model is loaded, load the prompt if it exists
    if (window.location.search.includes('prompt_id'))
    {
        const promptId = window.location.search.split('prompt_id=')[1];
        $.ajax({
            type: 'GET',
            url: `/api/prompts/${promptId}`,
            success: loadPrompt
        })
    }
}

function updateWordCount(prompt, options) {
    $.ajax({
            type: 'POST',
            url: '/api/token-count',
            contentType: 'application/json',
            data: JSON.stringify(buildPromptRequestData()),
            success: (data) => {
                const wordCountLabel = $("#wordCount");
                wordCountLabel.html(data.token_count);
                if (data.token_count > 75) {
                    wordCountLabel.addClass('text-red-500');
                } else {
                    wordCountLabel.removeClass('text-red-500');
                }
            }
        })
}

function buildPromptRequestData()
{
    return {
                'id': crypto.randomUUID().toString(),
                'modelNumber': $('#model').val(),
                'inferenceSteps': $('#inference-steps').val(),
                'guidanceScale': $('#guidance-scale').val(),
                'seed': $('#seed').val(),
                'resolution': $('#resolution').val(),
                'negative-prompt': $('#negative-prompt').val(),
                'generation-prompt': $('#generation-prompt').val(),
                'high-contrast': $('#high-contrast').is(':checked'),
                'water-color': $('#water-color').is(':checked'),
                'photo-realistic': $('#photo-realistic').is(':checked'),
                'charcoal': $('#charcoal').is(':checked'),
                'anime': $('#anime').is(':checked'),
                'sketch': $('#sketch').is(':checked'),
                'impressionist': $('#impressionist').is(':checked'),
                'recommended': $('#recommended').is(':checked'),
                'upscale-small-images': $('#upscale-small-images').is(':checked')
            };
}

$(document).ready(function () {

    const generateSeedButton = $('#generate-seed');
    const clearSeedButton = $('#clear-seed');
    const resetNegativePromptButton = $('#reset-negative-prompt');
    const inferenceSteps = $('#inference-steps');
    const guidanceScale = $('#guidance-scale');
    const recommendedCheckbox = $('#recommended');

    recommendedCheckbox.click(() => {
        updateWordCount(buildPromptRequestData());
        if (recommendedCheckbox.is(':checked')) {
            $(".style-choice").prop("checked", false);
        }
    })

    $(".style-choice").click(function() {
        updateWordCount(buildPromptRequestData());
        if ($(this).is(':checked')) {
            recommendedCheckbox.prop("checked", false);
        }
    })

    $('#keep-image').click(function() {
        const $this = $(this);
        const requestId = $this.data('id');
        if (!requestId)
        {
            toastr.error('No request id');
            return;
        }
        $.ajax({
            type: 'POST',
            url: `/api/keep-image`,
            contentType: 'application/json',
            data: JSON.stringify({
                'requestid': `${requestId}`
            }),
            success: function (data) {
                $this.addClass('hidden');
                toastr.success('Image saved');
            }
        })
    })

    generateSeedButton.click(() => {
        const seedInput = $('#seed');
        const min = Number(seedInput.attr("min"));
        const max = Number(seedInput.attr("max"));
        const range = max - min;
        const seed = Math.floor(Math.random() * range) + min;

        seedInput.val(seed);
    })

    clearSeedButton.click(() => {
        $('#seed').val(-1);
    })

    resetNegativePromptButton.click(() => {
        const negativePrompt = $('#negative-prompt');
        negativePrompt.val(negativePrompt.data('text'));
    });

    inferenceSteps.change(() => $('#inference-steps-value').html(inferenceSteps.val()));
    guidanceScale.change(() => $('#guidance-scale-value').html(guidanceScale.val()));

    $('#start-generation').click(() => {

        const generateButton = $('#start-generation');
        const originalText = generateButton.html();
        generateButton.html("<i class='fas fa-spinner fa-spin mr-2'></i> Generating...");
        generateButton.addClass('disabled');

        // Start the generation
        $('#generation-image')
            .removeAttr('src')
            .show();

        $('#keep-image')
            .data('id', '')
            .addClass('hidden');

        $.ajax({
            type: 'POST',
            url: '/api/start_generation',
            contentType: 'application/json',
            data: JSON.stringify(buildPromptRequestData()),
            success: function (data)
            {
                // Check every 5 seconds
                let intervalId = setInterval(function ()
                {
                    const requestId = data.id;
                    $.ajax({
                        type: 'GET',
                        url: '/api/check_generation/' + requestId,
                        success: function (data) {
                            if (data.finished === true)
                            {
                                $('#generation-image')
                                    .attr('src', data.image)
                                    .show();

                                $('#keep-image')
                                    .data('id', requestId)
                                    .removeClass('hidden');

                                clearInterval(intervalId);

                                $('#start-generation')
                                    .html(originalText)
                                    .removeClass('disabled');

                                $("#resultsSection").removeClass("hidden");
                            }
                        }
                    });
                }, 5000);
          }
        });
    });

    $('#model').change(() => {
        $.ajax({
            type: 'GET',
            url: '/api/models/' + $('#model').val(),
            success: onModelLoaded
        })
    });

    $("#generation-prompt").on('input', function() {
        const text = $(this).val().trim();
        const options = {
                'high-contrast': $('#high-contrast').is(':checked'),
                'water-color': $('#water-color').is(':checked'),
                'photo-realistic': $('#photo-realistic').is(':checked'),
                'charcoal': $('#charcoal').is(':checked'),
                'anime': $('#anime').is(':checked'),
                'sketch': $('#sketch').is(':checked'),
                'impressionist': $('#impressionist').is(':checked'),
                'recommended': $('#recommended').is(':checked'),
            };
        updateWordCount(text, options);
    });

    resetNegativePromptButton.trigger('click');
    clearSeedButton.trigger('click');

    $('#model').trigger('change');
});
