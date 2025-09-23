# List of directories to remove
CLEAN_BUILD_DIRS = _build jupyter_execute
CLEAN_DIRS = $(CLEAN_BUILD_DIRS) downloaded reference sections_readme

.PHONY: clean clean_build

# Removes the specified directories
clean:
	rm -rf $(CLEAN_DIRS)

clean_build:
	rm -rf $(CLEAN_BUILD_DIRS)

build:
	sphinx-apidoc --force --implicit-namespaces --module-first -o reference ../src/vuegen
	python split_readme.py
	sphinx-build -n -W --keep-going -b html ./ ./_build/