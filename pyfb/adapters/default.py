from .base import HTTPClientAdapter, HTTPRequestAdapter
import urllib2, urllib

class Client( HTTPClientAdapter ):
    '''
    Default http client implementation.  Makes synchronous requests
    with urllib2
    '''
    def request( self, url, method = 'GET', params = None ):
        opener = urllib2.build_opener()
        url, data = self._prepare_request( url, method, params )        
        request = urllib2.Request( url, data ) 
        request.get_method = lambda : method
        resp = opener.open( request )
        return ( resp.read(), resp.status )
    
    def _prepare_request( self, url, method, params ):
        method = method.upper()
        data = None
        if params:
            if method in ['POST', 'PUT']:
                data = urllib.urlencode( params )
            else:
                url += "?" + urllib.urlencode( params )
        return data, url
    
class Request( HTTPRequestAdapter ):
    """
    A simple dictionary based request adapter.
    """
    def __init__( self, params, cookies, session = None ):
        '''
        @param params: dict of params, values are strings or lists of strings
        @param cookies: dict of cookies
        @param session: dict like session object, or None if a session is not available.
        '''
        self.params = params
        self.cookies = cookies
        self._session = session
        
    def param( self, name, default = None ):
        if not self.params or name not in self.params: 
            return default
        value = self.params[name]
        if isinstance( value, list ):
            if len( value ): value = value[0]
            else: value = None
        return value
    
    def cookie( self, name, default = None ):
        if not self.cookies or name not in self.cookies: return default
        return self.cookies[name]
    
    def session( self ):
        return self._session

def request_adapter( params, cookies, session = None, *args, **kwargs ):
    return Request( params, cookies, session )

def client_adapter( *args, **kwargs ):
    return Client()

__all__ = ['Request', 'Client', 'request_adapter', 'client_adapter']
