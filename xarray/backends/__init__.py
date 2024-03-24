from importlib import util
"""Backend objects for saving and loading data

DataStores provide a uniform interface for saving and loading data in different
formats. They should not be used directly, but rather through Dataset objects.
"""
CfGribDataStore = _lazy_load_backend("cfgrib")
from .common import AbstractDataStore, BackendArray, BackendEntrypoint
from .file_manager import CachingFileManager, DummyFileManager, FileManager
H5NetCDFStore = _lazy_load_backend("h5netcdf")
from .memory import InMemoryDataStore
NetCDF4DataStore = _lazy_load_backend("netCDF4")
from .plugins import list_engines
PseudoNetCDFDataStore = _lazy_load_backend("pseudonetcdf")
PydapDataStore = _lazy_load_backend("pydap")
NioDataStore = _lazy_load_backend("pynio")
ScipyDataStore = _lazy_load_backend("scipy")
from .store import StoreBackendEntrypoint
ZarrStore = _lazy_load_backend("zarr")

def _lazy_load_backend(backend_name):
    """
    Lazily load a backend.

    Parameters
    ----------
    backend_name : str
        The name of the backend to load, e.g., 'scipy_'

    Returns
    -------
    A backend module if found, else raises ImportError
    """
    try:
        backend_module_name = f".{backend_name}_"
        spec = util.find_spec(backend_module_name, __name__)
        if spec is None:
            raise ImportError(f"Cannot import the backend: {backend_name}")
        backend_module = util.module_from_spec(spec)
        spec.loader.exec_module(backend_module)
        return backend_module
    except ImportError:
        raise RuntimeError(f"Required backend `{backend_name}` not installed.")

def get_available_backends():
    available_backends = []
    # Add code to populate 'available_backends' with names of backends that can be successfully imported using '_lazy_load_backend'
    backend_names = ["netCDF4", "scipy", "pydap", "h5netcdf", "cfgrib", "pseudonetcdf", "pynio", "zarr"]  # Add all backend names here
    for name in backend_names:
        try:
            _lazy_load_backend(name.lower())
            available_backends.append(name + "DataStore")
        except RuntimeError:
            continue
    return available_backends

__all__ = get_available_backends()
