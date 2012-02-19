'''
Adapters for the tornado server.
''' 
from . import base
from . import default
from pyfb import minitwisted
import tornado.httpclient as httpclient
import urllib

class Client( base.HTTPClientAdapter ): 
    def request_async( self, url, method = 'GET', params = None ):
        d = minitwisted.defer.Deferred()
        kwargs = {}
        body, url = self._prepare_request( url, method, params )
        if body: kwargs['body'] = body
        kwargs['method'] = method
        client = httpclient.AsyncHTTPClient()
        def callback( response ):
            d.callback( ( response.body, response.code ) )
            
        client.fetch( url, callback, **kwargs )          
        return d

def request_adapter( request, session = None, *args, **kwargs ):
    return default.request_adapter( request.arguments, request.cookies, session )

def client_adapter( *args, **kwargs ):
    return Client()

__all__ = ['request_adapter', 'client_adapter', 'ClientAdapter']
