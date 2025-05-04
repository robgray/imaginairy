class ModelConfig:
    def __init__(self,
                 model: str,
                 display_name: str,
                 use_32bit: bool,
                 inference_step_min: int,
                 inference_step_max: int,
                 inference_step_default: int,
                 guidance_scale_min: float,
                 guidance_scale_max: float,
                 guidance_scale_default: float,
                 resolutions: list[tuple[int, int]],
                 resolutions_default_index: int,
                 url: str | None,
                 prompt_tip: str | None = None,
                 negative_prompt_tip: str | None = None,
    ):
        self._model = model
        self._display_name = display_name
        self._use_32bit = use_32bit
        self._inference_step_min = inference_step_min
        self._inference_step_max = inference_step_max
        self._inference_step_default = inference_step_default
        self._guidance_scale_min = guidance_scale_min
        self._guidance_scale_max = guidance_scale_max
        self._guidance_scale_default = guidance_scale_default
        self._resolutions = resolutions
        self._resolutions_default_index = resolutions_default_index
        self._url = url
        self._prompt_tip = prompt_tip
        self._negative_prompt_tip = negative_prompt_tip

    @property
    def model(self) -> str:
        return self._model

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def use_32bit(self) -> bool:
        return self._use_32bit

    @property
    def inference_step_min(self) -> int:
        return self._inference_step_min

    @property
    def inference_step_max(self) -> int:
        return self._inference_step_max

    @property
    def inference_step_default(self) -> int:
        return self._inference_step_default

    @property
    def guidance_scale_min(self) -> float:
        return self._guidance_scale_min

    @property
    def guidance_scale_max(self) -> float:
        return self._guidance_scale_max

    @property
    def guidance_scale_default(self) -> float:
        return self._guidance_scale_default

    @property
    def resolutions(self) -> list[tuple[int, int]]:
        return self._resolutions

    @property
    def resolutions_default_index(self) -> int:
        return self._resolutions_default_index

    @property
    def url(self) -> str | None:
        return self._url

    @property
    def prompt_tip(self) -> str | None:
        return self._prompt_tip

    @property
    def negative_prompt_tip(self) -> str | None:
        return self._negative_prompt_tip