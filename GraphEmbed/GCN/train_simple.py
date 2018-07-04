# -*- coding: UTF-8 -*-
#没有利用图结构，只利用X原来的特征
from __future__ import print_function

import keras
from keras.layers import Input, Dropout,  Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.regularizers import l2
from keras import backend as K
from layers.graph import GraphConvolution
from utils import *

import time

# Define parameters
DATASET = 'cora'
FILTER = 'MLP'
MAX_DEGREE = 2  # maximum polynomial degree  几阶邻居
SYM_NORM = True  # symmetric (True) vs. left-only (False) normalization
NB_EPOCH = 200
PATIENCE = 10  # early stopping patience

# Get data
X, A, y = load_data(dataset=DATASET)
y_train, y_val, y_test, idx_train, idx_val, idx_test, train_mask = get_splits(y)



# Normalize X
X /= X.sum(1).reshape(-1, 1)

if FILTER == 'MLP':
    print('Using MLP filters...')
    A_ = preprocess_adj(A, SYM_NORM)   #处理过的A_是D-0.5 A D-0.5

else:
    raise Exception('Invalid filter type.')


X_in = Input(shape=(X.shape[1],))  #一个节点有1433 features.，所以输入形状就是X.shape[1]，

H = Dropout(0.5)(X_in)
H = Dense(16 , activation='relu', kernel_regularizer=l2(5e-4))(H)
H = Dropout(0.5)(H)
Y = Dense(y.shape[1] , activation='softmax')(H)

# Compile model
#  keras函数式模型（区别于序贯模型）  可构造拥有多输入和多输出的模型  如 model = Model(inputs=[a1, a2], outputs=[b1, b3, b3])
model = Model(inputs= X_in, outputs=Y)
model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.01))

# Helper variables for main training loop
wait = 0
preds = None
best_val_loss = 99999

# Fit
for epoch in range(1, NB_EPOCH+1):
    t = time.time()
    model.fit(X, y_train, sample_weight=train_mask, batch_size=A.shape[0], epochs=1, shuffle=False, verbose=0)

    # Predict on full dataset
    preds = model.predict(X, batch_size=A.shape[0])

    # Train / validation scores
    train_val_loss, train_val_acc = evaluate_preds(preds, [y_train, y_val],
                                                   [idx_train, idx_val])
    print("Epoch: {:04d}".format(epoch),
          "train_loss= {:.4f}".format(train_val_loss[0]),
          "train_acc= {:.4f}".format(train_val_acc[0]),
          "val_loss= {:.4f}".format(train_val_loss[1]),
          "val_acc= {:.4f}".format(train_val_acc[1]),
          "time= {:.4f}".format(time.time() - t))

    # Early stopping
    if train_val_loss[1] < best_val_loss:
        best_val_loss = train_val_loss[1]
        wait = 0
    else:
        if wait >= PATIENCE:
            print('Epoch {}: early stopping'.format(epoch))
            break
        wait += 1

# Testing
test_loss, test_acc = evaluate_preds(preds, [y_test], [idx_test])
print("Test set results:",
      "loss= {:.4f}".format(test_loss[0]),
      "accuracy= {:.4f}".format(test_acc[0]))
