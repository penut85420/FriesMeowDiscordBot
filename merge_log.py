import os
import contextlib
from datetime import datetime


def walk_dir(path):
    for dir_path, _, file_list in os.walk(path):
        for file_name in sorted(file_list):
            full_path = os.path.join(dir_path, file_name)
            yield full_path, file_name

newlog = dict()

for fullPath, fileName in walk_dir('./log'):
    with open(fullPath, 'r', encoding='UTF-8') as fin:
        for line in fin:
            try:
                # 2019-06-05 04:53:11
                ndate = line[:19]
                date = datetime.strptime(ndate, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
                arr = newlog.get(date, list())
                arr.append(line)
                newlog[date] = arr
            except:
                arr = newlog.get(date, list())
                arr.append(line)
                newlog[date] = arr

with contextlib.suppress(Exception):
    os.mkdir('./log-merge')

for k in newlog:
    with open('./log-merge/%s.log' % k, 'w', encoding='UTF-8') as fout:
        fout.writelines(newlog[k])
