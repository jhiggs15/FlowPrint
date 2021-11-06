import os

from flowprint.flowprint import FlowPrint
from flowprint.preprocessor import Preprocessor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


if __name__ == "__main__":
    dir = "/home/jhiggs/Downloads/pcap/us/android"

    # Create Preprocessor object
    preprocessor = Preprocessor(verbose=True)
    # Create Flows and labels
    listOfFiles = list()
    for filename in os.listdir(dir):
        listOfFiles.append("{}/{}".format(dir, filename))

    X, y = preprocessor.process(listOfFiles, listOfFiles)

    # # Save flows and labels to file 'flows.p'
    # preprocessor.save('flows.p', X, y)
    # # Load flows from file 'flows.p'
    # X, y = preprocessor.load('./flows.p')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

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

    print("here")
    # Print report with 4 digit precision
    print(classification_report(y_test, y_recognize, digits=4))