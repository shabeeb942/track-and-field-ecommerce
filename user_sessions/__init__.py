from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution


try:
    __version__ = get_distribution("django-user-sessions").version
except DistributionNotFound:
    # package is not installed
    __version__ = None
