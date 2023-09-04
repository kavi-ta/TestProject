from sanic import Sanic
from sanic.response import text
import requests
from PIL import Image
import cv2
from test import *

app = Sanic("TestApp")

@app.get("/")
async def test(request):
    # generate_final_image()
    # generate the final image from test.py and send that as response
    return text("sending file")
 
 