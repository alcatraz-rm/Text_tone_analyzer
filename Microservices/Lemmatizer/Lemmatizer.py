from flask import Flask

application = Flask(__name__)


@application.route('/hello', methods=['GET'])
def hello():
    return 'hello'


application.run(debug=True)
