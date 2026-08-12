PYTHON ?= python3
PACKAGE_PATH := $(CURDIR)/.claude/contextdb

.PHONY: test validate clean

test:
	PYTHONPATH="$(PACKAGE_PATH)" $(PYTHON) -W error::ResourceWarning -m unittest discover -s tests -v

validate:
	$(PYTHON) validate.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
	rm -f .claude/contextdb/state/context.db*
	rm -f .claude/contextdb/state/.writer.lock
