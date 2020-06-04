import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

cancer = datasets.load_breast_cancer()
#print(cancer.feature_names)
#print(cancer.target_names)

x = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.2)

#print(x_train,y_train)
classes = ['malignant','benign']
clf = svm.SVC(kernel="linear",C=2) #change the kernel type to change the model's accuracy
clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)
acc = metrics.accuracy_score(y_test,y_pred)
print("SVC: ",acc)

#compare with K nearest neighbors
kclf = KNeighborsClassifier(n_neighbors=11)
kclf.fit(x_train,y_train)
kacc = kclf.score(x_test,y_test) #calculate the model's accuracy
print("KNN: ",kacc)
