# import the necessary packages
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import cv2
import os
import lib
from datetime import date

def function(image_entered, name_entered):

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    #ap.add_argument("-n", "--name", required=True, help="patient name")
    #ap.add_argument("-i", "--image", required=True, help="image test")
    ap.add_argument("-t", "--trials", type=int, default=5, help="# of trials to run")
    args = vars(ap.parse_args())

    # define the path to the training and testing directories
    trainingPath = os.path.sep.join(["dataset", "training"])

    patientPath = os.path.sep.join(["dataset", name_entered])
    
    x = list(paths.list_images(patientPath))
    today = date.today()
    p1=patientPath+"/"+str(today)
    p = os.path.sep.join([p1, "{}.png".format(str(len(x)))])

    i=cv2.imread(image_entered)
    cv2.imwrite(p,i)

    # loading the training and testing data
    print("[INFO] loading data...")
    (trainFeatures, trainLabels) = lib.load_split(trainingPath)

    # encode the labels as integers 0:healthy, 1:parkinsons
    le = LabelEncoder()
    trainLabels = le.fit_transform(trainLabels)
    #testLabels = le.transform(testLabels)

    # initialize our trials dictionary
    trials = {}

    # loop over the number of trials to run
    for i in range(0, args["trials"]):
        # train the model
        print("[INFO] training model {} of {}...".format(i + 1,args["trials"]))
        model = RandomForestClassifier(n_estimators=100)
        model.fit(trainFeatures, trainLabels)
        metrics = {}

        # select last 4 images in the patient path
    patientPaths = list(paths.list_images(patientPath))
    y = len(patientPaths)
    z = 0
    if y > 4: z = y-4;
    idxs = np.arange(z, y)
    images = []
    print(z,y)

    # loop over the testing samples
    for i in idxs:
        # load the testing image, clone it, and resize it
        image = cv2.imread(patientPaths[i])
        output = image.copy()
        output = cv2.resize(output, (128, 128))

        #pre-process the image in the same manner we did earlier
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        img_date=os.path.split(patientPaths[i])
        liste=img_date[0].split("\\")
        # quantify the image and make predictions based on the extracted
        # features using the last trained Random Forest
        features = lib.quantify_image(image)
        preds = model.predict([features])
        label = le.inverse_transform(preds)[0]

        # draw the colored class label on the output image and add it to
        # the set of output images
        color = (0, 255, 0) if label == "healthy" else (0, 0, 255)
        cv2.putText(output, label, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            color, 2)
        cv2.putText(output, liste[2], (3, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            color, 2)
        images.append(output)

    # create a montage using 128x128 "tiles" with 1 row and 4 columns
    montage = build_montages(images, (140, 140), (4, 1))[0]

    # show the output montage
    cv2.imshow("Output", montage)
    cv2.waitKey(0)
