import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
from matplotlib import style
import pickle


data = pd.read_csv("student-mat.csv", sep=";")
data = data[["G1","G2","G3","studytime","failures","absences"]]

predict = "G3"

x = np.array(data.drop([predict],1))
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.1)

#Training model that creates pickle file comment out if training not needed
best = 0
for _ in range(30):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size=0.1)
    linear = linear_model.LinearRegression()
    linear.fit(x_train,y_train)
    acc = linear.score(x_test,y_test)
    print(acc)
    if acc > best:
        best = acc
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear,f)

#load data from before
pickle_in = open("studentmodel.pickle","rb")
linear = pickle.load(pickle_in)

print(f"m = {linear.coef_} \n"
      f"b = {linear.intercept_}")

predictions = linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

#plot the data
p = "G2"
style.use("ggplot")
pyplot.scatter(data[p],data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()

