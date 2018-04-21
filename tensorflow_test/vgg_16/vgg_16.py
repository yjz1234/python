#coding:utf-8

import tensorflow as tf
import input_data


#初始化参数
learning_rate = 0.001
training_iters = 200000
batch_size = 128
display_step = 10
n_input = 784
n_classes = 10
dropout = 0.75


#输入占位符
x = tf.placeholder(tf.float32,[None,n_input])
y = tf.placeholder(tf.float32,[None,n_classes])
keep_prob = tf.placeholder(tf.float32)
mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)

#定义卷积
def conv2d(name,x,W,b,strides=1):
	x = tf.nn.conv2d(x,W,strides=[1,strides,strides,1],padding='SAME')
	x = tf.nn.bias_add(x,b)
	return tf.nn.relu(x,name=name)
	
def maxpool2d(name, x,k=2):
	return tf.nn.max_pool(x,ksize=[1,k,k,1],strides=[1,k,k,1],padding='SAME',name=name)

def norm(name, l_input, lsize=4):
	return tf.nn.lrn(l_input, lsize, bias=1.0, alpha=0.001 / 9.0,beta=0.75, name=name)
weights = {
	'wc1_1':tf.Variable(tf.random_normal([3,3,1,64])),
	'wc1_2':tf.Variable(tf.random_normal([3,3,64,64])),
	'wc2_1':tf.Variable(tf.random_normal([3,3,64,128])),
	'wc2_2':tf.Variable(tf.random_normal([3,3,128,128])),
	'wc3_1':tf.Variable(tf.random_normal([3,3,128,256])),
	'wc3_2':tf.Variable(tf.random_normal([3,3,256,256])),
	'wc3_3':tf.Variable(tf.random_normal([3,3,256,256])),
	'wc4_1':tf.Variable(tf.random_normal([3,3,256,512])),
	'wc4_2':tf.Variable(tf.random_normal([3,3,512,512])),
	'wc4_3':tf.Variable(tf.random_normal([3,3,512,512])),
	'wc5_1':tf.Variable(tf.random_normal([3,3,512,512])),
	'wc5_2':tf.Variable(tf.random_normal([3,3,512,512])),
	'wc5_3':tf.Variable(tf.random_normal([3,3,512,512])),
	'wd1_1':tf.Variable(tf.random_normal([2*2*128,512])),
	'wd1_2':tf.Variable(tf.random_normal([512,512])),
	'wd1_3':tf.Variable(tf.random_normal([512,1000])),
	'out':tf.Variable(tf.random_normal([1000,10]))
		}
biases = {
	'bc1':tf.Variable(tf.random_normal([64])),
	'bc2':tf.Variable(tf.random_normal([128])),
	'bc3':tf.Variable(tf.random_normal([256])),
	'bc4':tf.Variable(tf.random_normal([512])),
	'bc5':tf.Variable(tf.random_normal([512])),
	'bd1':tf.Variable(tf.random_normal([512])),
	'bd2':tf.Variable(tf.random_normal([1000])),
	'out':tf.Variable(tf.random_normal([n_classes])),
		}
		
def vgg_16net(x,weights,biases,dropout):
	x = tf.reshape(x,shape=[-1,28,28,1])

	#第一层卷积
	conv1_1 = conv2d('conv1_1',x,weights['wc1_1'],biases['bc1'])
	conv1_2 = conv2d('conv1_2',conv1_1,weights['wc1_2'],biases['bc1'])
	#最大池化
	pool_1 = maxpool2d('pool_1',conv1_2,k=2)
	
	#第二层卷积
	conv2_1 = conv2d('conv2_1',pool_1,weights['wc2_1'],biases['bc2'])
	conv2_2 = conv2d('conv2_2',conv2_1,weights['wc2_2'],biases['bc2'])
	#最大池化
	pool_2 = maxpool2d('pool_2',conv2_2,k=2)
	
	#第三层卷积
	conv3_1 = conv2d('conv3_1',pool_2,weights['wc3_1'],biases['bc3'])
	conv3_2 = conv2d('conv3_2',conv3_1,weights['wc3_2'],biases['bc3'])
	conv3_3 = conv2d('conv3_3',conv3_2,weights['wc3_3'],biases['bc3'])
	#最大池化
	pool_3 = maxpool2d('pool_3',conv3_3,k=2)
	
	#第四层卷积
	conv4_1 = conv2d('conv4_1',pool_3,weights['wc4_1'],biases['bc4'])
	conv4_2 = conv2d('conv4_2',conv4_1,weights['wc4_2'],biases['bc4'])
	conv4_3 = conv2d('conv4_3',conv4_2,weights['wc4_3'],biases['bc4'])
	#最大池化
	pool_4 = maxpool2d('pool_4',conv4_3,k=2)
	
	#第五层卷积
	conv5_1 = conv2d('conv5_1',pool_4,weights['wc5_1'],biases['bc5'])
	conv5_2 = conv2d('conv5_2',conv5_1,weights['wc5_2'],biases['bc5'])
	conv5_3 = conv2d('conv5_3',conv5_2,weights['wc5_3'],biases['bc5'])
	#最大池化
	pool_5 = maxpool2d('pool_5',conv5_3,k=2)
	
	#全连接层1
	fc1 = tf.reshape(pool_5,[-1,weights['wd1_1'].get_shape().as_list()[0]])
	fc1 = tf.add(tf.matmul(fc1, weights['wd1_1']), biases['bd1'])
	fc1 = tf.nn.dropout(fc1, dropout)
	
	#全连接层2
	fc2 = tf.reshape(fc1,[-1,weights['wd1_2'].get_shape().as_list()[0]])
	fc2 = tf.add(tf.matmul(fc2,weights['wd1_2']),biases['bd1'])
	fc2 = tf.nn.dropout(fc2, dropout)
	
	#全连接层3
	fc3 = tf.reshape(fc2,[-1,weights['wd1_3'].get_shape().as_list()[0]])
	fc3 = tf.add(tf.matmul(fc3,weights['wd1_3']),biases['bd2'])
	fc3 = tf.nn.dropout(fc3, dropout)
	#输出层
	out = tf.add(tf.matmul(fc3,weights['out']),biases['out'])
	return out
#构建模型
pred = vgg_16net(x,weights,biases,keep_prob)

#定义损失函数和优化器
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y))
optimizer = tf.train.AdadeltaOptimizer(learning_rate = learning_rate).minimize(cost)

#评估函数
correct_pred = tf.equal(tf.argmax(pred,1),tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred,tf.float32))

#初始化变量
init = tf.global_variables_initializer()
with tf.Session() as sess:
	sess.run(init)
	step = 1
	while step*batch_size < training_iters:
		batch_x,batch_y = mnist.train.next_batch(batch_size)
		sess.run(optimizer,feed_dict={x:batch_x,y:batch_y,keep_prob:dropout})

		if step % display_step == 0:
			loss, acc = sess.run([cost,accuracy],feed_dict={x:batch_x,y:batch_y,keep_prob:1.})
			print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
				"{:.6f}".format(loss) + ", Training Accuracy= " + \
				"{:.5f}".format(acc))
		step+=1
	print("optimization finished")
	print("Testing Accuracy:", \
		sess.run(accuracy, feed_dict={x: mnist.test.images[:256],
										y: mnist.test.labels[:256],
										keep_prob: 1.}))
