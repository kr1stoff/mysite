-- 创建系统设置表格并添加初始数据
-- drop table if exists mysite.settings;
create table mysite.settings (
	id int auto_increment primary key,
	arg_name varchar(255),
	arg_value varchar(255)
);

insert into mysite.settings (arg_name, arg_value)
value ("illumina_bcl_directory", "/data/mengxf/mysite/test/illumina_bcldir");
