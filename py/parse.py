import json
import requests

import os


def download_image(url, local_filename=None):
    """
    下载图片并保存到本地。
    
    :param url: 图片的URL地址
    :param local_filename: 本地保存的文件名（含路径），如果不提供则默认使用URL的最后一部分作为文件名
    :return: 图片保存的本地路径
    """
    if local_filename is None:
        # 如果没有指定文件名，则从URL中提取
        local_filename = url.split('/')[-1]
    
    # 发送GET请求获取图片数据
    response = requests.get(url, stream=True)
    
    # 确保请求成功
    if response.status_code == 200:
        # 以二进制写模式打开文件
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024): 
                # 使用iter_content逐步写入文件，这样可以处理大文件
                if chunk:  # 过滤掉keep-alive新行
                    file.write(chunk)
        return local_filename
    else:
        print(f"Failed to retrieve image, status code: {response.status_code}")
        return None

def process_json_files(dir_path):
    imageInfoList = []
    imageDir = "./images"
    os.makedirs(imageDir, exist_ok=True)    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):  # 确保文件是.json文件
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        dataList = data["list"]
                        for i, itemData in enumerate(dataList) :
                            imageTitle = itemData["title"]
                            imageContent = itemData["content"]
                            imageId = itemData["id"]
                            imageUrl = itemData["image"]
                            localImagePath = f"./images/{imageId}.jpg"
                            download_image(imageUrl, localImagePath)
                        # 在这里处理data，例如打印内容
                        # print(f"Processing {file_path}:")
                        # print(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {file_path}: {e}")

# parsed_json = json.loads(json_string)

process_json_files('./py/')