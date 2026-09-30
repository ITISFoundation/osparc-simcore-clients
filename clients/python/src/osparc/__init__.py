import nest_asyncio2

from ._info import openapi as openapi
from ._version import __version__ as __version__
from .api import *  # noqa: F403

# APIs
from .exceptions import *  # noqa: F403
from .models import *  # noqa: F403

nest_asyncio2.apply()  # allow to run coroutines via asyncio.run(coro)
