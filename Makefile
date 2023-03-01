GLOBAL_PY := python3
BUILD_VENV ?= .venv
BUILD_PY := $(BUILD_VENV)/bin/python

# .PHONY: init
# init: node_modules $(BUILD_VENV)

# node_modules: package.json package-lock.json
# 	npm install

# $(BUILD_VENV):
# 	$(GLOBAL_PY) -m venv $(BUILD_VENV)
# 	$(BUILD_PY) -m pip install -U pip

.PHONY: run
run:
	$(BUILD_VENV)/bin/python -m server &
	cd frontend && npm run dev &

.PHONY: run-ha
run-ha:
	docker-compose \
		-f dev/homeassistant/docker-compose.yml \
		up
