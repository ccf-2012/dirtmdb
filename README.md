# DirTMDb
将目录中的第一个 .nfo 文件中的 tmdbid 提取出来，将目录名改名为 Plex 标识，如 {tmdb-12345}


## 使用
```
python3 dirtmdb.py -h

usage: dirtmdb.py [-h] [-i] [-t] [-s SUCCESS_LIST] dir

rename folder with tmdbid.

positional arguments:
  dir                   folder path.

options:
  -h, --help            show this help message and exit
  -i, --imdb            rename folder with IMDb id.
  -t, --tmdb            rename folder with TMDb id.
  -s SUCCESS_LIST, --success-list SUCCESS_LIST
                        output success list.
```

## 例子
```
python3 dirtmdb.py  /gd/movie/other -s sus.txt
```
* 如果要改名为带 IMDb 后缀：
```
python3 dirtmdb.py  --imdb /gd/movie/other

```

