.PHONY: test sdist wheel release pre-release clean

test:
	python runtests.py

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal

release: clean sdist wheel
	twine upload dist/*

pre-release: sdist wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
