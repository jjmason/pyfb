'''
Facebook implementation
created Feb 18, 2012
''' 
import pyfb.adapters
from launchpadlib.credentials import access_token_page
import urllib
from twisted.web.http import urlparse
from cgi import parse_qs
from pyfb import minitwisted
import base64
class FacebookException( Exception ):pass
def _b64_url_decode( s ):
    #Pad it
    while len( s ) % 4 != 0: s += '='
    #Replace _ with / and - with +
    s = s.replace( '_', '/' ).replace( '-', '+' )
    return base64.b64decode( s )

class Facebook( object ):
    def __init__( self, app_id, app_secret, request, client ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.request = request
        self.client = client 
        session = request.session()
        self.is_session_real = session is not None
        self.session = session or {}
        
    def access_token( self, redirect_uri = None ):
        access_token = self._quick_access_token()
        if access_token: return access_token
        code = self.code()
        if code:
            url, params = self._prepare_access_token_request( code, redirect_uri )
            body, status = self.client.request( url, params = params )
            if status == 200:
                response = parse_qs( body )
                if 'access_token' in response:
                    self._access_token = response['_access_token']
                    return self._access_token
            else:
                raise FacebookException( 'request for access_code returned error %s' % ( status ) )
            
        self._access_token = None
        
    def _quick_access_token( self ):
        try:return self._access_token
        except AttributeError: pass 
        signed_request = self.signed_request()
        if signed_request and 'oauth_token' in signed_request:
            self._access_token = signed_request['oauth_token']
            return self._access_token
        
    def access_token_async( self, redirect_uri = None ):
        d = minitwisted.defer.Deferred()
        access_token = self._quick_access_token()
        if access_token: return d.callback( access_token )
        code = self.code()
        if code:
            url, params = self._prepare_access_token_request( code, redirect_uri )
            def callback( result ):
                body, status = result
                if status != 200:
                    d.errback( FacebookException( 'request for access token returned status %s' % ( status ) ) )
                resp = parse_qs( body )
                self._access_token = resp.get( 'access_token', None ) 
                d.callback( self._access_token )
            
            r = self.client.request_async( url, params = params )
            r.addBoth( callback, d.errback )
        else:
            self._access_token = None
            d.callback( None )
        return d
    
    def user( self ):
        pass
    
    def user_async( self ):
        pass
    
    def signed_request( self ):
        try: return self._signed_request
        except AttributeError:pass
        sr = self.request.param( 'signed_request' )
        if not sr:
            sr = self.request.cookie( 'fbsr_%s' % self.app_id )
        if not sr:
            self._signed_request = None
            return 
        sig, payload = sr.split( '.', 2 )
        sig = _b64_url_decode( sig )
        
    
    def code( self ):
        try: return self._code
        except AttributeError: pass
        sr = self.signed_request()
        if sr and 'code' in sr:
            self._code = sr['code']
        #TODO: XSRF protection
        self._code = self.request.param( 'code' )
        return self._code
