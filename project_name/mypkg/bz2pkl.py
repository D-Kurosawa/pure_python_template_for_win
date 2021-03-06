"""Compress and decompress pickle

compress:   convert pickle to bz2
decompress: convert bz2 to pickle
"""
import bz2
import pickle
from pathlib import Path
from typing import Any
from typing import Union


def loads(compress_obj: Any) -> Any:
    try:
        decompress = bz2.decompress(compress_obj)
    except OSError:
        try:
            return pickle.loads(compress_obj)
        except Exception:
            raise IOError(f"object <{compress_obj}> is not pickle object")
    else:
        return pickle.loads(decompress)


def dumps(obj: Any, compress: bool = True, compress_level: int = 1) -> Any:
    pkl = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    if compress:
        return bz2.compress(pkl, compresslevel=compress_level)
    else:
        return pkl


def load(file: Union[str, Path]) -> Any:
    if not Path(file).exists():
        raise FileNotFoundError(file)

    try:
        with bz2.BZ2File(file, "rb") as f:
            pkl = f.read()
    except OSError:
        try:
            with open(file, "rb") as f:
                return pickle.load(f)
        except Exception:
            raise IOError(f"file <{file}> can not read to pickle object")
    else:
        return pickle.loads(pkl)


def dump(
    obj: Any, file: Union[str, Path], compress: bool = True, compress_level: int = 1
):
    if compress:
        with bz2.BZ2File(file, "wb", compresslevel=compress_level) as f:
            f.write(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
    else:
        with open(file, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    pass
