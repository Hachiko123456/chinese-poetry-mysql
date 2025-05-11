# ��ʫ���Զ�¼�����ݿ�(mysql)

## ���л���

python 3.11(pipenv)

## config.json ˵��

``` jsonc
"mysql": {
	"host": "127.0.0.1",				// ��������ַ
	"user": "root",					// �û���
	"password": "123456",				// ����
	"port": "3306",					// �˿�
	"database": "test",				// ���ݿ�����
},
"table": "chinese_poetry",				// ʫ�ʱ��� !!!ע��, �������Ѵ��ڻ�ɾ���ñ�, ��ע�ⱸ��!
"tableAuthor": "chinese_poetry_author",			// ���߱��� !!!ע��, �������Ѵ��ڻ�ɾ���ñ�, ��ע�ⱸ��!
"source": "/opt/chinese-poetry",			// ��ʫ�ʸ�Ŀ¼
"files": {						// ��ʫ�ʱ��������߱�������Ϊ0ʱ, �����Ӧ���ļ�
	"data": [					// ¼�����ݵĲ���, ����Ը�����Ҫ�޸Ļ�ɾ����������
		{
			"path": "json/poet.tang.*.json",// ָ��ƥ����ļ�(Unix �ļ���ģʽƥ��)
			"dynasty": "��",		       // ָ������
			"collection": "��Ԋ",	      // ָ������
			"author": "����"		      // ��ѡ, �ֶ�ָ������
		}
	],
	"include": ["��Ԋ", "���~"],		     // ֻ�����ض���collection
	"exclude": ["�ĉ�Ӱ"],			      // �������ض���collection, ��include��Ϊ��, �������Ч
	"authors": ["ci/author.song.json"]		 // ƥ�������ļ�(Unix �ļ���ģʽƥ��)
}
```

## ʹ�÷���

> 1. ǰ������ [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry.git)

> 2. �� `config.json.sample` ���Ϊ `config.json` �����ú���ز���

> 3. ���� `start.py`

``` shell
git submodule update --init --recursive
pipenv shell
pipenv install
python ./start.py
```
