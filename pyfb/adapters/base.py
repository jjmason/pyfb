'''
<LICENCE>
Adapters for various web frameworks.
'''  
from pyfb import minitwisted
class HTTPRequestAdapter( object ):
    '''
    Wraps an http request of some sort.
    '''
    def cookie( self, name, default = None ):
        """Get the value of a cookie, or None if the cookie is not present."""
        raise NotImplemented
    
    def param( self, name, default = None ):
        """
        Get the value of a request parameter as a string.  Generally, we're 
        not interested in multi-value parameters, and in that case an implementation
        can just return the first value. 
        *** The return value must be urldecoded! ***
        """
        raise NotImplemented 
     
    def session( self ):
        """
        Return a dictionary like session object.  If it doesn't make sense
        to have a session for whatever reason, this method should return None.
        """
        return None
    
class HTTPClientAdapter( object ):
    '''
    Wraps an http client of some sort.
    '''
    
    def request( self, url, method = 'get', params = None ):
        """
        Make a synchronous HTTP request.
        @param url: The url to request
        @param method: The HTTP method.
        @param params: A dict like object containing request parameters.
        @return: A ( body, status ) tuple, where body is a string or an object
                with a read method, and status is an int. 
        """
        raise NotImplemented
    
    def request_async( self, url, method = 'get', params = None ):
        """
        Make an aysnchronous HTTP request.  The default implementation just uses the
        `request` method. 
        
        @param url: The url to request
        @param method: The HTTP method.
        @param params: A dict like object containing request parameters.
        @return: A `minitwisted.defer.Deferred
        """
        d = minitwisted.defer.Deferred()
        try:
            d.callback( *self.request( url, method, params ) )
        except Exception as e:
            d.errback( e ) 
        return d

 
    
