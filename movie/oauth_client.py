#coding:utf-8
import json
import re
import urllib
import urllib.parse
import urllib.request


class OAuth_Base():
    def __init__(self, kw):
        """self.oauth_type_id = kw.get('oauth_type_id', 0)
        self.oauth_type = kw.get('oauth_type', '')

        self.client_id = kw.get('client_id', '')
        self.client_secret = kw.get('client_secret', '')
        self.redirect_uri = kw.get('redirect_uri', '')
        self.scope = kw.get('scope', '')
        self.state = kw.get('state', '')

        self.url_authorize = kw.get('url_authorize', '')
        self.url_access_token = kw.get('url_access_token', '')
        self.url_open_id = kw.get('url_open_id', '')
        self.url_user_info = kw.get('url_user_info', '')
        self.url_email = kw.get('url_email', '')"""

        if not isinstance(kw, dict):
            raise Exception("arg is not dict type")

        for key, value in kw.items():
            setattr(self, key, value)

    def _get(self, url, data):
        request_url = '%s?%s' % (url, urllib.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def _post(self, url, data):
        request = urllib.request.Request(url, data=urllib.urlencode(data))
        response = urllib.request.urlopen(request)
        # response = urllib2.urlopen(url, urllib.urlencode(data))
        return response.read()

    def get_auth_url(self):
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': self.scope,
                  'state': self.state}
        return '%s?%s' % (self.url_authorize, urllib.urlencode(params))

    def get_access_token(self, code):
        pass

    def get_open_id(self):
        pass

    def get_user_info(self):
        pass

    def get_email(self):
        pass


class OAuth_Github(OAuth_Base):
    openid = ''

    def get_access_token(self, code):
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code,
                  'redirect_uri': self.redirect_uri}

        response = self._post(self.url_access_token, params)

        result = urllib.parse.parse_qs(response, True)
        self.access_token = result['access_token'][0]
        return self.access_token

    def get_open_id(self):
        if not self.openid:
            self.get_user_info()

        return self.openid

    def get_user_info(self):
        params = {'access_token': self.access_token, }
        response = self._get(self.url_user_info, params)

        result = json.loads(response)
        self.openid = result.get('id', '')
        return result

    def get_email(self):
        params = {'access_token': self.access_token, }
        response = self._get(self.url_email, params)

        result = json.loads(response)
        return result[0]['email']
