import re


def convert_classname_to_tablename(name: str) -> str:
    '''
    Converts a class name to a table name.

    Args:
        name: The class name.

    Returns:
        The table name in snakecase format.

    '''
    tbl_name = re.sub(r'([^_])([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', tbl_name).lower()


def convert_tablename_to_classname(name: str) -> str:
    '''
    Converts a table name to a class name.

    Args:
        name: The table name.

    Returns:
        The class name in camelcase format.

    '''
    return ''.join((word.capitalize() for word in name.split('_')))


class _Unset:
    '''
    Object class needed to identify unset properties of ORM objects

    '''

    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super().__new__(cls)
        return cls._inst

    def __bool__(self):
        return False

    def __repr__(self):
        return '<unset>'


unset = _Unset()
'The object to identify unset class properties and method parameters.'
