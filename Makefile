.PHONY: test sdist wheel release pre-release clean

test:
	PYTHONWARNINGS=all PYTHONPATH=".:tests:$PYTHONPATH" django-admin.py test --settings=tests.settings

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
