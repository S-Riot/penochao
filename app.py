from flask import Flask

app = Flask(__name__)

@app.@app.route('/')
def hello():
    return 'App de penochao'

if __name__ == '__main__':
    app.run()
