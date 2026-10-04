PYTHON ?= python3
PACKAGE_PATH := $(CURDIR)/.claude/contextdb

.PHONY: test validate manifest clean

test:
	PYTHONPATH="$(PACKAGE_PATH)" $(PYTHON) -W error::ResourceWarning -m unittest discover -s tests -v

validate:
	$(PYTHON) validate.py

# Every tracked file except the manifest itself, as ./-relative sha256 lines in C-locale order.
manifest:
	git ls-files . ':!MANIFEST.sha256' | sed 's|^|./|' | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
	rm -f .claude/contextdb/state/context.db*
	rm -f .claude/contextdb/state/.writer.lock
