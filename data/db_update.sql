drop table if exists `student`;
CREATE TABLE student
(
	`username` VARCHAR(128) NOT NULL comment '用户名',
	`grade` VARCHAR(32) NOT NULL comment '年级',
	`nickname` VARCHAR(128) NULL comment '昵称',
	`password` VARCHAR(128) NOT NULL comment '密码',
    `major` varchar(32) null comment '专业名称',
    `school` varchar(32) null comment '所属学院',
    `user_id` varchar(32) not null comment '学号',
	`email` VARCHAR(128) NULL comment '邮箱',
	`mail` VARCHAR(128) NULL comment '邮编',
	`call` VARCHAR(128) NULL comment '联系电话',
	`signature` VARCHAR(256) NULL comment '签名',
	`pre_school` VARCHAR(256) NULL comment '原学校',
	`address` VARCHAR(256) NULL comment '地址',
	`detail_address` VARCHAR(512) NULL comment '详细地址',
	`pic_url` VARCHAR(256) NULL comment '头像链接',
	unique key(`username`),
	primary key (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='学生表';

drop table if exists `course`;
CREATE TABLE `course`
(
    `cou_id` varchar(128) not null comment '课程resourceID',
    `course_name` varchar(512) not null comment '课程名称',
    `time` varchar(1024) not null comment '上课时间',
    `teacher` VARCHAR(32) not null comment '授课老师',
	primary key (`cou_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='课程表';

drop table if exists `stu_course`;
CREATE TABLE `stu_course`
(
	`sc_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
    `stu_id` varchar(128) not null REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    `cou_id` varchar(128) not null REFERENCES `course` (`cou_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`sc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='学生-课程表';


drop table if exists `post`;
CREATE TABLE post
(
	`post_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`title` VARCHAR(128) NOT NULL comment '标题',
	`content` TEXT NOT NULL comment '帖子内容',
	`tags` TEXT NULL comment '标签',
	`status` INTEGER NOT NULL default 0 comment '状态，0 = 草稿，1 = 发布',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`author_id` INTEGER NOT NULL REFERENCES student(`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	`cou_id` varchar(128) NOT NULL REFERENCES `course` (`cou_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='日志表';

drop table if exists `comments`;
CREATE TABLE `comments`
(
	`com_id` INTEGER NOT NULL AUTO_INCREMENT comment '主键',
	`content` TEXT NOT NULL comment '评论内容',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`author_id` INTEGER NOT NULL REFERENCES `student` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	`post_id` INTEGER NOT NULL REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	primary key (`com_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='评论表';
