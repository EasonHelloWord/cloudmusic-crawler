import requests
import json
import time
import os
import threading
import ast
import py7zr

def info(song_id):
    # song_id = "509313150"

    # 请求歌曲详情API的URL
    url = "https://music.163.com/api/song/detail?ids=[{0}]"

    # 请求头信息
    headers = {
        "Referer": "https://music.163.com/song?id={0}".format(song_id),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # 发送请求获取歌曲详情数据
    try:
        response = requests.get(url.format(
            song_id), headers=headers, timeout=5)
    except:
        return {'code': 404}
    data = response.text
    # 将返回的数据解析为JSON格式
    json_data = json.loads(data)
    return (json_data)


def data(song_id):
    # 请求评论数据API的URL
    url = "https://music.163.com/api/v1/resource/comments/R_SO_4_{0}?limit=20&offset=0"

    # 请求头信息
    headers = {
        "Referer": "https://music.163.com/song?id={0}".format(song_id),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # 发送请求获取评论数据
    try:
        response = requests.get(url.format(
            song_id), headers=headers, timeout=5)
    except:
        return {'code': 404}
    data = response.text
    # 将返回的数据解析为JSON格式
    json_data = json.loads(data)

    # # 获取评论数量
    # comment_count = json_data["total"]

    return (json_data)


def start(start, end):
    song_id = start
    while song_id < end:
        if os.path.exists(f'./data/{song_id}.json'):
            # print(f'{song_id}已经爬取过了')
            song_id += 1
            continue
        now = f"{time.time():.0f}"
        # info_data = info(song_id)
        # info_data['time'] = now
        # with open(f"./info/{song_id}.json", "w", encoding="utf-8") as f:
        #     json.dump(info_data, f, ensure_ascii=False, indent=4)
        data_data = data(song_id)
        data_data['time'] = now
        e = 0
        try:
            with open(f"./data/{song_id}.json", "w", encoding="utf-8") as f:
                json.dump(data_data, f, ensure_ascii=False, indent=4)
        except:
            e += 1
            if e <= 5:
                print(f'{song_id}写入异常，第{e}次尝试')
                continue
            else:
                print(f'{song_id}写入失败')
                open("./error.txt", "a",
                     encoding="utf-8").write(f'{str(song_id)}\n')
        if data_data['code'] == 200:
            # if int(data_data.get('total', 0)) >= 1000:
            #     print(f'{song_id}加入选择范围')
            #     open("./info.txt", "a",
            #          encoding="utf-8").write(f'{str(song_id)}\n')
                # info_data = info(song_id)
                # info_data['time'] = now
                # e = 0
                # try:
                #     with open(f"./info/{song_id}.json", "w", encoding="utf-8") as f:
                #         json.dump(info_data, f, ensure_ascii=False, indent=4)
                # except:
                #     e += 1
                #     if e <= 5:
                #         print(f'{song_id}写入异常，第{e}次尝试')
                #         continue
                #     else:
                #         print(f'{song_id}写入失败')
                #         open("./error.txt", "a",
                #          encoding="utf-8").write(f'{str(song_id)}\n')
                # if info_data['code'] == 200:
                #     print(f'爬取{song_id}成功')
                #     song_id += 1
                #     continue
                # elif info_data['code'] == 406:
                #     os.remove(f"./info/{song_id}.json")
                #     print(f'{song_id}频繁，一分钟后重新请求')
                #     time.sleep(60)
                #     continue
                # else:
                #     open("./error.txt", "a",
                #          encoding="utf-8").write(f'{str(song_id)}\n')
                #     os.remove(f"./info/{song_id}.json")
                #     print(f'爬取{song_id}失败')
                #     print(info_data)
                #     song_id += 1
                #     continue

            print(f'爬取{song_id}成功')
            song_id += 1
            continue
        elif data_data['code'] == 406:
            os.remove(f"./data/{song_id}.json")
            print(f'{song_id}频繁，一分钟后重新请求')
            time.sleep(60)
            continue
        else:
            open("./error.txt", "a",
                 encoding="utf-8").write(f'{str(song_id)}\n')
            os.remove(f"./data/{song_id}.json")
            print(f'爬取{song_id}失败')
            print(data_data)
            song_id += 1
            continue
        # if info_data['code'] == 200 and data_data['code'] == 200:
        #     print(f'爬取{song_id}成功')
        #     song_id += 1
        # elif info_data['code'] == 406:
        #     os.remove(f"./info/{song_id}.json")
        #     os.remove(f"./data/{song_id}.json")
        #     print(f'{song_id}频繁，一分钟后重新请求')
        #     time.sleep(60)
        #     continue
        # else:
        #     open("./error.txt", "a",
        #          encoding="utf-8").write(f'{str(song_id)}\n')
        #     os.remove(f"./info/{song_id}.json")
        #     os.remove(f"./data/{song_id}.json")
        #     print(f'爬取{song_id}失败')
        #     print(info_data)
        #     print(data_data)
            # song_id += 1


def divide_range(x1, x2, n):
    # 计算每个区间的大小
    interval_size = int((x2 - x1) / n)

    # 初始化列表
    result = []

    # 遍历所有区间，计算区间的起始值和结束值，并将其作为元组添加到列表中
    for i in range(n):
        start = x1 + i * interval_size
        end = start + interval_size
        result.append((start, end))

    return result


if __name__ == "__main__":
    with open('list.txt', 'r') as f:
        content = f.read()

    id_list = ast.literal_eval(content)
    for starts,ends in id_list:
        ns = 50
        a = divide_range(starts, ends+1, ns)
        threads =[]
        for x, y in a:  # *100
            print(f'创建任务{x}-{y}')
            t = threading.Thread(target=start, args=(x, y))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        first_item = id_list.pop(0)

        
        

        # 定义文件夹路径和 7z 文件名
        folder_path = './data'
        archive_name = f"./end/{starts}-{ends}.7z"

        # 打包文件夹内的所有文件到 7z 文件
        with py7zr.SevenZipFile(archive_name, 'w') as archive:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    archive.write(filepath, os.path.relpath(filepath, folder_path))

        # 删除文件夹内的所有文件
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                os.remove(os.path.join(dirpath, filename))



        time.sleep(10000)
        with open('list.txt', 'r') as f:
            content = f.write(id_list)
        print("完成：", first_item)