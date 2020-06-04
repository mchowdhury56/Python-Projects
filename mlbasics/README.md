# Mlbasics

Below is a list of descriptions of each file:

student-mat.csv - Csv of student data used in LinearRegression.py

car.data - Car evaluation data set used in KNN.py

LinearRegression.py - Implementation of linear regression to predict students' final grades based on data in student-mat.csv. The script creates a pickle file after training the model which can be commented out if the pickle is already created. The results of regression are then plotted using pyplot from matplotlib.

KNN.py - Implementation of the K nearest neighbors algorithm to predict the the quality of cars in car.data based on the conditions of certain features of the car. The predictions are also compared to the actual quality of the car. The values of the dataset are processed into integer values that the model can use to train.

SVM.py - Implementation of a support vector machine to predict if a breast cancer tumor is malignant or benign based on the data provided by the breast cancer dataset from sklearn. The accuracy of the SVM is also compared with the KNN accuracy.

Kmeans.py - Implementation of the K Means algorithm to classify handwritten digits from sklearn's digits dataset. The bench_k_means function to score the model is taken from the sklearn website.
