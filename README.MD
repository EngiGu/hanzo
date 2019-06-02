## config intro
    - 整个项目有 `doom`, `crawler`, `extractor` 三个部分, `extractor`位于 `crawler`下， 是独立的模块
    - `doom` 基于公司项目`shield`

    - `spiders` -> `crawler/config.py`
    -  `bloom` ->  `bloom/config.py`
    -  `extractor` ->  `extractor/config.py`
    -  `doom` ->  `doom/settings/config.py`


## type intro
```
    1: 'import task',
    2: 'parse to type2',
    3: 'parse to type1',
    4: 'parse type1 error',
    5: 'parse type2 error'
```
    - 单个站点优先级顺序：2, 3, 1, 4, 5 

## type1 type3 type4 stru
```
        {
            'page': 100,
            'site': 'dajie',
            'type': 1/3/4,
            'keyword': 'xxxxxxxxxxxxx'
            .....
        }

```
    - 以上字段不可少, type1翻页解析出来的会带上`origin_task`字段标记源任务

## type2 type5  stru
```
        {
            'site': 'dajie',
            'type': 2/5,
            'url': 'xxxxxxxxxxxxx'
            .....
        }

```
    - 以上字段不可少， type1解析出来的会带上`origin_task`字段标记源任务

## spiders task http api stru
    - get:  `http://127.0.0.1:3333/task?site=dajie`, `site`是必填字段, 返回格式如下：
    ```
        {
        code: 0,
        msg: "success",
        task: "{}",  # str
        }
    ```
    - post: `http://127.0.0.1:3333/task`, body格式如下：
    ```{
        'site': 'dajie', 
        'task': 'task',  #str
        'type': 1
        }
    ```


## rabbitmq store stru
```
        {"site": site, "type": type, "content": content, "curr_task": curr_task}

```
    - 字段不可少，推送和接受都采用str

## parse list stru
```
        {
            "resume_list": [{'url':'xxx', 'hashed_key': 'yyy',....}, {}],
            "current_page": 1,
            "last_page": 1
        }
```
    - `hashed_key` 和 `url` 是必须字段


