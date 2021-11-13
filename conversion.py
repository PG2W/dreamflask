import base64
from PIL import Image
from io import BytesIO
import uuid
import base64

class Conversion:
    def __init__(self, x:str):
        self.base64 = x

    def makeFiles(self): #Laver en ny 

        self.fileName = str(uuid.uuid4())  + '.txt'
        #print(self.fileName)

        f = open(self.fileName,"w+")

        self.strToTxt()

        

    def strToTxt(self):

        with open(self.fileName, "w") as text_file:
            text_file.write(self.base64)

        self.convToPng()

    def convToPng(self):
        
        # f = open(self.fileName, 'r')
        # data = f.read()
        # f.closed

        im = Image.open(BytesIO(base64.b64decode(self.base64)))
        print(im)
        #self.pic = im.save(self.fileName + '.png')
        return im


    def convToBase64(self, im):
        byte_io = BytesIO()
        im.save(byte_io, format='JPEG')
        my_string = base64.b64encode(byte_io.getvalue())
        return my_string
@classmethod
def convtob(im):
    mystring = str(base64.b64encode(im))
    return mystring