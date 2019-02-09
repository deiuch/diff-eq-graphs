from pip._internal import main
from importlib.util import find_spec

NOT_FOUND_MSG = 'Module {} was not found! Try to install it? [Y/n] '
NOT_INSTALLED_MSG = 'Module {} wan unable to be installed! Try again later!'


def install(*module_names):
    """
    Install all the given modules if they are not exist.
    :param module_names: List of module names to check and, if not exist, install
    :return If everything is installed - return 0, else - 1
    """
    for m_name in module_names:
        if not find_spec(m_name):
            if input(NOT_FOUND_MSG.format(m_name)).lower() not in 'Nn':
                if main(['install', m_name]):
                    print(NOT_INSTALLED_MSG.format(m_name))
                    return 1
            else:
                return 1
    return 0
