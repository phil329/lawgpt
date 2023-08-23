import SparkApi

# 以下密钥信息从控制台获取
appid = "f54bca1a"  # 填写控制台中获取的 APPID 信息
api_secret = "ZGJmMjY3YWFmNGY5N2Q1YWMwOGZlMjFh"  # 填写控制台中获取的 APISecret 信息
api_key = "2e7516edf376713eb5d99fc812a87ed5"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“generalv2”
domain = "generalv2"  # v2.0版本

# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

text = [
    # {'role': "user", 'content': '你好，你能够帮我生成一份起诉状吗？'},
    # {'role': "assistant", 'content': '您好，我是星火，我可以帮您生成一份起诉状，请先给我几份模板。'},
    # {'role': "user", 'content': '’‘好的，这是一份模板：'
    #                             '民事起诉状'
    #                             '原告：姓名，性别：   ，    年    月    日 出生，   族，住址： 省  市  区  镇  村 组 号'
    #                             '联系电话：        。'
    #                             '被告一： 姓名   ，性别：  ，    年    月    日 出生，  族，住址： 省  市  区  路  小区   号楼  单元  室。'
    #                             '联系电话：        。'
    #                             '被告二：    保险股份有限公司        分公司，住所地：  省   市   区   路   号   座   层  。'
    #                             '负责人：        。职务：        。'
    #                             '联系电话：        。'
    #                             '案由：机动车交通事故责任纠纷'
    #                             '诉讼请求：'
    #                             '一、依法判决被告一赔偿原告各项损失共计    元（其中：医疗费    元、后续医疗费    元、误工费    元、伙食费    元、护理费    元、交通费    元、住宿费    元、营养费    元、残疾赔偿金    元、残疾辅助器具费    元、被抚养人生活费    元、精神损害抚慰金    元）；'
    #                             '二、依法判决被告一赔偿原告车辆损失共计    元；'
    #                             '三、依法判决被告二在责任保险赔偿限额范围内对被告一的上述赔偿义务承担连带赔偿责任；'
    #                             '四、本案诉讼费由被告承担。'
    #                             '事实及理由：'
    #                             '一、事故概况'
    #                             '   年   月   日，原告驾驶车牌号为   的小轿车与被告一驾驶的  汽车发生交通事故，造成原告人身与财产损害。事故地点为： ；事故原因为： 。该事故已由  市  区交通警察支队做出编号为  的道路交通事故认定书，认定被告承担事故全部责任，原告不承担事故责任。'
    #                             '二、保险情况'
    #                             '事故发生前，被告车辆已在被告二购买了交通事故责任强制保险和商业险。 '
    #                             '原告认为：被告一应就交通事故造成原告的损失予以赔偿，被告二应当在保险责任范围内承担连带责任。为维护原告合法权益，特向贵院具状起诉，请求支持原告请求。'
    #                             ''
    #                             '此致'
    #                             '人民法院'
    #                             '具状人（签名或盖章）：                     '
    #                             '        年        月        日'''},
    # {'role': 'assistant', 'content': '好的我都了解了，我会按照你的模板来生成起诉状'},
    # {'role': 'user', 'content': '让我们开始吧，请一步步引导我填写起诉状模板上所需要的信息，最后生成一份起诉状'},
    # {'role': "user", 'content': '帮我把我写的地址填入下面的住址中，你需要先确定我给的是哪个省哪个城市哪个区或者县，如果城市或者省份是{“上海”、“北京”、“天津”、“重庆”}中的任一城市，则“省份”和“城市”都填入该城市，如果不是这四个，请把刚刚确认的那个省哪个市哪个区或者县和具体的地址填入："住址": { "省份": null, "城市": null, "区/县": null, "其他": null } 比如一个输入是"甘肃静安县"，输出为"住址": { "省份": 甘肃省, "城市": 平凉市, "区/县": 静安县, "其他": null }，我的输入是：栖霞区仙林大道163号'},
    # {'role': "assistant", 'content': '"住址": { "省份": "江苏省", "城市": "南京市", "区/县": "栖霞区", "其他": 仙林大道163号 }'},
]


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text



if __name__ == '__main__':
    text.clear
    # text_start_assistant = '您好，我是星火，我可以帮您生成一份起诉状，请先告诉我您的姓名、年龄、民族、联系方式和住址'
    text_start_assistant = '您好，我是星火，有什么可以帮你的吗'
    print("星火:" + text_start_assistant, end="")
    getText("assistant", text_start_assistant)
    while (1):
        Input = input("\n" + "我:")
        question = checklen(getText("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        getText("assistant", SparkApi.answer)
        # print(str(text))


