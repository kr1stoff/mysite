-- 创建系统设置表格并添加初始数据
-- drop table if exists mysite.settings;
create table mysite.settings (
	id int auto_increment primary key,
	arg_name varchar(255),
	arg_value varchar(255)
);
-- 添加初始数据
insert into mysite.settings (arg_name, arg_value) value (
		"illumina_bcl_directory",
		"/data/mengxf/mysite/test/illumina_bcldir"
	);
-- 创建任务列表
create table mysite.tasks (
	id int auto_increment primary key,
	task_number varchar(255),
	chip_number varchar(255),
	workflow varchar(255),
	created_at datetime,
	completed_at datetime,
	bcl_status int,
	fastq_status int,
	analysis_status int
);
-- 删除列
-- alter table mysite.tasks drop column task_number;
-- 添加列
-- alter table mysite.tasks add column task_number varchar(255);
--  删除表
-- drop table mysite.tasks;
