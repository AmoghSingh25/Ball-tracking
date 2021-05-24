from flask import Flask, render_template, Response
from track import start

app=Flask(__name__)


@app.route('/')
def vid():
    return Response(start(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)