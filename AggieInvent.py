import functools
import time
from flask import Flask, jsonify, Response

app = Flask(__name__)


def returns_content_type(mime_type):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            content, code = f(*args, **kwargs)
            return Response(content, code, mimetype=mime_type)
        return decorated_function
    return decorator

## System functionality
# No auth
@app.route('/')
def index():
  return 'Open Sesame device gateway'

# No auth for easy integration with monitoring tools/services
@app.route('/status')
def system_status():

    def door_data(doorid):
        status = 200
        last_seen = time.time()
        return { 'status': status, 'last_seen': last_seen }

    details = {
        'doors': { doorid: door_data(doorid) for doorid in [1] }
    }

    return jsonify(details), 200


## Door functionality
@app.route('/doors/<doorid>/unlock', methods=['POST'])
@returns_content_type('text/plain')
# @require_basic_auth
def door_unlock(doorid):
    #TODO: Unlock door


    return ('Door is now unlocked', 200)


@app.route('/doors/<doorid>/lock', methods=['POST'])
@returns_content_type('text/plain')
# @require_basic_auth
def door_lock(doorid):
    #TODO: lock door


    return ('Door is now locked', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=False)
