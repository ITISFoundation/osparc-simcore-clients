import nest_asyncio
from ._version import __version__ as __version__
from ._exceptions import *  # noqa: F403
from .api import *  # noqa: F403

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)
