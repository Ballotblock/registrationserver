# Running Test
Execute this command in the root project folder
``python -m unittest tests/test_foobar.py``

# Coverage
Install ``python-coverage`` then execute from
the root project folder:

```python
python -m unittest discover
coverage run -m unittest discover
coverage html
firefox  htmlcov/index.html
```

``coverage`` will output HTML files that make it
trivial to see which sections of code haven't been 
executed yet. These sections should have unittests written 
for them!