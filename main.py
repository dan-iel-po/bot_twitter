from flask import Flask, request, render_template, abort

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen/ttdm', methods=['POST'])
def ttdm_listen():
    if (request.method== 'POST'):
        print(request.json)
        return 'success', 200
    else:
        abort(400)