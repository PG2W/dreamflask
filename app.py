from flask import Flask, url_for, request
import json
from conversion import Conversion
from dream_maker import DreamMaker

app = Flask(__name__)

def convStepOne(fileb64):
    return fileb64 + "a"

@app.route('/api/dream', methods=['POST'])
def dreamimage():
    content = request.get_json()
    fileb64 = Conversion(content['file'])
    dreammaker = DreamMaker()
    shit = fileb64.convToPng()
    shitdone = dreammaker.dream(shit, size=50, nOct=1)
    print(shitdone)
    baseshit = fileb64.convToBase64(shitdone)
    return baseshit




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')