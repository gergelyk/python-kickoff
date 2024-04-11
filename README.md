# kickoff

Turns your Python script or module into an application with decent user interface.

Let's have a look at `demo.py`:

```py
"""Very simple application"""

def hello(*, name="World"):
    """Say hello"""

    print(f"Hello {name}!")
```

![](https://raw.githubusercontent.com/gergelyk/python-kickoff/master/docs/source/_static/demo-cli.png)

![](https://raw.githubusercontent.com/gergelyk/python-kickoff/master/docs/source/_static/demo-gui.png)

## For software developers...

*kickoff* is inspired by utilities like [invoke](http://www.pyinvoke.org), [fire](https://github.com/google/python-fire), [runfile](https://code.activestate.com/pypm/runfile). It has similar function with this difference that it looks at function signatures, therefore doesn't need from the developer to use decorators or any dedicated API. This way *kickoff* provides developers with following advantages:

* Basic UI provided with zero overhead
* Enhanced UI provided through annotations
* Compatibility with environments where *kickoff* is not installed
* Testability and reusability of top-level commands
* Shebang support

## For software users...

*kickoff* is built on top of stunning [click](https://click.palletsprojects.com/) module as well as third-party add-ons to provide the users with following features:

* Hierarchical CLI interface
* Correction suggestions for misspelled commands
* REPL with command completion and access to underlying shell
* GUI (experimental feature)

## Resources

* [Source Code](https://github.com/gergelyk/python-kickoff)
* [Package](https://pypi.org/project/kickoff/)
* [Documentation](https://python-kickoff.readthedocs.io/en/latest/)

## Development

Preparing environment:

```python
./setup.sh
source venv/bin/activate
```

Updating dependencies:

```python
vi requirements.in
vi setup.py
pip-compile
pip-sync
```

Releasing:

```python
# update version:
vi docs/source/conf.py
vi setup.py
git commit -am "foobar"
git tag 1.2.3

# upload code
git push
git push --tags
python3 setup.py build sdist
twine upload dist/kickoff-1.2.3.tar.gz

# upload documentation
log into readthedocs.io and trigger a Build
```
