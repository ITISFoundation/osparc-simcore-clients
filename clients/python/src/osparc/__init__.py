import nest_asyncio
from ._version import __version__ as __version__

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)
