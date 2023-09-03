VERSION  := v1.0.0
GIT_HASH := $(shell git rev-parse --short HEAD)
SERVICE  := video-zimu-translator

.PHONY: help
help: ### Display this help screen.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: deps
deps: ### Package the runtime requirements.
	@pip freeze > requirements.txt

.PHONY: lint
lint: ### Improve your code style.
	@pyflakes gen_zimu.py
	@pycodestyle gen_zimu.py --ignore=E101,E121,E123,E124,E125,E126,E128,E131,E266,E402,E501,E731,W191,W293,W503
	@pyflakes add_text_and_blur.py
	@pycodestyle add_text_and_blur.py --ignore=E101,E121,E123,E124,E125,E126,E128,E131,E266,E402,E501,E731,W191,W293,W503

.PHONY: init
init: ### Init runtime env.
	@mkdir -p .video_tmp
	@mkdir -p .audio_tmp
	@mkdir -p .whisper_model
	@mkdir -p .srt_files
	@mkdir -p .texted_video_tmp
	@mkdir -p .blurred_video_tmp
