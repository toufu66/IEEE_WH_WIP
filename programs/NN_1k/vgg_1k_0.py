#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 08:22:32 2019

@author: masahiro
"""

import tensorflow as tf
import numpy as np
import mkbatch_1d as mkb
import get_file_path as gfp
import random
import multiprocessing as mp
core_num=mp.cpu_count()
fft_tap=mkb.fft_tap
sl_win=mkb.sl_win
#mode=["train","test"]
for_num=mkb.for_num

outs=5

is_training = tf.placeholder(tf.bool)
keep_prob = tf.placeholder(tf.float32)





def batch_norm_wrapper(inputs, is_training, decay = 0.99):
    epsilon = 1e-5
    scale = tf.Variable(tf.ones([inputs.get_shape()[-1]]))
    beta = tf.Variable(tf.zeros([inputs.get_shape()[-1]]))
    pop_mean = tf.Variable(tf.zeros([inputs.get_shape()[-1]]), trainable=False)
    pop_var = tf.Variable(tf.ones([inputs.get_shape()[-1]]), trainable=False)

    if is_training is True:
        batch_mean, batch_var = tf.nn.moments(inputs,[0])
        train_mean = tf.assign(pop_mean,
                               pop_mean * decay + batch_mean * (1 - decay))
        train_var = tf.assign(pop_var,
                              pop_var * decay + batch_var * (1 - decay))
        with tf.control_dependencies([train_mean, train_var]):
            return tf.nn.batch_normalization(inputs,
                batch_mean, batch_var, beta, scale, epsilon)
    else:
        return tf.nn.batch_normalization(inputs,
            pop_mean, pop_var, beta, scale, epsilon)




file_path,li_train,li_test=gfp.file_path,gfp.li_train,gfp.li_test



test_size=32
batchsize = 2**6
epoch=4000*3
all_datasize=len(li_train)


# プレースホルダー
#x_ = tf.placeholder(tf.float32, shape=(None, for_num,int(fft_tap/2)-1, 1))
#x_=batch_norm_wrapper(_x_,is_training)
#x_ = tf.placeholder(tf.float32, shape=(None, 3,256, 1))


x_ = tf.placeholder(tf.float32, shape=(None, fft_tap, 1))

# 畳み込み層1
conv1_features = 256 # 畳み込み層1の出力次元数
max_pool_size1 = 2 # 畳み込み層1のマックスプーリングサイズ
conv1_1w = 0.9*tf.Variable(tf.truncated_normal([5, 3, conv1_features], stddev=0.1), dtype=tf.float32) # 畳み込み層1の重み
conv1_2w = 0.9*tf.Variable(tf.truncated_normal([5, conv1_features, conv1_features], stddev=0.1), dtype=tf.float32) # 畳み込み層1の重み


_conv1_1_c2 = tf.nn.conv1d(x_, conv1_1w, stride=1, padding="SAME") # 畳み込み層1-畳み込み
_conv1_2_c2 = tf.nn.conv1d(_conv1_1_c2, conv1_2w, stride=1, padding="SAME") # 畳み込み層1-畳み込み

conv1_c2=batch_norm_wrapper(_conv1_2_c2,is_training)
#conv1_relu = tf.nn.leaky_relu(conv1_c2+conv1_b) # 畳み込み層1-ReLU

conv1_b = tf.Variable(tf.constant(0.1, shape=[conv1_features]), dtype=tf.float32) # 畳み込み層1のバイアス

conv1_relu = tf.nn.relu(conv1_c2+conv1_b) # 畳み込み層1-ReLU

#conv1_mp = tf.nn.max_pool(conv1_relu, ksize=[1, max_pool_size1,1, 1], strides=[1, max_pool_size1, 1, 1], padding="SAME") # 畳み込み層1-マックスプーリング
conv1_mp =tf.layers.max_pooling1d(conv1_relu, pool_size=max_pool_size1, strides=max_pool_size1,padding="SAME")










conv2_features = 128 # 畳み込み層2の出力次元数
max_pool_size2 = 2 # 畳み込み層2のマックスプーリングのサイズ
conv2_1w = 0.9*tf.Variable(tf.truncated_normal([5, conv1_features, conv2_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み
conv2_2w = 0.9*tf.Variable(tf.truncated_normal([5, conv2_features, conv2_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み


conv2_b = tf.Variable(tf.constant(0.1, shape=[conv2_features]), dtype=tf.float32) # 畳み込み層2のバイアス

_conv2_1_c2 = tf.nn.conv1d(conv1_mp, conv2_1w, stride=1, padding="SAME") # 畳み込み層2-畳み込み
_conv2_2_c2 = tf.nn.conv1d(_conv2_1_c2, conv2_2w, stride=1, padding="SAME") # 畳み込み層2-畳み込み

conv2_c2=batch_norm_wrapper(_conv2_2_c2,is_training)


#conv2_relu = tf.nn.leaky_relu(conv2_c2+conv2_b) # 畳み込み層2-ReLU
conv2_relu = tf.nn.relu(conv2_c2+conv2_b) # 畳み込み層2-ReLU
#conv2_mp = tf.nn.max_pool(conv2_relu, ksize=[1,  max_pool_size2,1, 1], strides=[1, max_pool_size2, 1, 1], padding="SAME") # 畳み込み層2-マックスプーリング
conv2_mp =tf.layers.max_pooling1d(conv2_relu, pool_size=max_pool_size2, strides=max_pool_size2,padding="SAME")



# 畳み込み層's3
conv3_features = 64 # 畳み込み層2の出力次元数
max_pool_size3 = 2 # 畳み込み層2のマックスプーリングのサイズ
conv3_1w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv2_features, conv3_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み
conv3_2w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv3_features, conv3_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み
conv3_3w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv3_features, conv3_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み

conv3_b = tf.Variable(tf.constant(0.1, shape=[conv3_features]), dtype=tf.float32) # 畳み込み層2のバイアス

_conv3_1_c2 = tf.nn.conv1d(conv2_mp, conv3_1w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み
_conv3_2_c2 = tf.nn.conv1d(_conv3_1_c2, conv3_2w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み
_conv3_3_c2 = tf.nn.conv1d(_conv3_2_c2, conv3_3w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み




conv3_c2=batch_norm_wrapper(_conv3_3_c2,is_training)

#conv3_relu = tf.nn.leaky_relu(conv3_c2+conv3_b) # 畳み込み層2-ReLU
conv3_relu = tf.nn.relu(conv3_c2+conv3_b) # 畳み込み層2-ReLU


#conv3_relu = tf.nn.relu(conv3_c2+conv3_b) # 畳み込み層2-ReLU
#conv3_mp = tf.nn.max_pool(conv3_relu, ksize=[1,  max_pool_size3,1, 1], strides=[1, max_pool_size3, 1,1], padding="SAME") # 畳み込み層2-マックスプーリング
conv3_mp =tf.layers.max_pooling1d(conv3_relu, pool_size=max_pool_size3, strides=max_pool_size3,padding="SAME")






# 畳み込み層4's
conv4_features = 32 # 畳み込み層2の出力次元数
max_pool_size4 = 2 # 畳み込み層2のマックスプーリングのサイズ
conv4_1w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv3_features, conv4_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み
conv4_2w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv4_features, conv4_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み
conv4_3w = 0.9*tf.Variable(tf.truncated_normal([ 5, conv4_features, conv4_features], stddev=0.1), dtype=tf.float32) # 畳み込み層2の重み

conv4_b = tf.Variable(tf.constant(0.1, shape=[conv4_features]), dtype=tf.float32) # 畳み込み層2のバイアス

_conv4_1_c2 = tf.nn.conv1d(conv3_mp, conv4_1w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み
_conv4_2_c2 = tf.nn.conv1d(_conv4_1_c2, conv4_2w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み
_conv4_3_c2 = tf.nn.conv1d(_conv4_2_c2, conv4_3w, stride= 1, padding="SAME") # 畳み込み層2-畳み込み




conv4_c2=batch_norm_wrapper(_conv4_3_c2,is_training)

#conv3_relu = tf.nn.leaky_relu(conv3_c2+conv3_b) # 畳み込み層2-ReLU
conv4_relu = tf.nn.relu(conv4_c2+conv4_b) # 畳み込み層2-ReLU


#conv3_relu = tf.nn.relu(conv3_c2+conv3_b) # 畳み込み層2-ReLU
#conv3_mp = tf.nn.max_pool(conv3_relu, ksize=[1,  max_pool_size3,1, 1], strides=[1, max_pool_size3, 1,1], padding="SAME") # 畳み込み層2-マックスプーリング
conv4_mp =tf.layers.max_pooling1d(conv4_relu, pool_size=max_pool_size4, strides=max_pool_size4,padding="SAME")



# 全結合層1

result_w = x_.shape[1] // (max_pool_size1*max_pool_size2*max_pool_size3*max_pool_size4)
result_h = x_.shape[2] // (max_pool_size1*max_pool_size2*max_pool_size3*max_pool_size4)
fc_input_size = result_w * result_h * conv4_features # 畳み込んだ結果、全結合層に入力する次元数
fc_features1 = 2048 # 全結合層の出力次元数（隠れ層の次元数）
s = conv3_mp.get_shape().as_list() # [None, result_w, result_h, conv2_features]

_conv_result = tf.reshape(conv3_mp, [-1, s[1]*s[2]]) # 畳み込みの結果を1*N層に変換
conv_result=tf.nn.dropout(_conv_result,keep_prob)#dropout

fc1_w = 0.9*tf.Variable(tf.truncated_normal([s[1]*s[2], fc_features1], stddev=0.1), dtype=tf.float32) # 重み
#fc1_w = tf.Variable(tf.truncated_normal([fc_input_size.value, fc_features], stddev=0.1), dtype=tf.float32) # 重み
fc1_b = tf.Variable(tf.constant(0.1, shape=[fc_features1]), dtype=tf.float32) # バイアス


# 全結合層1 with drop_out
#fc1 = tf.nn.leaky_relu(batch_norm_wrapper(tf.matmul(conv_result, fc1_w),is_training)+fc1_b) 
_fc1 = tf.nn.relu(tf.matmul(conv_result, fc1_w)+fc1_b) 
fc1=tf.nn.dropout(_fc1,keep_prob)
#fc1 = tf.nn.relu(tf.matmul(conv_result, fc1_w)+fc1_b) # 全結合層1
fc_features2 = 1024
# 全結合層2
fc2_w = 0.9*tf.Variable(tf.truncated_normal([fc_features1, fc_features2], stddev=0.1), dtype=tf.float32) # 重み
fc2_b = tf.Variable(tf.constant(0.1, shape=[fc_features2]), dtype=tf.float32) # バイアス

#fc2 = tf.nn.leaky_relu(batch_norm_wrapper(tf.matmul(fc1, fc2_w),is_training)+fc2_b) # 全結合層2
_fc2 = tf.nn.relu(tf.matmul(fc1, fc2_w)+fc2_b) # 全結合層2
fc2=tf.nn.dropout(_fc2,keep_prob)
#fc2 = tf.nn.relu(tf.matmul(fc1, fc2_w)+fc2_b) # 全結合層2

# 全結合層3
fc3_w = 0.9*tf.Variable(tf.truncated_normal([fc_features2, outs], stddev=0.1), dtype=tf.float32) # 重み
fc3_b = tf.Variable(tf.constant(0.1, shape=[outs]), dtype=tf.float32) # バイアス
y = tf.nn.softmax(tf.matmul(fc2, fc3_w)+fc3_b)
y_ = tf.placeholder(tf.float32, shape=(None, outs))

# クロスエントロピー誤差
#cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
cross_entropy =tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y,1.0e-10,1)),reduction_indices=[1]))

# 勾配法
#train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
train_step = tf.train.AdamOptimizer(learning_rate=0.0001,beta1=0.9,beta2=0.999,epsilon=1.0e-7).minimize(cross_entropy)


# 正解率の計算
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init=tf.global_variables_initializer()
config = tf.ConfigProto(inter_op_parallelism_threads=core_num,
    intra_op_parallelism_threads=core_num,
    gpu_options=tf.GPUOptions(allow_growth=True))
sess = tf.Session(config = config)
#sess = tf.Session()
saver=tf.train.Saver()
saver.restore(sess,"./model_vgg_0/model.ckpt")
#sess.run(init)
random.shuffle(li_train)
random.shuffle(li_test)
#random.shuffle(li_vali)


#initialized batch head
bh=0
ic = 0
acc=[]
vh=0

for i in range(epoch):
    #print("loop:",i)
    #if(bh>ind_train[4]):
    if(bh>=2048):
        bh=0
        
        random.shuffle(li_train)
        
    #print("bhead:",bh)
    #print(i)    
    batch_x=mkb.batch_data(li_train[bh:bh+batchsize])
    batch_y=mkb.ind_to_label(li_train[bh:bh+batchsize])    
    bh+=batchsize
    
    #drop = np.random.binomial(1,0.4,[batchsize,int(data_size/2)])
    #drop = np.where(drop==0, 1e-6,drop)
    
    #train_prob=1.0
    sess.run(train_step, feed_dict={x_: batch_x, is_training: True,y_: batch_y, keep_prob:0.9})
    acc0,loss,output=sess.run([accuracy,cross_entropy,tf.argmax(y,1)], feed_dict={x_: batch_x,is_training: True, y_: batch_y, keep_prob:0.9})
    acc=np.append(acc,acc0)
    #print(sess.run(tf.argmax(y,1),feed_dict={x_:batch_x,is_training: True}))
    print(output)
    print(np.argmax(batch_y,1),"\n")
    print("acc:",acc0,"loss",loss)
    
    if i%10 ==0:
        ic+=1
        vali_x=mkb.batch_data(li_test[vh:vh+batchsize])
        vali_y=mkb.ind_to_label(li_test[vh:vh+batchsize])
        vh+=batchsize
        
        print("loop:",i)
        print("------------------------------")
        print('train:',acc0)
        #print(sess.run(tf.argmax(y,1),feed_dict={x:batch_x,keep_prob:1.0}),"\n",batch_y)
        
        print('validation acc:',sess.run(accuracy, feed_dict={x_: vali_x,is_training: True, y_: vali_y, keep_prob:1.0}))
        print('-------------------------------------------------')
        if vh>=300:
            vh=0
            random.shuffle(li_test)
        if ic%5 == 0:    
            saver.save(sess,"./model_vgg_0_add1/model.ckpt")
        



test_x=mkb.batch_data(li_test)
test_y=mkb.ind_to_label(li_test)
saver.save(sess,"./model_vgg_0_add1/model.ckpt")
print("------------------------------")
print('test acc:',sess.run(accuracy, feed_dict={x_: test_x,is_training: False, y_: test_y, keep_prob:1.0}))
