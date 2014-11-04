Extranet.py
===========

A python library to interact with Unify's school management system.

## Installation

It is not in pypi yet, so you will have to clone this repo and build the
package.

```sh
python setup.py sdist
pip install -- dist/extranet*.tar.gz
```

## Usage

```python
>>> from extranet import Extranet
>>> e = Extranet(BASE_URL, login, password)
>>> e.get_timetable()
>>> ...
```

Feel free to send pull requests :)

