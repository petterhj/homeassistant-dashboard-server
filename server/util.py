# https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/tasks.py
from __future__ import annotations

import asyncio
import logging
from asyncio import ensure_future
from functools import wraps
from pathlib import Path
from traceback import format_exception
from typing import Any, Callable, Coroutine, Union

from starlette.concurrency import run_in_threadpool
from PIL import Image


NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[Any, Any, None]]
NoArgsNoReturnDecorator = Callable[
    [Union[NoArgsNoReturnFuncT, NoArgsNoReturnAsyncFuncT]],
    NoArgsNoReturnAsyncFuncT,
]


def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    logger: logging.Logger | None = None,
    raise_exceptions: bool = False,
    max_repetitions: int | None = None,
) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is periodically re-executed after its first call.

    The function it decorates should accept no arguments and return nothing. If necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior to decoration.

    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: bool (default False)
        If True, the function will wait for a single period before the first call
    logger: Optional[logging.Logger] (default None)
        The logger to use to log any exceptions raised by calls to the decorated function.
        If not provided, exceptions will not be logged by this function (though they may be handled by the event loop).
    raise_exceptions: bool (default False)
        If True, errors raised by the decorated function will be raised to the event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to repeat.
        See https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler for more info.
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`, the function is repeated forever.
    """

    def decorator(
        func: NoArgsNoReturnAsyncFuncT | NoArgsNoReturnFuncT,
    ) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called version of itself.
        """
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                if wait_first:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if is_coroutine:
                            await func()  # type: ignore
                        else:
                            await run_in_threadpool(func)
                        repetitions += 1
                    except Exception as exc:
                        if logger is not None:
                            formatted_exception = "".join(
                                format_exception(
                                    type(exc), exc, exc.__traceback__
                                )
                            )
                            logger.error(formatted_exception)
                        if raise_exceptions:
                            raise exc
                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator


def get_bit_depth(image: Image.Image) -> int:
    """Calculate bit depth from PIL image mode and format."""
    mode = image.mode

    # Common mode mappings
    mode_depths = {
        '1': 1,          # 1-bit pixels, black and white
        'L': 8,          # 8-bit pixels, grayscale
        'P': 8,          # 8-bit pixels, mapped to other mode using palette
        'RGB': 24,       # 3x8-bit pixels, true color
        'RGBA': 32,      # 4x8-bit pixels, true color with transparency
        'CMYK': 32,      # 4x8-bit pixels, color separation
        'YCbCr': 24,     # 3x8-bit pixels, color video format
        'LAB': 24,       # 3x8-bit pixels, L*a*b* color space
        'HSV': 24,       # 3x8-bit pixels, Hue, Saturation, Value color space
        'LA': 16,        # L with alpha
        'PA': 16,        # P with alpha
    }

    # Check for 16-bit modes
    if mode in ['I', 'F']:  # 32-bit signed integer or 32-bit floating point
        return 32
    elif mode == 'I;16':    # 16-bit unsigned integer
        return 16

    return mode_depths.get(mode, 8)  # Default to 8-bit


def get_image_details(image_path: Path) -> dict[str, Any]:
    """Get detailed information about an image file."""
    with Image.open(image_path) as image:
        details = {
            "file_size": image_path.stat().st_size,
            "mime_type": Image.MIME.get(image.format),
            "resolution": image.size,
            "mode": image.mode,
            "bit_depth": get_bit_depth(image),
            "has_transparency": 'transparency' in image.info or image.mode in ['RGBA', 'LA', 'PA'],
            "palette_size": len(image.getpalette()) // 3 if image.mode == 'P' else None,
            "compression": image.info.get('compression'),
        }
    return details
