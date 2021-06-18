from numpy import asarray
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from math import ceil
import os
from PIL import Image
Categories = ["butterfly", "cat", "chicken", "cow", "dog", "elephant", "horse", "sheep", "spider", "squirrel"]
ratio = 0.85
image_size = (25, 25)
train_labels = np.array([], dtype=int)
train_images = np.array([])
test_labels = np.array([], dtype=int)
test_images = np.array([])
train_images = np.reshape(train_images, (-1,25,25,3))
test_images = np.reshape(test_images, (-1,25,25,3))
for path in Categories:
    os.chdir(path)
    filenames = os.listdir(path=".")
    N_train = ceil(len(os.listdir())*ratio)
    count = 0
    for filename in filenames:
        i = Categories.index(path)
        count += 1
        image = Image.open(filename)
        image = image.resize(image_size)
        image = image.convert('RGB')
        next_img = asarray(image)
        next_img = np.reshape(next_img, (-1,25,25,3))
        '''
        if count < 700:
            train_labels = np.append(train_labels, i)
            train_images = np.append(train_images, next_img, 0)
        elif count >= 700 and count < 750:
            test_labels = np.append(test_labels, i)
            test_images = np.append(test_images, next_img, 0)
        else:
            break
        '''
        if count <= N_train: 
            train_labels = np.append(train_labels, i)
            train_images = np.append(train_images, next_img, 0)
        else:
            test_labels = np.append(test_labels, i)
            test_images = np.append(test_images, next_img, 0)
        
    os.chdir("..")
train_images = train_images/255
test_images = test_images/255
model=keras.Sequential([keras.layers.Conv2D(32, 3, padding='same', activation='relu', input_shape=(25,25,3)),
                        keras.layers.Flatten(),
                        #keras.layers.Dense(90000,input_dim=270000,activation='relu'),
                        #keras.layers.Dense(1875, input_shape=(25, 25, 3), activation='relu'),
                        keras.layers.Dense(1500, activation='relu'),
                        keras.layers.Dense(1200, activation='relu'),
                        keras.layers.Dense(1000, activation='relu'),
                        keras.layers.Dense(800, activation='relu'),
                        #keras.layers.Dropout(0.1),
                        keras.layers.Dense(500, activation='relu'),
                        #keras.layers.Dense(1000, activation='relu'),
                        keras.layers.Dense(400, activation='relu'),
                        keras.layers.Dense(300, activation='relu'),
                        keras.layers.Dense(200, activation='relu'),
                        keras.layers.Dense(100, activation='relu'),
                        keras.layers.Dense(50, activation='relu'),
                        #keras.layers.Dense(10, activation='relu'),
                        keras.layers.Dense(10, activation='softmax')
                       ])           
model.compile(optimizer='Adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images,train_labels,
        epochs = 10,
        validation_split = 0,
        verbose = 2
        )
test_loss,test_acc=model.evaluate(test_images,test_labels)
print("Доля верных ответов на тестовых данных",round(test_acc*100,6))
predication=model.predict(test_images)
pred_y=[]
for x in predication:
  m=max(x)
  for i in range(len(x)):
    if x[i]==m:
      pred_y+=[i]
y_actu = pd.Series(test_labels, name='Actual')
y_pred = pd.Series(pred_y, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
print(df_confusion)
'''
0   "butterfly"
1   "cat"
2   "chicken"
3   "cow"
4   "dog"
5   "elephant"
6   "horse"
7   "sheep"
8   "spider"
9   "squirrel"
'''