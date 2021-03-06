from tkinter.constants import DISABLED
import tkinter.filedialog as fd
import tensorflow as tf
import tkinter
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import cv2
import os
from mtcnn.mtcnn import MTCNN
import tensorflow
from tensorflow.keras.preprocessing import image
import numpy as np

# create a window
top = tkinter.Tk()


# set the title of the window
top.title("Fake Face Detection")

# set windows size
top.geometry("900x500")

# top.resizable(width=False, height=False)

# add a label
l = tkinter.Label(top, text="Fake Face Detection using Deep Learning", font=("Helvetica", 20)).pack(pady=20)

# variable to store filename 
filename = tkinter.StringVar()
# variable to store prediction result
result = tkinter.StringVar()

def select_file():
    fileName = fd.askopenfilename(initialdir = "/",title = "Select file",
    filetypes = (("mp4 files","*.mp4"),
    ("all files","*.*")))

    # assign filename
    filename.set(fileName)


# add button to the window with command to pick file and run the program
b = tkinter.Button(top, text="(1) - Select Video", command=select_file).pack(pady=10)

# display file name on the window
l = tkinter.Label(top, text="Video Path: ", font=("Helvetica", 12, 'bold')).pack()
l1 = tkinter.Label(top, textvariable=filename).pack()

# def extract_frames():

#     # load the video
#     cap = cv2.VideoCapture(filename.get())
#     # create a folder named faces
#     # if it does not exist
#     if not os.path.exists('faces'):
#         os.makedirs('faces')
#     # read the video
#     index = 0
#     while True:
#         # read the frame
#         ret, frames = cap.read()
#         # if the frame is empty
#         if not ret:
#             break

#         # save the face
#         cv2.imwrite('frames/'+str(index)+'.jpg', frames)
#         index += 1
#         top.update_idletasks()
#         print(index)

#     # close the video
#     cap.release()
#     # show done message
#     tkinter.Label(top, text="Frame Extracted").pack()


def extract_frames_and_faces():

    # load the video
    cap = cv2.VideoCapture(filename.get())
    # create a folder named faces
    # if it does not exist
    if not os.path.exists('frames'):
        os.makedirs('frames')
    # create a folder named faces
    # if it does not exist
    if not os.path.exists('faces'):
        os.makedirs('faces')


    # read the video
    index = 0
    while True:

        # show progress bar
        
        # read the frame
        ret, frames = cap.read()
        # if the frame is empty
        if not ret:
            break

        # save the frame
        cv2.imwrite('frames/'+str(index)+'.jpg', frames)
        index += 1

        # detect faces
        detector = MTCNN()
        faces = detector.detect_faces(frames)
        # if faces are detected
        if len(faces) > 0:
            for face in faces:
                # extract the face
                x, y, w, h = face['box']
                face_img = frames[y:y+h, x:x+w]
                # save the face
                cv2.imwrite('faces/'+str(index)+'.jpg', face_img)
                index += 1
            

    # close the video
    cap.release()
    # show done message
    if filename.get() != "":
        tkinter.Label(top, text="Face Extracted").pack()
    else:
        tkinter.Label(top, text="No Video Selected").pack()


def select_image():
    file_path = fd.askopenfilename(initialdir = "/",title = "Select file",
    filetypes = (("jpg files","*.jpg"),
    ("all files","*.*")))

    uploaded = Image.open(file_path)
    uploaded.thumbnail((200, 200))
    render = ImageTk.PhotoImage(uploaded)
    img = tkinter.Label(top, image=render)
    img.image = render
    img.place(x=550, y=200)
    classify_image(file_path);


def classify_image(file_path): 
    # load model
    model = tensorflow.keras.models.load_model('model/c_model.h5')
    # make prediction
    test_image = image.load_img(file_path, target_size=(150, 150, 3)) # this is a PIL image
    test_image_arr = image.img_to_array(test_image) # convert to array
    test_image_arr = np.expand_dims(test_image, axis=0) # add an axis to the array
    logits = model.predict(test_image_arr) # logits is the output of the model
    predictions = tf.nn.softmax(logits).numpy() # convert to numpy array
    
    if np.argmax(predictions) == 0:
        # result = "The selected image classified as Fake."
        # # assign to result
        # result.set(result)
        l = tkinter.Label(top, text="The selected image classified as Fake").pack()
        print("The selected image classified as Fake")

        
    else:
        # result = "The selected image classified as Real."
        # # assign to result
        # result.set(result)
        l = tkinter.Label(top, text="The selected image classified as Real").pack()
        print("The selected image classified as Real")




    
# display result
b1 = tkinter.Button(top, text="(2) - Extract Frames & Faces", command=extract_frames_and_faces).pack(pady=20)
b2 = tkinter.Button(top, text="(3) - Classify on Single Image", command=select_image).pack(pady=20)
b3 = tkinter.Button(top, text="(4) - Classify on Multiple Image").pack(pady=20)


top.mainloop()
