# -*- coding: UTF-8 -*-
from __future__ import print_function

from keras.layers import Input, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras.regularizers import l2

from layers.graph import GraphConvolution
from utils import *

import time

# Define parameters
DATASET = 'cora'
FILTER = 'localpool'             #'chebyshev'    #'localpool'
MAX_DEGREE = 2  # maximum polynomial degree  几阶邻居
SYM_NORM = True  # symmetric (True) vs. left-only (False) normalization
NB_EPOCH = 200
PATIENCE = 10  # early stopping patience

# Get data
X, A, y = load_data(dataset=DATASET)

# print(X.shape, A.shape, y.shape)    #(2708, 1433) 2708个样本点，每个样本1433列特征    (2708, 2708)  2708个样本点的邻接矩阵     (2708, 7)  7个类onehot
# Dataset has 2708 nodes, 5429 edges, 1433 features.
# (2708L, 1433L) (2708, 2708) (2708L, 7L)

y_train, y_val, y_test, idx_train, idx_val, idx_test, train_mask = get_splits(y)



# Normalize X
X /= X.sum(1).reshape(-1, 1)

if FILTER == 'localpool':
    """ Local pooling filters (see 'renormalization trick' in Kipf & Welling, arXiv 2016)   localized first-order approximation  """
    print('Using local pooling filters...')
    A_ = preprocess_adj(A, SYM_NORM)   #处理过的A_是D-0.5 A D-0.5
    #print(A_.shape)   #(2708, 2708)
    support = 1
    graph = [X, A_]
    # print("X.shape ", X.shape)  #(2708L, 1433L)
    # print("A_.shape ", A_.shape)   #(2708, 2708)

    #以下写法都可以 https://blog.csdn.net/weixin_38145317/article/details/79549406
    #G = [Input(shape=(None, None), batch_shape=(None, None), sparse=True)]  #数组，包含 Input  这一个元素
    #G = [Input(shape=(None,), sparse=True)]
    #batch_shape：指batch size, 例如batch_shape=(10,32),意味着 输入的batch=10,即实际输入为10行，32列的矩阵，batch_shape=(None,32)意味着任意batch的32列向量
    G = [Input(batch_shape=(None, None), sparse=True)]  #数组，包含 Input  这一个元素

elif FILTER == 'chebyshev':
    """ Chebyshev polynomial basis filters (Defferard et al., NIPS 2016)  """
    print('Using Chebyshev polynomial basis filters...')
    L = normalized_laplacian(A, SYM_NORM)
    L_scaled = rescale_laplacian(L)
    T_k = chebyshev_polynomial(L_scaled, MAX_DEGREE)
    support = MAX_DEGREE + 1
    graph = [X]+T_k
    G = [Input(shape=(None, None), batch_shape=(None, None), sparse=True) for _ in range(support)]

else:
    raise Exception('Invalid filter type.')

#  shape,不包括batch size, 例如 shape=(32,), 意味着输入是1行32列的向量
X_in = Input(shape=(X.shape[1],))  #一个节点有1433 features.，所以输入形状就是X.shape[1]，

# Define model architecture
# NOTE: We pass arguments for graph convolutional layers as a list of tensors.
# This is somewhat hacky, more elegant options would require rewriting the Layer base class.
H = Dropout(0.5)(X_in)
# print("H.shape ", H.shape)
# print("[H] len  ", len([H]))
# print("G len ", len(G))
# print("[H]+G len ", len([H]+G) )
H = GraphConvolution(16, support, activation='relu', kernel_regularizer=l2(5e-4))([H]+G)   ##数组[H, G]，包含 H G 这2个元素 在tensor里面表示为[H]+G
H = Dropout(0.5)(H)
Y = GraphConvolution(y.shape[1], support, activation='softmax')([H]+G)

# Compile model
#  keras函数式模型（区别于序贯模型）  可构造拥有多输入和多输出的模型  如 model = Model(inputs=[a1, a2], outputs=[b1, b3, b3])
model = Model(inputs=[X_in]+G, outputs=Y)
model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.01))

# Helper variables for main training loop
wait = 0
preds = None
best_val_loss = 99999

# Fit
for epoch in range(1, NB_EPOCH+1):

    # Log wall-clock time
    t = time.time()

    # Single training iteration (we mask nodes without labels for loss calculation)
    # graph 对应 inputs=[X_in]+G   真实的graph = [X, A_]    也就是说 X对应X_in，   A_对应G
    # 也就是说，X_in = Input(shape=(X.shape[1],))
    # G = [Input(shape=(None, None), batch_shape=(None, None), sparse=True)]  shape是一个2维邻接矩阵的维度
    # y_train对应 outputs=Y
    model.fit(graph, y_train, sample_weight=train_mask,
              batch_size=A.shape[0], epochs=1, shuffle=False, verbose=0)

    # Predict on full dataset
    preds = model.predict(graph, batch_size=A.shape[0])

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
