from flask import Flask,jsonify
from flask_cors import CORS
import os
import cv2
# from dotenv import load_dotenv

# load_dotenv()



app = Flask(__name__)
CORS(app)
harcascade_file_name = os.environ.get("HAARCASCADE_FILE_NAME",False)


@app.route("/", methods=['GET'])
def opencv():
    try:
        cascade = cv2.data.haarcascades
        if harcascade_file_name:    
            path = os.path.join(cascade, harcascade_file_name)
            if(os.path.exists(path)):
                return "exists"
        # print(f" HaarCadcade abs Path : {os.path.abspath(cascade+haarcascadeFIle)}\n HaarCascade Path Rel : {cascade}")

    except Exception as e:
        print(e)

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