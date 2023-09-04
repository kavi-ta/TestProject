import requests
import cv2
from PIL import Image
import numpy as np
# fetch all data

def generate_final_image():
    data_url = "https://api.slingacademy.com/v1/sample-data/photos?offset=0&limit=132"
    # 
    data  = requests.get(data_url)
    data = data.json()
    # print(data)
    final_array = np.empty(shape=(32,32,3))
    # print(data["photos"])
    for test_data in data["photos"]:
        try:
        # test a single data from the url
            # print(test_data)
            image_url = test_data["url"]
        # test_img = requests.get(image_url, stream = True).raw

        # read , resize and save the image file
            img_response = Image.open(requests.get(image_url, stream = True).raw)
        except Exception as e :
            # if there is error in decoding replace the image tile with a blue image
            img_response = Image.new(mode="RGB", size=(32,32) , color=(0,0,255))
            print("here in exception")
        img_response = img_response.resize((32,32))

        id = test_data["id"]
        im1 = img_response.save(f"images/{id}.jpg")
        # img = cv2.imread(f"images/{id}.jpg", cv2.IMREAD_COLOR)
        # cv2.imshow("img",img)
        # cv2.waitKey(0)
        # cv2.destoryAllWindows()

        new_img = Image.open(f"images/{id}.jpg")
        array1 = np.array(new_img)
        final_array= np.vstack((final_array,array1))

        
        # reading and creating a single image
        # print(data)
    # print(final_array)
    img_new = Image.fromarray(final_array, 'RGB').save("final.jpg")