
.PHONY: help  # Shows this message
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20

.PHONY: clean  # Cleaning artefacts
clean:
	find . | grep -E "(dist$$|node_modules$$)" | xargs rm -rf


.PHONY: check  # Runs linters
check:
	@echo "Run eslint"
	@exec yarn run lint
	@exec yarn run biome-lint

.PHONY: lint  # Runs linters and fixes auto-fixable errors
lint:
	@echo "Run eslint"
	@exec yarn run lint --fix
	@exec yarn run biome-check

.PHONY: test  # Runs tests
test:
	@echo "Run tests"

.PHONY: install  # Install base+dev requirements
install:
	@exec yarn install


.PHONY: dev  # Run dev server
dev:
	@exec yarn run dev --host 0.0.0.0 --port 5173

.PHONY: start  # Run prod server
start:
	@exec nginx -g 'daemon off;'

.PHONY: build  # Build prod server
build:
	@exec yarn run build

