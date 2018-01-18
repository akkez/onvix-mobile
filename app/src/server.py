import json
import requests
from flask import Flask, session, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')
CORS(app, supports_credentials=True)
sessions = dict()

def default_session():
	s = requests.Session()
	s.headers.update({
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
		'Origin': 'https://onvix.tv',
	})
	return s


def current_session(session):
	if 'email' not in session or session['email'] not in sessions:
		raise ApiException("Unauthorized")
	return sessions[session['email']]


@app.route('/api/auth', methods=['POST'])
def ovnix_auth():
	data = request.get_json()
	login = data.get('login', '')
	password = data.get('password', '')
	session['email'] = login

	sess = default_session()
	r = sess.post('https://onvix.tv/users/sign_in', data={
		'user[email]': login,
		'user[password]': password,
		'user[remember_me]': 'true'
	}, allow_redirects=False)
	sessions[login] = sess
	return jsonify(success='user_id' in r.text)


@app.route('/api/status')
def profile():
	sess = current_session(session)

	r = sess.get('https://onvix.tv/profile.json')
	profile = json.loads(r.text)
	r = sess.get('https://onvix.tv/api/v1/home.json')
	shows = json.loads(r.text)['watch_now']
	my_shows = [dict(
		title='{} ({})'.format(i['title_ru'], i['title_en']),
		token=i['token'], id=i['id'],
		poster='https://onvix.tv{}'.format(i['poster']['medium']),
		type=i['type']
	) for i in shows]

	return jsonify(email=profile['email'], days_remaining=profile['subscription_days'], raw=profile, shows=my_shows)


@app.route('/api/show/<string:type>/<string:show_id>')
def show(show_id, type):
	sess = current_session(session)

	r = sess.get('https://onvix.tv/{type}/{id}.json'.format(id=show_id, type=dict(
		movie='movies', serial='serials'
	).get(type)))
	show = json.loads(r.text)

	return jsonify(show)


def _play_media(session, api_params):
	r = session.get(**api_params)
	show = json.loads(r.text)
	if 'media_files' not in show:
		raise ApiException('Failed to fetch media')
	hls_url = show['media_files']['hls']
	if hls_url[:4] != 'http':
		hls_url = 'https:{}'.format(hls_url)
	r = session.get(hls_url)
	lines = filter(lambda x: x[:4] == 'http', r.text.splitlines())
	return jsonify(media=show['media_files'], stream_urls=list(lines))


@app.route('/api/play_movie/<string:show>/<string:stream>')
def play_movie(show, stream):
	sess = current_session(session)
	movie_url = 'https://onvix.tv/api/v1/streaming/movies/{show}/{stream}'.format(show=show, stream=stream)
	return _play_media(sess, dict(url=movie_url))


@app.route('/api/play_serial/<string:show>/<string:stream>/<int:season>/<int:episode>')
def play_serial(show, stream, season, episode):
	sess = current_session(session)
	serial_url = 'https://onvix.tv/api/v1/streaming/serials/{show}/{stream}'.format(show=show, stream=stream)
	return _play_media(sess, dict(url=serial_url, params=dict(episode=episode, season=season)))


class ApiException(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['success'] = False
		rv['message'] = self.message
		return rv


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

