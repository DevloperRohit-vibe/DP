# import rembg
# from PIL import Image
# import numpy as np
# import cv2

# image = Image.open("1img2.jpg")

# result = rembg.remove(image)
# image_bytes = result.tobytes()
# # nd1arr = np.frombuffer(image_bytes,dtype=np.uint8)
# imagestring = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
# print(imagestring)
# # # Image.SAVE("result.jpg",)
# # result.convert("RBG").save("output.jpg")

from flask import Flask,jsonify,request
from flask_cors import CORS
import os
import cv2
import numpy as np
from dotenv import load_dotenv
import base64

load_dotenv()

image_path = "image2.webp"

app = Flask(__name__)
CORS(app)
harcascade_file_name = os.environ.get("HAARCASCADE_FILE_NAME",False)


def process(image):
    cascade = cv2.data.haarcascades
    if harcascade_file_name:    
        cascade_xml_path = os.path.join(cascade, harcascade_file_name)
        if(os.path.exists(cascade_xml_path)):
            face_cascade = cv2.CascadeClassifier(cascade_xml_path)
            # image = cv2.imread(image_path)
            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
                )
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(500,500)
            )
            # print("faces",faces)
            for (x,y,w,h) in faces:
                print(x,y,w,h)
            # for (x,y,w,h) in face:
                cv2.rectangle(image,(x, y), (x+w,y+h), (0,255,0), 15)
            # cv2.imwrite("image.jpg",image)
            print("image saved")
            return image


def rotateImage(image) :
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return rotated_image

@app.route("/", methods=['POST'])
def opencv():
    try:

        if request.data :
            # print("b64string",b64string)
            raw_data = request.get_data(parse_form_data=True)
            data_url = raw_data.decode('utf-8')
            print("REQUEST RECEIVED")
            print("data_url",data_url[:50])
            prefixstr,b64string = data_url.split(",",1)
            b64bytes = base64.b64decode(b64string)
            np_1d_array = np.frombuffer(b64bytes, dtype=np.uint8)
            file_array = cv2.imdecode(np_1d_array,cv2.IMREAD_COLOR)
            roImgArr = rotateImage(file_array)

            sucess , imgenc = cv2.imencode('.jpg', roImgArr)
            if sucess:    
                print("imgenc",imgenc)
                base64_bytes = base64.b64encode(imgenc)
                # base64_bytes = base64.b64encode(cv2.imencode('.jpg', roImgArr)[1])
                print("base64_bytes",base64_bytes[:50])
                base64_string = base64_bytes.decode('utf-8')
                print(base64_string[:50])
                return jsonify({
                    "prefix": prefixstr,
                    "image": base64_string
                })

            # print(file_array)
            # image = process(file_array)
            # if len(image):
            #     # print(image)
            #     isDone, data = cv2.imencode('.jpg',image)
            #     b64_bytes = base64.b64encode(data)
            #     b64_string = b64_bytes.decode('utf-8')
            #     print(type(b64_bytes))
            #     print(type(b64_string))
            # return jsonify({
            #     "prefix": prefixstr,
            #     "image": b64_string
            # })

        
        return jsonify({
            "data": "not found"
        })



            
        # print(f" HaarCadcade abs Path : {os.path.abspath(cascade+haarcascadeFIle)}\n HaarCascade Path Rel : {cascade}")

    except Exception as e:
        print("e")

if __name__ == "__main__":
    print("server started..")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


# from flask import Flask, jsonify,request
# from flask_cors import CORS
# import os
# import cv2
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# # Loading haar cascade here

# CASCE_PATH = os.path.join(cv2.data.haarcascades,"haarcascade_frontalface_default.xml")

# print(CASCE_PATH)
# print(dir(cv2.CascadeClassifier))

# face_cascade = cv2.CascadeClassifier(CASCE_PATH)

# # Make sure the cascade actually loaded

# if face_cascade.empty():
#     raise RuntimeError(
#         f"Failed to load Haar Cascade from: {CASCE_PATH}"
#     )


# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({
#         "status": "online",
#         "service": "PhotoID Face Detection API"
#     })

# @app.route("/detect-face", methods=["POST"])
# def detect_face():
#     if "image" not in request.files:
#         return jsonify({
#             "success": False,
#             "error": "No image uploaded. Use field name 'image'."
#         }), 400

#     file = request.files["image"]
#     if file.filename == "":
#         return jsonify({
#             "success": False,
#             "error": "Empty filename."
#         }), 400

#     try:

#         image_bytes = file.read()
#         image_array = np.frombuffer(
#             image_bytes,
#             dtype=np.uint8
#         )

#         image = cv2.imdecode(
#             image_array,
#             cv2.IMREAD_COLOR
#         )

#         if image is None:
#             return jsonify({
#                 "success": False,
#                 "error": "Could not decode the uploaded image."
#             }), 400


#         # ------------------------------------------
#         # Convert to grayscale
#         # ------------------------------------------

#         gray = cv2.cvtColor(
#             image,
#             cv2.COLOR_BGR2GRAY
#         )


#         # ------------------------------------------
#         # Detect faces
#         # ------------------------------------------

#         faces = face_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.1,
#             minNeighbors=5,
#             minSize=(30, 30)
#         )


#         # ------------------------------------------
#         # Convert results to JSON
#         # ------------------------------------------

#         face_data = []

#         for index, (x, y, w, h) in enumerate(faces):

#             face_data.append({
#                 "id": index + 1,
#                 "x": int(x),
#                 "y": int(y),
#                 "width": int(w),
#                 "height": int(h)
#             })

#         print(face_data)
#         # ------------------------------------------
#         # Response
#         # ------------------------------------------

#         return jsonify({
#             "success": True,
#             "faces_detected": len(face_data),
#             "faces": face_data
#         })


#     except Exception as e:

#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

# @app.route('/api', methods=['GET'])
# def hello():
#     print(request)
#     return jsonify({'message': 'Hello, World!'})


# if __name__ == "__main__":
#     print("server started..")
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)