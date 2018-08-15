
这个是对pymysql的使用写成class，简化数据库的操作<br><br>

里面内置了一部分需要写的MySQL语句，将他变成一个函数的简单调用，使用方法<br><br>


alter_table_change(table_name, old_modify, new_modify, data_type='')<br>
    #功能：改变字段名<br><br>

alter_table_modify(table_name, modify, data_type='')<br>
    #功能：改变字段<br><br>

alter_table_name(old_table, new_table)<br>
    #功能：改变表名<br><br>

create_database(database)<br>
    #功能:创建数据库<br><br>

create_table(table_name, content)<br>
    #功能:创建表<br><br>
	
delete_data(table_name, condition)<br>
    #功能:删除数据，condition为限制条件，同样需要先选择数据库<br><br>

drop_database(database)<br>
    #功能:删除数据库<br><br>

drop_table(selfe, table_name)<br>
    #功能:删除表，需要在之前选择数据库<br><br>

my_connect(self)<br>
    #定义一个函数获取游标,连接数据库<br><br>

select_data(table_name, condition)<br>
    #功能：简单查询，condition同样为限制条件<br><br>

source_file(filename)<br>
    #功能:导入数据<br><br>

table_out(table_name, outfile)<br>
    #功能:导出数据表，需要先选择数据库<br><br>

use_database(database)<br>
    #功能:选择数据库,执行数据库之内的操作必须先选择数据库<br><br>

class初始化<br>
d=database(host,username,password)

连接数据库:<br>
d.my_connect()<br><br>

接下来就直接使用上面的函数进行简单的mysql操作
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	