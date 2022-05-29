.PHONY: check-black check-isort check-flake8 static-analysis test sdist wheel release pre-release clean

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal

release: clean sdist wheel
	twine upload dist/*

pre-release: sdist wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$)' | xargs rm -rf
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

check-black:
	@echo "--> Running black checks"
	@black --check --diff .

check-isort:
	@echo "--> Running isort checks"
	@isort --check-only .

check-flake8:
	@echo "--> Running flake8 checks"
	@flake8 .

check-yamllint:
	@echo "--> Running yamllint checks"
	@yamllint .

static-analysis: check-black check-isort check-flake8 check-yamllint

# Format code
.PHONY: fmt

fmt:
	@echo "--> Running isort"
	@isort .
	@echo "--> Running black"
	@black .

# Test
.PHONY: test

test:
	@echo "--> Running tests"
	PYTHONWARNINGS=all PYTHONPATH=".:tests:$PYTHONPATH" django-admin test --settings=tests.settings
