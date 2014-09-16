drop database if exists `coursemate`;

create database `coursemate`
	default character set utf8
	default collate utf8_general_ci;

use coursemate;

drop table if exists `student`;
CREATE TABLE student
(
	`user_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`username` VARCHAR(128) NOT NULL comment '用户名',
	`sex` tinyint NOT NULL comment '性别',
	`grade` VARCHAR(32) NOT NULL comment '年级',
	`nickname` VARCHAR(128) NULL comment '昵称',
	`password` VARCHAR(128) NOT NULL comment '密码',
    `major` varchar(32) null comment '专业名称',
    `school` varchar(32) null comment '所属学院',
    `number` varchar(32) not null comment '学号',
	`email` VARCHAR(128) NULL comment '邮箱',
	`mail` VARCHAR(128) NULL comment '邮编',
	`call` VARCHAR(128) NULL comment '联系电话',
	`signature` VARCHAR(256) NULL comment '签名',
	`pre_school` VARCHAR(256) NULL comment '原学校',
	`address` VARCHAR(256) NULL comment '地址',
	`detail_address` VARCHAR(512) NULL comment '详细地址',
	`pic_url` VARCHAR(256) NULL comment '头像链接',
	`score` INTEGER not NULL comment '用户积分',
	`rank` INTEGER not NULL comment '用户等级',
	`login_time` INTEGER not null comment '最近登录时间',
	`cookie` VARCHAR(1024) NULL comment 'cookie',
	unique key(`username`),
	primary key (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='学生表';

drop table if exists `teacher`;
CREATE TABLE `teacher`
(
	`tea_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
    `tea_name` varchar(512) not null comment '姓名',
    `school` varchar(512) null comment '所属学院',
	`sex` VARCHAR(16) NULL comment '性别',
	`score` INTEGER NOT NULL comment '评价分数',
	primary key (`tea_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='教师表';

drop table if exists `course`;
CREATE TABLE `course`
(
	`cou_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
    `resourceID` varchar(32) not null comment '课程resourceID',
    `course_name` varchar(512) not null comment '课程名称',
    `time` varchar(1024) not null comment '上课时间',
    `tea_id` INTEGER not null comment '授课老师',
	CONSTRAINT `cou_ibfk_1` FOREIGN KEY (`tea_id`)
		REFERENCES `teacher` (`tea_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`cou_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='课程表';

drop table if exists `stu_course`;
CREATE TABLE `stu_course`
(
	`sc_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
    `stu_id` INTEGER not null comment '课程ID',
    `cou_id` INTEGER not null comment '学生ID',
	CONSTRAINT `sc_ibfk_1` FOREIGN KEY (`cou_id`)
		REFERENCES `course` (`cou_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `sc_ibfk_2` FOREIGN KEY (`stu_id`)
		REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`sc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='学生-课程表';

drop table if exists `friend`;
CREATE TABLE `friend`
(
	`fr_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
    `stu1` INTEGER not null comment '学生1',
    `stu2` INTEGER not null comment '学生2',
	CONSTRAINT `fr_ibfk_1` FOREIGN KEY (`stu1`)
		REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `fr_ibfk_2` FOREIGN KEY (`stu2`)
		REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`fr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='好友关系表';

drop table if exists `post`;
CREATE TABLE post
(
	`post_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`title` VARCHAR(128) NOT NULL comment '标题',
	`content` TEXT NOT NULL comment '帖子内容',
	`tags` TEXT NULL comment '标签',
	`status` INTEGER NOT NULL default 0 comment '状态，0 = 草稿，1 = 发布',
	`create_time` INTEGER not null comment '创建时间',
	`author_id` INTEGER NOT NULL comment '作者',
	`cou_id` INTEGER NOT NULL comment '关联课程',
	CONSTRAINT `post_ibfk_1` FOREIGN KEY (author_id)
		REFERENCES student(`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `post_ibfk_2` FOREIGN KEY (`cou_id`)
		REFERENCES `course` (`cou_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='日志表';

drop table if exists `comments`;
CREATE TABLE `comments`
(
	`com_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`content` TEXT NOT NULL comment '评论内容',
	`create_time` INTEGER not NULL comment '评论时间',
	`author_id` INTEGER NOT NULL comment '评论者',
	`post_id` INTEGER NOT NULL comment '回复帖子ID',
	CONSTRAINT `com_ibfk_1` FOREIGN KEY (`author_id`)
		REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `com_ibfk_2` FOREIGN KEY (`post_id`)
		REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`com_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='评论表';

drop table if exists `message`;
CREATE TABLE `message`
(
	`me_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`fr_id` INTEGER NOT NULL comment '对应好友对',
	`content` VARCHAR(1024) NOT NULL comment '消息内容',
	`send_time` INTEGER not NULL comment '发送时间',
	CONSTRAINT `me_ibfk_1` FOREIGN KEY (`fr_id`)
		REFERENCES `friend` (`fr_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`me_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='好友间消息表';
