import re
import os
import json
import pandas as pd


def get_project_path(project_name='lawgpt_cp'):
	# 获取当前文件的绝对路径
	p_path = os.path.abspath(os.path.dirname(__file__)) 
	# 通过字符串截取方式获取
	return p_path[:p_path.index(project_name) + len(project_name)]


def flatten_dictionary(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# 将展平的 DataFrame 转换回带字典的 JSON 格式
def unflatten_dataframe(df, sep='_'):
    result = {}
    for col in df.columns:
        parts = col.split(sep)
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = df[col][0]
    return result

def json2file(yuangao,beigao,second_state):
    json_data = {
                "原告": yuangao,
                "被告": beigao
                }
    json_data.update(second_state)

    project_path = get_project_path()
    generate_json_file(json_data, os.path.join(project_path,'output','json_folder','person.json'))

def generate_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



def extract_json_from_string(text,outfile=None):
    '''
    请注意，上述示例假定只有一个有效的JSON文本。如果存在多个JSON文本，将只提取第一个匹配项。
    
    '''
    text = text.replace("None", "null").replace("none", "null")

    patterns = [r'```json([\s\S]*)```',r'({[\s\S]*})',]

    for pa in patterns:
        match = re.search(pa, text)
        if match:
            break

    if match:
        json_text = match.group(1).strip()
        # print(json_text)
        try:
            data = json.loads(json_text)
            if outfile:
                generate_json_file(data,outfile)
            return data
            
        except json.JSONDecodeError as e:
            # print(f"Invalid JSON format: {e}")
            res = f"Invalid JSON format: {e} \n {json_text}"
            return res



# 递归遍历 JSON 数据，将值为 null 的键值对的值设置为"无"，但不包含有内容的键值对
def transverse_on_json(json_data):
    """遍历json dict，寻找缺失值为空

    Args:
        json_data (_type_): _description_

    Returns:
        _type_: _description_
    """    
    keys_get = []
    keys_miss = []

    for key, value in json_data.items():
        if isinstance(value, dict):
            keys_get_tmp,keys_miss_tmp = transverse_on_json(value)
            if keys_miss_tmp:
                keys_miss.append(key)
            else:
                keys_get.append(key)
        elif value:
            keys_get.append(key)
        elif value is None:
            keys_miss.append(key)
    return keys_get,keys_miss



if __name__ == '__main__':
    text = ''' hel{"text":"school","name":"lily"}'''
    text = person_json_template="""{ "姓名": null, "性别": null, "出生日期": null, "民族": null, "住址": null, "联系方式": null, "身份证号": null, "法定代理人": {"姓名": null, "性别": null, "出生日期": null, "民族": null, "住址": null, "联系方式": null, "身份证号": null}, 委托诉讼代理人": { "姓名": null, "事务所": null } }"""
# 

    # status = extract_json_from_string(text,'output.json')
    # with open('output.json','r') as f:
    #     data = json.load(f)
    # print(type(data),data)
    # print()

    # get,miss = transverse_on_json(data)
    # print(get)

    # print(miss)
    data = '{"住址": "河北省保定市阳光大街与东风路交叉口仁和公寓底商第12号"}'

    a = extract_json_from_string(text)
    print(a)
