import json
import os
import traceback
from glob import glob
from typing import cast

from colorama import Fore
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from console_py import console
import zhconv

fields = {
    "author": {"type": "string"},
    "author_id": {"type": "int"},
    "dynasty": {"type": "string"},
    "title": {"type": "string"},
    "rhythmic": {"type": "string"},
    "chapter": {"type": "string"},
    # "paragraphs": {"type": "json"},
    "notes": {"type": "json"},
    "collection": {"type": "string"},
    "section": {"type": "string"},
    "content": {"type": "json"},
    "comment": {"type": "json"},
    "tags": {"type": "json"},
}

console = console.Console()


# 将json文件录入mysql数据库
def importData(connect: MySQLConnection, source: str, table: str, info: dict):
    path = info["path"]
    dynasty = info["dynasty"]
    collection = info["collection"]
    author = info.get("author")
    if isinstance(path, str):
        names = list(glob(f"{source}/{path}"))
    else:
        names = []
        for v in path:
            names += list(glob(f"{source}/{v}"))
    console.log()
    begin = console.info(f"正在处理  {collection}")
    cursor = cast(MySQLCursor, connect.cursor())
    success = 0
    error = 0
    for name in names:
        filename = os.path.basename(name)
        relName = os.path.relpath(name, source)
        try:
            console.log(f"正在处理文件  {relName}")
            file = open(name, "r", encoding="utf-8")
            # 繁体转简体
            data = json.loads(zhconv.convert(file.read(), 'zh-cn'))
            if filename == "tangshisanbaishou.json":
                data = shisanbai(data)
            if not isinstance(data, list):
                data = [data]
            for poet in data:
                values = []
                content_is_valid = True
                for field in fields:
                    if fields[field]["type"] == "string":
                        value = poet.get(field, "")
                        if field == "collection":
                            value = collection
                        elif field == "dynasty":
                            value = dynasty
                        elif field == "author":
                            if author:
                                value = author
                            if not value:
                                value = "不詳"
                        values.append(value)
                    elif field == "content":
                        value = poet.get(field, None)
                        if not value:
                            value = poet.get('paragraphs', None)
                        if not value:
                            value = poet.get('para', None)
                        if not value:
                            content_is_valid = False
                        values.append(json.dumps(value, ensure_ascii=False))
                    else:
                        value = poet.get(field, None)
                        if field == "tags":
                            if not isinstance(value, list):
                                try:
                                    value = [value]
                                except Exception:
                                    value = []
                            # if collection not in value:
                            #     value.append(collection)
                        elif field == 'author_id':
                            value = -1
                        values.append(json.dumps(value, ensure_ascii=False))
                if not content_is_valid:
                    print('内容为空，忽略......')
                    continue
                # 处理 null 字符串
                processed_values = [
                    None if isinstance(v, str) and v.strip().lower() in {'null', '[null]'} else v
                    for v in values
                ]
                params = [None] + processed_values
                num_placeholders = len(fields) + 1
                sql = f"INSERT INTO `{table}` VALUES ({', '.join(['%s'] * num_placeholders)})"
                cursor.execute(sql, params)
                success += 1
        except Exception:
            console.error(traceback.format_exc())
            end = console.error(f"{relName}  处理出错")
            error += 1
    if error == 0:
        end = console.success(f"{collection}  处理完毕", begin)
    else:
        end = console.warning(f"{collection}  处理完毕，共有{error}个错误", begin)
    cursor.close()
    console.log()
    return {
        "collection": collection,
        "count": success,
        "time": f"{console.round(end - begin)}s",
    }


# 录入作者
def importAuthors(
        connect: MySQLConnection,
        source: str,
        table: str,
        paths: list[str],
):
    names = ()
    for path in paths:
        names += tuple(glob(f"{source}/{path}"))
    console.log()
    begin = console.log("正在处理  作者", Fore.CYAN)
    cursor = connect.cursor()
    success = 0
    error = 0
    for name in names:
        name = os.path.normpath(name)
        relName = os.path.relpath(name, source)
        try:
            console.log(f"正在处理文件  {relName}")
            file = open(name, "r", encoding="utf-8")
            data = json.loads(zhconv.convert(file.read(), 'zh-cn'))
            if type(data).__name__ != "list":
                data = [data]
            for author in data:
                sql = f"INSERT INTO `{table}` VALUES (null,%s,%s,%s)"
                cursor.execute(
                    sql,
                    (
                        author.get("name") or "",
                        author.get("desc") or author.get("description") or "",
                        author.get("short_description") or "",
                    ),
                )
                success += 1
        except Exception:
            console.error(traceback.format_exc())
            console.error(f"{relName}  处理出错")
            error += 1
    if error == 0:
        end = console.success("作者  处理完毕", begin)
    else:
        end = console.warning(f"作者  处理完毕，共有{error}个错误", begin)
    cursor.close()
    console.log()
    return {
        "collection": "作者",
        "count": success,
        "time": f"{console.round(end - begin)}s",
    }


# 特殊处理唐诗三百首
def shisanbai(data: dict):
    content = data["content"]
    data["dynasty"] = "唐"
    result: list[dict] = []
    for group in content:
        for poet in group["content"]:
            if poet["subchapter"]:
                poet["title"] = poet["subchapter"]
            else:
                poet["title"] = poet["chapter"]
            del poet["chapter"]
            del poet["subchapter"]
            poet["tags"] = ["唐诗三百首", group["type"]]
            result.append(poet)
    return result
