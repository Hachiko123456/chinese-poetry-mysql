class Sql:
    create_favorite_sql = """create table favorite
    (
    	id bigint unsigned auto_increment comment '收藏ID'
    		primary key,
    	user_id bigint unsigned not null comment '用户ID',
    	poetry_id int not null comment '诗歌ID',
    	create_time datetime default CURRENT_TIMESTAMP not null comment '收藏时间'
    )
    collate=utf8mb4_general_ci;

    create index favorite_poetry_id_IDX
    	on favorite (poetry_id);

    create index favorite_user_id_IDX
    	on favorite (user_id);

    """

    create_poetry_access_history_sql = """create table poetry_access_history
(
	id bigint unsigned auto_increment comment '主键ID'
		primary key,
	user_id bigint unsigned not null comment '用户ID（关联用户表）',
	poetry_id bigint unsigned not null comment '诗歌ID（关联诗歌表）',
	view_time datetime(6) default CURRENT_TIMESTAMP(6) not null comment '访问时间（精确到微秒）',
	ip_address varchar(45) null comment '访问者IP地址（支持IPv6最长格式）',
	device_info varchar(255) null comment '访问设备信息（如浏览器、操作系统）'
)
comment '诗歌访问历史记录表' collate=utf8mb4_general_ci;

create index idx_user_poetry_time
	on poetry_access_history (user_id, view_time);

"""
    create_poetry_type_sql = """create table poetry_type
(
	id int unsigned auto_increment comment '主键ID'
		primary key,
	type varchar(50) not null comment '诗歌类型',
	name varchar(255) not null comment '类型名称',
	sub_title varchar(255) null comment '朝代背景',
	representative_poet varchar(255) null comment '代表诗人',
	poetry_order int null comment '诗词顺序',
	constraint uk_type
		unique (type)
)
comment '诗歌类型表' collate=utf8mb4_general_ci;

"""
    import_poetry_type_sql="""INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (1, 'TS', '唐诗', '中国诗歌黄金时期,格律诗成熟发展,收录近五万首作品', '李白,杜甫,王维', 400);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (2, 'TSB', '唐诗三百首', '蘅塘退士编选本,蒙学经典教材,涵盖77位诗人', '张九龄,孟浩然,王昌龄', 410);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (3, 'YDTS', '御定全唐诗', '清代官修总集,收录48700余首,涵盖2200位诗人', '李世民,上官婉儿,李隆基', 420);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (4, 'SMTS', '水墨唐诗', '诗书画三绝结合,明代文人创作,现存1200幅作品', '王维,柳宗元,韦应物', 430);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (5, 'SS', '宋诗', '以文为诗新风尚,哲理诗盛行,存世27万首', '苏轼,陆游,杨万里', 610);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (6, 'SC', '宋词', '长短句音乐文学,现存词牌870种,作品2万余', '辛弃疾,李清照,柳永', 600);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (7, 'HJJ', '花间集', '首部文人词总集,收录晚唐五代500首,影响婉约派', '温庭筠,韦庄,皇甫松', 500);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (8, 'NTEZC', '南唐诗', '五代十国南唐创作,存词286首,亡国之音典范', '李煜,冯延巳,徐铉', 1200);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (9, 'YQ', '元曲', '包含散曲杂剧,现存小令3853首,套数457套', '关汉卿,马致远,白朴', 700);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (10, 'SJ', '诗经', '西周至春秋诗歌,风雅颂三体,305篇全集', '佚名（民间采集）', 100);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (11, 'SSWJ', '四书五经', '儒家核心经典,包含大学、中庸等九部典籍', '孔子及其弟子', 900);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (12, 'LY', '论语', '孔子言行录,20篇512章,儒家第一经', '孔子,曾子,子贡', 910);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (13, 'YMY', '幽梦影', '清代笔记小品,219则人生感悟,骈散结合文体', '张潮', 1100);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (14, 'NLXD', '纳兰性德诗词', '现存348首词作,哀感顽艳风格,王国维高度评价', '纳兰性德', 800);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (15, 'MX', '蒙学', '传统启蒙教材,包含三字经、千字文等经典', '周兴嗣,王应麟,李毓秀', 1000);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (16, 'CCSJ', '曹操诗集', '建安文学代表,现存完整诗作21首,古直悲凉', '曹操,曹丕,曹植', 300);
INSERT INTO chinese_poetry.poetry_type (id, type, name, sub_title, representative_poet, poetry_order) VALUES (17, 'CC', '楚辞', '骚体文学源头,收录17篇,开创浪漫主义传统', '屈原,宋玉,景差', 200);"""

    create_social_auth_sql = """create table social_auth
(
	id bigint unsigned auto_increment
		primary key,
	user_id bigint unsigned not null,
	platform varchar(10) not null comment '微信/QQ/微博等',
	openid varchar(64) not null,
	unionid varchar(64) null,
	create_time datetime default CURRENT_TIMESTAMP not null,
	constraint uk_platform_openid
		unique (platform, openid)
)
collate=utf8mb4_unicode_ci;

create index social_auth_openid_IDX
	on social_auth (openid);

create index social_auth_user_id_IDX
	on social_auth (user_id);

"""

    create_user_info_sql = """create table user_info
(
	id bigint unsigned auto_increment comment '用户ID'
		primary key,
	nickname varchar(64) null comment '用户昵称',
	avatar_url varchar(255) not null comment '头像URL',
	gender tinyint(1) default 0 not null comment '性别 0-未知 1-男 2-女',
	province varchar(20) null comment '省份',
	city varchar(20) null comment '城市',
	country varchar(20) null comment '国家',
	email varchar(100) null comment '邮箱（预留字段）',
	create_time datetime default CURRENT_TIMESTAMP not null comment '创建时间',
	update_time datetime null on update CURRENT_TIMESTAMP comment '更新时间'
)
collate=utf8mb4_unicode_ci;

"""
