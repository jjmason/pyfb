from . import tornado, default

__adapter_module = None

def use_adapter( module ):
    global __adapter_module
    if isinstance( module, basestring ):
        __adapter_module = __import__( module )

def request_adapter( *args, **kwargs ):
    if __adapter_module is None: use_adapter( 'pyfb.adapters.default' )
    return __adapter_module.request_adapter( *args, **kwargs )

def client_adapter( *args, **kwargs ):
    if __adapter_module is None: use_adapter( 'pyfb.adapters.default' )
    return __adapter_module.client_adapter( *args, **kwargs )
