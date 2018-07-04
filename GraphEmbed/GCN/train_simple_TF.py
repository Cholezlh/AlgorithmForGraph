# -*- coding: UTF-8 -*-
#只用原始向量，没用图向量
#2000 test_arruracy: 0.389

from __future__ import print_function

import keras
from keras.layers import Input, Dropout,  Dense, Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.regularizers import l2
from keras import backend as K
from layers.graph import GraphConvolution
from utils import *
import tensorflow as tf
import time

# Define parameters
DATASET = 'cora'
NB_EPOCH = 2000
PATIENCE = 10  # early stopping patience

# Get data
X, A, y = load_data(dataset=DATASET)

idx_train = range(500)
idx_test = range(500, 1500)
y_train = np.zeros(y.shape, dtype=np.int32)
y_test = np.zeros(y.shape, dtype=np.int32)
y_train[idx_train] = y[idx_train]
y_test[idx_test] = y[idx_test]
train_mask = sample_mask(idx_train, y.shape[0])
test_mask = sample_mask(idx_test, y.shape[0])

# Normalize X
X /= X.sum(1).reshape(-1, 1)

weight = {
    'h1': tf.Variable(tf.random_normal([1433, 16])),
    'out': tf.Variable(tf.random_normal([16, 7]))
}
bias = {
    'h1': tf.Variable(tf.random_normal([16])),
    'out': tf.Variable(tf.random_normal([7]))
}


X_in = tf.placeholder('float', shape =[None, 1433])
y_ = tf.placeholder('float', shape = [None, 7])
keep_prob = tf.placeholder(tf.float32)

X_in= tf.nn.dropout(X_in, keep_prob=0.5)
layer1 = tf.matmul(X_in, weight['h1']) + bias['h1']
layer1 = tf.nn.relu(layer1)
layer1= tf.nn.dropout(layer1, keep_prob=0.5)
out_layer = tf.matmul(layer1, weight['out']) + bias['out']

# #we mask nodes without labels for loss calculation
# 定义损失函数
loss = tf.nn.softmax_cross_entropy_with_logits( logits=out_layer, labels=y_)
loss = tf.boolean_mask(loss, train_mask)
cost = tf.reduce_mean(loss)

# 优化
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

# 初始化所有变量
init = tf.initialize_all_variables()
correct_prediction = tf.equal(tf.argmax(out_layer, 1), tf.argmax(y, 1))
correct_prediction = tf.boolean_mask(correct_prediction, test_mask)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(1, NB_EPOCH + 1):
        _, c, a = sess.run([optimizer, cost, accuracy], feed_dict={X_in:X, y_:y_train, keep_prob: 0.5})
        print("Epoc ", epoch, " cost: ", c, " accuracy: ", a)

        if epoch % 1000 == 0:
            print(epoch, 'test_arruracy:', accuracy.eval({X_in:X, y_:y_test, keep_prob: 1}))


