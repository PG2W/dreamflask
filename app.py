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
    dreammaker = DreamMaker()
    fileb64 = Conversion(content['file'])
    try:
        lr = float(content['lr'])
    except:
        lr = 0.002
    
    try:
        size = int(content['size'])
    except:
        size = 500

    try:
        noct = int(content['noct'])
    except:
        noct = 2
    
    try:
        nsublayer = int(content['nsublayer'])
    except:
        nsublayer = 41

    shit = fileb64.convToPng()
    shitdone = dreammaker.dream(shit, size=size, lr=lr, nOct=noct, nSubLayer=nsublayer)
    baseshit = fileb64.convToBase64(shitdone)
    return baseshit




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")