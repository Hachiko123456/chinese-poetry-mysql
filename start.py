import json
from typing import cast

import mysql.connector
from colorama import Fore
from mysql.connector import MySQLConnection

from console_py import console
from db import importAuthors, importData

console = console.Console()


def start():
    console.logPath = "./log.txt"
    begin = console.log("开始处理文件", Fore.CYAN)

    # 获取各种参数
    configFile = open("./config.json", "r", encoding="utf-8")
    config = json.loads(configFile.read())
    table = config["table"]
    tableAuthor = config["tableAuthor"]
    source = config["source"]
    data = config["files"]["data"]
    include = config["files"]["include"]
    exclude = config["files"]["exclude"]
    authors = config["files"]["authors"]

    # 连接数据库
    connect = cast(MySQLConnection, mysql.connector.connect(**config["mysql"]))
    cursor = connect.cursor()
    cursor.execute("SET names 'utf8mb4'")

    # 删除旧表, 创建新表
    # 诗词表
    if len(table):
        cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
        sql = f"""CREATE TABLE `{table}` (
            `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
            `author` text DEFAULT NULL COMMENT '作者名称',
            `author_id` int(11) DEFAULT NULL COMMENT '作者id',
            `dynasty` text NOT NULL COMMENT '朝代',
            `title` text DEFAULT NULL COMMENT '作品标题',
            `rhythmic` text DEFAULT NULL COMMENT '词牌名',
            `chapter` text DEFAULT NULL COMMENT '篇章',
--             `paragraphs` text NOT NULL COMMENT '正文段落',
            `notes` text DEFAULT NULL COMMENT '注解',
            `collection` text NOT NULL COMMENT '分类 TS（唐诗） YDTS（御定全唐诗） SMTS（水墨唐诗） SS（宋诗） SC（宋词） HJJ（花间集） NTEZC（南唐二主词） YQ（元曲） SJ（诗经） SSWJ（四书五经） LY（论语） NLXD（纳兰性德诗集） MX（蒙学） CCSJ（曹操诗集） CC（楚辞） YMY（幽梦影）',
            `section` text DEFAULT NULL COMMENT '分章信息',
            `content` longtext NOT NULL COMMENT '全文',
            `comment` text DEFAULT NULL COMMENT '评论赏析',
            `tags` text DEFAULT NULL COMMENT '标签',
            PRIMARY KEY (`id`),
            KEY `idx_author_id` (`author_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"""
        cursor.execute(sql)
    # 作者表
    if len(tableAuthor):
        cursor.execute(f"DROP TABLE IF EXISTS `{tableAuthor}`")
        sql = f"""CREATE TABLE `{tableAuthor}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` varchar(100) NOT NULL,
            `description` text,
            `short_description` text,
            PRIMARY KEY (`id`),
            KEY `idx_author_id` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"""
        cursor.execute(sql)

    # 循环处理json文件
    arr = []
    maxLenCollection = 0
    maxLenTime = 0
    total = 0
    res = None
    hasInclude = len(include) > 0
    hasExclude = len(exclude) > 0
    if len(table):
        for info in data:
            if hasInclude and info["collection"] not in include:
                continue
            if hasExclude and info["collection"] in exclude:
                continue
            res = importData(connect, source, table, info)
            arr.append(res)
            maxLenCollection = max(maxLenCollection, console.strLen(res["collection"]))
            maxLenTime = max(maxLenTime, console.strLen(res["time"]))
            if isinstance(res["count"], int):
                total += res["count"]
    if len(tableAuthor):
        if isinstance(authors, str):
            authors = [authors]
        res = importAuthors(connect, source, tableAuthor, authors)
        arr.append(res)
        maxLenCollection = max(maxLenCollection, console.strLen(res["collection"]))
        maxLenTime = max(maxLenTime, console.strLen(res["time"]))
        if isinstance(res["count"], int):
            total += res["count"]

    print('开始匹配作者信息')
    update_author_sql = """update chinese_poetry p set author_id = (select id from chinese_poetry_author pa where pa.name=p.author limit 1)"""
    cursor.execute(update_author_sql)
    print('匹配作者信息成功')

    cursor.close()

    connect.commit()
    connect.close()

    # 最后输出统计信息
    end = console.log("所有文件处理完毕", Fore.GREEN, begin)
    console.log()
    for v in arr:
        collection = console.strAlign(v["collection"], maxLenCollection, "L")
        time = console.strAlign(v["time"], maxLenTime, "L")
        console.log(f"{collection}  用时：{time}  记录数：{v['count']}")
    console.log(f"共计用时：{console.round(end - begin)}s")
    console.log(f"记录总数：{total}")
    console.log()


if __name__ == "__main__":
    start()
