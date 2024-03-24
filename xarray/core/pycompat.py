from __future__ import annotations

from importlib import import_module, util
from typing import Any, Literal

import numpy as np
from packaging.version import Version

from .utils import is_duck_array

integer_types = (int, np.integer)

ModType = Literal["dask", "pint", "cupy", "sparse"]


class DuckArrayModule:
    """
    Solely for internal isinstance and version checks.

    Motivated by having to only import pint when required (as pint currently imports xarray)
    https://github.com/pydata/xarray/pull/5561#discussion_r664815718
    """

    module: ModType | None
    version: Version
    type: tuple[type[Any]]  # TODO: improve this? maybe Generic
    available: bool

    def __init__(self, mod: ModType) -> None:
        spec = util.find_spec(mod)
        self.module = None
        self.version = Version("0.0.0")
        self.type = ()
        self.available = spec is not None

    def load(self):
        if self.available and self.module is None:
            self.module = import_module(self.mod)
            self.version = Version(self.module.__version__)
            if self.mod == "dask":
                self.type = (import_module("dask.array").Array,)
            elif self.mod == "pint":
                self.type = (self.module.Quantity,)
            elif self.mod == "cupy":
                self.type = (self.module.ndarray,)
            elif self.mod == "sparse":
                self.type = (self.module.SparseArray,)
            else:
                raise NotImplementedError


dsk = DuckArrayModule("dask")
dask_version = dsk.version
dask_array_type = dsk.type

sp = DuckArrayModule("sparse")
sparse_array_type = sp.type
sparse_version = sp.version

cupy_array_type = DuckArrayModule("cupy").type


def is_dask_collection(x):
    if dsk.available:
        dsk.load()
        return import_module("dask.array").is_dask_collection(x)
    else:
        return False


def is_duck_dask_array(x):
    return is_duck_array(x) and is_dask_collection(x)
