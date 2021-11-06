import csv
import os

from flowprint.flowprint import FlowPrint
from flowprint.preprocessor import Preprocessor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def loadFiles():
    preprocessor = Preprocessor(verbose=True)
    X, y = preprocessor.load('./flows.p')
    return X, y


def readFiles():
    dir = "/home/jhiggs/Downloads/pcap/us/android"

    # Create Preprocessor object
    preprocessor = Preprocessor(verbose=True)
    # Create Flows and labels
    listOfFiles = list()
    for filename in os.listdir(dir):
        listOfFiles.append("{}/{}".format(dir, filename))

    X, y = preprocessor.process(listOfFiles, listOfFiles)
    # Save flows and labels to file 'flows.p'
    preprocessor.save('flows.p', X, y)

    return X, y
    # Load flows from file 'flows.p'


if __name__ == "__main__":

    f = open("datasets/Source.csv", "w")
    f.truncate()
    f.close()

    if os.path.exists("./flows.p"):
        X,y = loadFiles()
    else:
        X,y = readFiles()


    for x in range(2):
        print("iteration {}".format(x))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5)

        # Create FlowPrint object
        flowprint = FlowPrint(
            batch       = 300,
            window      = 30,
            correlation = 0.1,
            similarity  = 0.9
        )

        # Fit FlowPrint with flows and labels
        flowprint.fit(X_train, y_train)

        # Create fingerprints for test data
        fp_test = flowprint.fingerprint(X_test)
        # Predict best matching fingerprints for each test fingerprint
        y_pred = flowprint.predict(fp_test)

        # # Store fingerprints to file 'fingerprints.json'
        # flowprint.save('fingerprints.json')
        # # Load fingerprints from file 'fingerprints.json'
        # # This returns both the fingerprints and stores them in the flowprint object
        # fingerprints = flowprint.load('./fingerprints.json')


        # Create FlowPrint object
        flowprint = FlowPrint(
            batch       = 300,
            window      = 30,
            correlation = 0.1,
            similarity  = 0.9
        )

        # Fit FlowPrint with flows and labels
        flowprint.fit(X_train, y_train)

        # Recognise which app produced each flow
        y_recognize = flowprint.recognize(fp_test)
        # Detect previously unseen apps
        # +1 if a flow belongs to a known app, -1 if a flow belongs to an unknown app
        y_detect    = flowprint.detect(fp_test)

        # Print report with 4 digit precision
        report = classification_report(y_test, y_recognize, digits=4, output_dict=True)

        with open('datasets/Source.csv', 'a', newline='') as csvfile:
            fieldNames = ['accuracy/recall', 'precision', 'f1-score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
            if x == 0:
                writer.writeheader()
            writer.writerow({'accuracy/recall': report['accuracy'], 'precision': report['weighted avg']['precision'],
                            'f1-score': report['weighted avg']['f1-score']})


