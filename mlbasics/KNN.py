import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data = pd.read_csv("car.data")

le = preprocessing.LabelEncoder() #process the data for the model by associating values to labels

#for each column turn the column into a list of integer values
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))

x = list(zip(buying, maint, door, persons, lug_boot, safety))  # features
y = list(cls)  # labels

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

model = KNeighborsClassifier(9) #9 neighbors accuracy will vary based on number of neighbora
model.fit(x_train,y_train) #train the model
acc = model.score(x_test,y_test) #calculate the model's accuracy
print(acc)

#test the model
predicted = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"] #accuracy ratings 0-3 respectively
for x in range(len(predicted)):
    print("Predicted: ", names[predicted[x]], "Data: ", x_test[x], "Actual: ", names[y_test[x]])
    n = model.kneighbors([x_test[x]],9)
    print("N: ", n) #print the results and the distance between all the neighbors in each group





