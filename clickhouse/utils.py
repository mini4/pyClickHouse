import re


def convert_classname_to_tablename(s):
    s = re.sub(r'([^_])([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def convert_tablename_to_classname(name):
    return ''.join((word.capitalize() for word in name.split('_')))


class _Unset:
    '''Object class needed to identify unset parameters of ORM objects'''

    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super().__new__(cls)
        return cls._inst

    def __bool__(self):
        return False

    def __repr__(self):
        return '<unset>'


unset = _Unset()
