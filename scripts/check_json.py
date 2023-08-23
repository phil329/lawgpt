import json

def filter_null_values(json_text):
    # 解析输入的 JSON 文本
    data = json.loads(json_text)

    # 递归遍历 JSON 数据，将值为 null 的键值对的值设置为"无"，但不包含有内容的键值对
    def recursive_filter(data):
        filtered_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                nested_filtered_data = recursive_filter(value)
                if nested_filtered_data:
                    filtered_data[key] = nested_filtered_data
            elif isinstance(value, list):
                nested_filtered_data = []
                for item in value:
                    if isinstance(item, dict):
                        nested_item = recursive_filter(item)
                        if nested_item:
                            nested_filtered_data.append(nested_item)
                if nested_filtered_data:
                    filtered_data[key] = nested_filtered_data
            elif value is None:
                filtered_data[key] = "无"
        return filtered_data

    # 将值为 null 的键值对的值设置为"无"，但不包含有内容的键值对
    filtered_data = recursive_filter(data)

    # 将筛选后的数据转换回 JSON 文本
    filtered_json = json.dumps(filtered_data, ensure_ascii=False)

    return filtered_json


# 示例输入
json_text = '''
{
  "案由": null,
  "原告": {
    "姓名": "王仁淞",
    "性别": "男",
    "出生日期": null,
    "民族": null,
    "其他信息": null,
    "住址": null,
    "联系方式": null
  },
  "法定代理人/指定代理人": {
    "姓名": null,
    "其他信息": null
  },
  "委托诉讼代理人": {
    "姓名": null,
    "其他信息": null
  },
  "被告": {
    "姓名": null,
    "其他信息": null
  },
  "结尾": {
    "法院名称": null,
    "附件": null,
    "签名": null,
    "日期": null
  }
}
'''

# 调用函数进行筛选并将值为 null 的键值对的值设置为"无"，但不包含有内容的键值对
filtered_json = filter_null_values(json_text)

# 输出结果
print(filtered_json)