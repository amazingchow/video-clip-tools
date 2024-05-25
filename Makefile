include .env.local .env.secret .env.shared
export

VERSION  := v0.1.0
GIT_HASH := $(shell git rev-parse --short HEAD)
SRC      := $(shell find . -type f -name '*.py' -not -path "./.venv/*")
CURR_DIR := $(shell pwd)

.PHONY: help
help: ### Display this help screen.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: init
init: ### Initialize the project.
	@echo "Initializing the project..."
	@echo "Creating directories..."
	@mkdir -p ./.data/.audio_tmp
	@mkdir -p ./.data/.blurred_video_tmp
	@mkdir -p ./.data/.cover_tmp
	@mkdir -p ./.data/.srt_files
	@mkdir -p ./.data/.texted_video_tmp
	@mkdir -p ./.data/.video_tmp
	@mkdir -p ./.data/.whisper_model
	@echo "Creating virtual env..."
	@poetry install

.PHONY: lint
lint: ### Improve your code style. (isort, pyflakes, pycodestyle)
	@echo "Running import sort..."
	@isort --atomic --multi-line=VERTICAL_HANGING_INDENT ${SRC}
	@echo "Running static code analysis..."
	@pyflakes ${SRC}
	@echo "Running code style check..."
	@pycodestyle ${SRC} --ignore=W293,E131,E402,E501

.PHONY: extract_audio_from_video
extract_audio_from_video: ### Extract audio from video files.
	@echo "Extracting audio from video files..."
	@poetry run python -m video_clip_tools.extract_audio_from_video

.PHONY: extra_content_from_audio
extra_content_from_audio: ### Extract content from audio files.
	@echo "Extracting content from audio files..."
	@poetry run python -m video_clip_tools.extra_content_from_audio
