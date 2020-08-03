# Deploy to test repository

```
# https://packaging.python.org/guides/using-testpypi/
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install twine wheel
rm -rf dist/ build/ slack_bolt.egg-info/ && python setup.py sdist bdist_wheel
twine check dist/*

# Deploy to test repository
twine upload --repository testpypi dist/*
# Test installation
pip install -U --index-url https://test.pypi.org/simple/ slack_bolt
```
