#coding:utf-8
#强调：只针对文件夹复制，因为文件复制一般都有直接的命令
#在当前目录下生成一个复制的文件夹，环境windows，linux需要修改文件夹分割
import os

#文件夹复制程序，思路：先获取目录下的所有文件或文件夹名字，判断是不是文件，是就在传入的pwd目录下复制，不是就创建一个文件夹，并且生成新的pwd和file_path、，并且再次调用此函数
def copy_tree(file_path,pwd):
	l = os.listdir(file_path)
	for i in l:
		if os.path.isfile(os.path.join(file_path,i)):
			with open(os.path.join(pwd,i),'wb') as f1:
				with open(os.path.join(file_path,i),'rb') as f2:
					f1.write(f2.read())
		else:
			os.makedirs(os.path.join(pwd,i))
			copy_tree(os.path.join(file_path,i),os.path.join(pwd,i))

#主函数
def main():
	dir_name = input('请输入复制文件夹名字的路径：')
	pwd = os.path.join(dir_name.split('\\')[-1])
	dir_name = os.path.join(dir_name)
	print(pwd)
	print(dir_name)
	os.makedirs(pwd)
	copy_tree(dir_name,pwd)


if __name__ == '__main__':
	main()