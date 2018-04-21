该脚本实现了使用tensorflow实现vgg16，并且训练mnist，预测与输出




池化的计算涉及到神经元的计算

最后连接层的神经元应该是：
	pool_size * pool_size * batch_size
pool_size = (上一层pol_size – 池化尺寸)/2+1
例如
	输入尺寸28，
	batch_size =128
	池化尺寸2，
	池化后的维度为（28-2）/2+1=14
	如果现在输出，连接层神经元就是，14*14*128
	即 'wd1_1':tf.Variable(tf.random_normal([14*14*128,25088])),

