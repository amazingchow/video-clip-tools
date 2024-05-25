include .env.local .env.secret .env.shared
export

VERSION  := v0.1.0
GIT_HASH := $(shell git rev-parse --short HEAD)
SRC      := $(shell find . -type f -name '*.py' -not -path "./venv/*")
CURR_DIR := $(shell pwd)

.PHONY: help
help: ### Display this help screen.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: init
init: ### Initialize the project.
	@mkdir -p ${CURR_DIR}/.data/.audio_tmp \
		${CURR_DIR}/.data/.blurred_video_tmp \
		${CURR_DIR}/.data/.cover_tmp \
		${CURR_DIR}/.data/.srt_files \
		${CURR_DIR}/.data/.texted_video_tmp \
		${CURR_DIR}/.data/.video_tmp \
		${CURR_DIR}/.data/.whisper_model
	@poetry install

.PHONY: lint
lint: ### Improve your code style. (isort, pyflakes, pycodestyle)
	@echo "Running import sort..."
	@isort --atomic --multi-line=VERTICAL_HANGING_INDENT ${SRC}
	@echo "Running static code analysis..."
	@pyflakes ${SRC}
	@echo "Running code style check..."
	@pycodestyle ${SRC} --ignore=W293,E131,E402,E501
