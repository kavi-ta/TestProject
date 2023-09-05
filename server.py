from sanic import Sanic
import requests
from PIL import Image
import cv2
import numpy as np
from sanic.response import file



app = Sanic("TestApp")

@app.get("/")
async def test(request):
    # maintains an array for all the image values for concatenating them at the end
    image_data = []
    # fetch all the data
    data_url = "https://api.slingacademy.com/v1/sample-data/photos?offset=0&limit=132"
    data  = requests.get(data_url).json()

    # iterate all the photos 
    for current_data in data["photos"]:
        current_img_url = current_data["url"]

        fetch_error = False
        try:
            # try fetching the image from url
            fetch_image_from_url = requests.get(current_img_url, stream = True).raw
        except Exception as e:
            # if error in fetching => represent a black image
            image = np.zeros((512, 512, 1), dtype = "uint8")
            # set fetch_error =  True to avoid running into the next exception
            fetch_error = True

        try:
            # check if there was no fetching_error
            assert fetch_error == False
            # decode the image_data
            arr = np.asarray(bytearray(fetch_image_from_url.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)
            # resize the image to 32x32 
            image = cv2.resize(image,(32,32))
        except Exception as e:
            # check if exception was caused due to decoding error and not fetching_error
            if fetch_error == False:
                image = np.full((32, 32, 3), (255,0, 0), np.uint8)
        # append the image vector in the image_data list
        image_data.append(image)
    # concatenate ver
    concatenated_image = cv2.vconcat(image_data)
    # finally write the image in a file and serve the file
    cv2.imwrite("generatedimage.jpg", concatenated_image)
    return await file("generatedimage.jpg")
 
 