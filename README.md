## Project Izyleaf Recommender
The project was conducted by 5 CentraleSupélec students: Abderrahmane, Eliott, Laure, Remy, and Elias, supervised by Wassila Ouerdane and the startup IzyLeaf. It aims to create a recommendation system utilizing neural networks, KNN, and clustering techniques. A report containing the state of the art, methodology, and results is available on the repository.
### Table of Contents

1. [Structure](#structure)
   1. [izyleaf-server](#izyleaf-server)
   2. [izyleaf-web](#izyleaf-web)
   3. [neuralnet-training](#neuralnet-training)
   4. [clustering](#clustering)
   5. [kNN](#knn)
2. [Clustering](#clustering-section)
3. [Izyleaf Test Suite](#izyleaf-test-suite)
   1. [Installation](#installation)

### Structure

The repository contains multiple folders and the report. Below, we provide a quick overview of each folder along with detailed instructions on how to run it and additional information.

#### izyleaf-server

This folder contains the server application.

#### izyleaf-web

This folder contains the Node.js web application. For more details, refer to the section "Izyleaf Test Suite."

#### neuralnet-training

This folder contains a Jupyter Notebook for training the model. We recommend running it in Google Colab, but you can also use it locally. Make sure to install the necessary packages mentioned in the first cell. Moreover, we have a small python snippet for how to use the model, inside of the notebook, and in another file is the recommendation function that was used in IzyleafTestSuite, which loads in the model from the filesystem and runs it on the data. If you take a look at izyleaf-server, you'll get a better idea of how to use it in an app. Because it needs to store the session vectors for each user (something we've done with TinyDB in the test suite but most databases can store arrays) and to run some preprocessing on all the car data (which can be ofcourse cached for better performance) before loading it into the model.


#### kNN

This folder contains the kNN model in a Jupyter notebook, the packages necessary for it to run are the ones imported in the first cell. Make sure to install them beforehand.

---

#### Clustering

In the folder named "Clustering," you will find the following files:

1. The folder named "Données bêta IzyLeaf" contains the dataset related to cars.
2. The Jupyter notebook "Clustering.ipynb" to select the characteristics of the clustering, perform the clustering analysis, and observe the results.
3. The file "requirement.txt" provides a list of all the necessary packages and their versions. You can install these packages by running the command `pip install -r requirement.txt`.

---

### Izyleaf Test Suite

#### Installation

1. Install Node.js (version 18.16 or later). This is necessary for the web application.
2. Install Python 3. This is for the Flask web server (we used Python because it integrates easily with TensorFlow).
3. Install the Node.js requirements:

```bash
cd izyleaf-web
npm install
```

4. Install the Python requirements:

```bash
cd izyleaf-server
pip install -r requirements.txt
```

5. Run the web application:

```bash
cd izyleaf-web
npm run start
```

6. Run the Python server:

```bash
cd izyleaf-server
python -m flask --debug run
```
