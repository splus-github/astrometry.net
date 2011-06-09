from urllib2 import urlopen
from urllib2 import Request
from urllib import urlencode
from exceptions import Exception

from astrometry.net.api_util import json2python, python2json

class MalformedResponse(Exception):
	pass
class RequestError(Exception):
	pass


class Client(object):

	def __init__(self,
				 apiurl = 'http://oven.cosmo.fas.nyu.edu:9002/api/'):
		self.session = None
		self.apiurl = apiurl

	def get_url(self, service):
		return self.apiurl + service

	def send_request(self, service, args):
		'''
		service: string
		args: dict
		'''
		if self.session is not None:
			args += { 'session' : self.session }
		print 'Python:', args
		json = python2json(args)
		print 'Sending json:', json
		data = urlencode({'request-json': json})
		print 'Sending data:', data
		url = self.get_url(service)
		print 'Sending to URL:', url
		#f = urlopen(url, data)

		content_type = 'multipart/form-data; boundary=----------AaB03x'
		body = ['----------AaB03x',
			'Content-Disposition: form-data; name="request-json"',
			'',
			'{"apikey": "lzoszzpljmivlsqe"}',
			'----------AaB03x'
			]
		body = '\r\n'.join(body)
		print body
		request = Request(url=url,
    headers={'Content-Type':content_type},
    data=body)

		f = urlopen(request)
		txt = f.read()
		print 'Got json:', txt
		result = json2python(txt)
		print 'Got result:', result
		stat = result.get('status')
		print 'Got status:', stat
		if stat == 'error':
			errstr = result.get('errormessage', '(none)')
			raise RequestError('server error message: ' + errstr)
		return result

	def login(self, apikey):
		args = { 'apikey' : apikey }
		result = self.send_request('login', args)
		sess = result.get('session')
		print 'Got session:', sess
		if not sess:
			raise RequestError('no session in result')
		self.session = sess

	def upload(self, f):
		pass					

if __name__ == '__main__':
	c = Client()
	c.login('lzoszzpljmivlsqe')