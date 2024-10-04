import nest_asyncio
from ._version import __version__ as __version__

# APIs
from .exceptions import *  # noqa: F403
from .models import *  # noqa: F403
from .api import *  # noqa: F403

from ._info import openapi as openapi

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)
