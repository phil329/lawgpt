# 对话开始
start_chat="您好，我是星火起诉书生成助手，很高兴为您服务！\n\n 我现在需要**原告**的信息。\n\n请问原告是 *自然人（个人）* 还是 *非自然人（公司）* 呢？"

# {"姓名": null, "性别": null json Template#ull, "住址": null, "联系方式": null, "身份证号": null}
person_json_template="""{'姓名': null, '性别': null, '出生日期': null, '民族': null, '住址': null, '联系方式': null, '身份证号': null, "法定代理人": null, '委托诉讼代理人': {'姓名': null, '事务所': null}}"""
company_json_template="""{ "公司名称": null, "公司所在地":  null, '统一社会信用代码': null, "法人": { "姓名": null, "职务": null, "联系方式": null},"委托诉讼代理人": {"姓名": null,"事务所": null}}"""

# Prompt 
gudie_1_2="下面有段客户的文字，请判断客户是需要以个人的名义还是公司的名义起诉，如果是个人请输出1，否则输出2。记住只需1或2。提问和回答如下:"
# person_json_template="""{ "姓名": null, "性别": null, "出生日期": null, "民族": null, "住址": { "省份": null, "城市": null, "区/县": null }, "联系方式": null, "委托诉讼代理人": { "姓名": null, "事务所": null } }"""
guide_agent="""客户将告诉你是否需要委托代理人。若用户没有或者不需要委托代理人，则不变；如有请填入下面的json模板中"""+person_json_template+"""提问和回答如下: """
address_complete_json="""，请帮我补全以上住址使其包含省市区信息，并以如下json格式输出:{"住址":""}"""
# gudie_json="""你是一名精通民事起诉的律师。客户将给你一段文字，需要你提取全部关键信息，不丢失信息，填充到下面的json文件中，并符合json语法，记住只需把这个json文件输出给我。"""+json_template+"""提问和回答如下: """
gudie_yuangao_person_json="""你是一名精通民事起诉的律师。客户将给你一段文字，需要你提取全部关键信息，不丢失信息，填充到下面的json文件中，并符合json语法，记住只需把这个json文件输出给我。"""+person_json_template+"""提问和回答如下: """
gudie_beigao_person_json="""你是一名精通民事起诉的律师。客户将给你一段文字，需要你提取被告人的全部关键信息，不丢失信息，填充到下面的json文件中，并符合json语法，记住只需把这个json文件输出给我。"""+person_json_template+"""提问和回答如下: """

gudie_yuangao_company_json="""你是一名精通民事起诉的律师。客户将给你一段文字，需要你提取全部关键信息，不丢失信息，填充到下面的json文件中，并符合json语法，记住只需把这个json文件输出给我。"""+company_json_template+"""提问和回答如下: """
gudie_beigao_company_json="""你是一名精通民事起诉的律师。客户将给你一段文字，需要你提取被告公司的全部关键信息，不丢失信息，填充到下面的json文件中，并符合json语法，记住只需把这个json文件输出给我。"""+company_json_template+"""提问和回答如下: """

gudie_again="你是一名精通民事起诉的律师。客户将给你一段文字，需要你判断是否客户需要继续加入原告信息，如果需要请输出1，否则输出2。记住只需1或2。提问和回答如下:"
gudie_again_2="你是一名精通民事起诉的律师。客户将给你一段文字，需要你判断是否客户需要继续加入被告信息，如果需要请输出1，否则输出2。记住只需1或2。提问和回答如下:"
gudie_question="""你是一名精通民事起诉的律师。已经有的诉讼书内容的json文件如下。"""+person_json_template+"""请输出一句话，继续引导用户补全信息"""

gudie_second_json1="""你是一名精通民事起诉的律师。客户将给你一段文字，仅需提取案由、诉讼请求、事实和理由。如有证据，请说明证据和证据来源；请注意，用户说明中，若无证据请勿编纂留空。
提问和回答如下:"""

gudie_second_json2="""把这段话填入这份json文件中。不要修改原句，也不要生成新的键。
{ "案由": null, 诉讼请求": null, "事实和理由": null, "证据": { "证据和证据来源": null, "证人姓名和住所": null } }"""
second_guide="好的，我已经知道您的原告的基本信息了。请问您可以继续提供被告人的信息吗？包括姓名、性别、出生日期、民族、住址、联系方式"
third_guide="好的，我已经知道您的所有基本信息了。能进一步给出您的诉讼请求吗？"

gudie_second_step0="""请根据用户输入判断案由类型，案由类型一般有机动车交通事故责任纠纷、民间借贷纠纷、离婚纠纷、合同纠纷、买卖合同纠纷、金融借款合同纠纷、借款合同纠纷、劳动争议、房屋买卖合同纠纷、建设工程施工合同纠纷、土地经营权纠纷等，如果不是以上案由类型，请自行判断，请注意一定要以以下json格式输出案由类别：{"案由":""}，用户的输入是："""
guide_second_step1="""以上是可以参考的诉讼请求模板，请根据以下原告描述内容生成诉讼请求部分，注意严格按照原告意思，不要随意篡改，不要出现第一第二第三人称。请注意分点阐述，原告:"""
# 事实和请求
guide_second_step2="""以上是可以参考的事实与理由模板，请根据以下原告描述内容生成事实与理由部分，注意严格按照原告意思，不要随意篡改，不要出现第一第二第三人称。请注意分点阐述，原告:"""
# 证据
gudie_second_step3="""你是一名精通民事起诉的律师。请从下面客户输入的文字中提取客户说的证据内容，注意只需要输出证据"""
gudie_second_step4="""你是一名律师，我会告诉你被告人的住址，请列举他们住所地的人民法院，并只输出法院名称。例如福建省福州是仓山区人民法院这样的管辖法院。住址是"""
gudie_second_step5="""你是一名精通民事起诉的律师。请从下面客户输入的文字中提取客户说的法院信息"""

# 为一段对话生成标题
summary_chat_prompt = '我给你提供一段对话，请你帮我生成20字以内的标题，请体现文字具体信息和特点。'

# 总结相关法律知识的知识卡片
knowledge_comment_prompt = '你是知识提示卡片，请回答涉及到的相关法律以及具体条款，分条简单阐述，大概的结构:“涉及的法律和具体条款:1.某个法律的某一条规定了什么什么什么\n2. 某个法律的某一条规定了什么什么什么\n”。请注意无需体现与案件有关信息。'


# 寻找相关案例的判罚情况
related_result_prompt = '假如你是一个法官，请找出与下面诉讼请求相似内容的某一个案件的判罚情况，要给出案件、判罚情况、事实和理由以及证据。请注意不要给出下面案件的判罚及相关信息。'


#判断是个人还是公司
res_judge_p_1=["个人","1","我自己","自然人"]
res_judge_c_2=["公司","企业","2","非自然人","不是自然人"]


#判断是否继续添加信息
res_judge_go_1=["继续","再加一个","是","需要","要的","行呀","添加","可以"]
res_judge_no_2=["不继续","不用","没有了","否","是我自己","不需要","不要","不添加了","不"]
res_judge_jj_3=["手机号码是","代理人是","汉族","性别"]

# 民间借贷—事实和理由提示
debt_usr_reason_example = "\n事实与理由：原告经人介绍认识被告，后被告以店铺经营周转为由多次找原告借钱。2023年8月24日，被告为还银行贷款向原告处借款50000元，借款期限为3个月，双方约定按年利率3%支付利息，承诺承担连带保证责任。基于对被告的信任，原告以现金的方式向被告交付了借款。后原告因自己急于用钱多次向被告催要借款，但被告以各种理由拖延，拒不归还借款。为了维护原告的合法权利，特向贵院提起诉讼。"

# 民间借贷—诉讼请求提示
debt_usr_request_example = "\n诉讼请求：\n1. 请求被告归还借款50000元及利息；\n2. 请求判令保证人请在此输入保证人姓名对借款本息承担连带保证责任；\n3、请求判令本案诉讼费用由被告承担。"

debt_usr_reason_prompt = "1. 双方认识过程\n2. 被告借款的原因：（还银行贷款/投资需要/买房/买车/资金周转/其他原因）\n 3. 被告借款金额（元）\n 4. 借款的交付方式：现金/银行转账/网络电子汇款/票据支付\n 4. 被告借款的时间\n 5. 您与被告约定的借款期限？（月）\n 6. 是否约定了利息。如有，请说明约定的利息（年利率%）\n 7. 合同是书面还是口头订立（书面合同/口头约定）\n 8. 是否向被告催要过\n 9. 合同法中是否约定了保证人？如有，保证的方式（一般保证/连带责任保持），是否起诉保证人"

debt_usr_request_prompt = "1. 本金和利息\n 2. 是否起诉保证人\n 3. 诉讼费律师费等"

traffic_usr_reason_prompt ="1. **当事人类型：** 机动车驾驶员 / 非机动车驾驶员（类型：电动自行车 / 自行车 / 三轮车） / 乘车人 / 行人\n2. **交警部门责任认定：**\n\t1) 交警部门是否做出责任认定？\n\t\ta) 被告方当事人在事故中的责任（无责任，次要责任，同等责任，主要责任，全部责任，双方无责任） \n\t\t\ti. 是否接受交警部门的认定？ \n\t\tb) 交警部门未作认定\n3. **事故发生时间：** xx年xx月xx日\n4. **是否协商过赔偿事宜：**\n5. **对方车辆是否购买汽车强制保险：**\n\t1) 已购买：保险公司是否已赔偿相关损失（已赔偿 / 未赔偿）\n\t2) 未购买\n\t3) 不清楚"

traffic_usr_request_prompt ="**当事人损失包括：**\n\t1) 财产损失（车辆损失，其他财产损失）：\n\t\ta) 财产损失（施救花费，维修花费，车辆停运导致的损失，使用替代交通工具产生的费用，车辆彻底损坏的损失，其他财产的损失）\n\t\tb) 财产损失金额（元）\n\t2) 人身损失：\n\t\ta) 人身损失（医疗费，交通费，住宿费，住宿伙食补助费，营养费，护理费，误工费，鉴定费，后续治疗费，残疾赔偿金，被扶养人生活费，精神损失抚慰金，其他）\n\t\tb) 人身损害金额（元）\n\t\tc) 是否住院： \n\t\t\ti. 住过（住院时间、出院时间） \n\t\tii. 没住过 \n\t\td) 有无做过伤残等级鉴定"

# 机动车—事实和理由提示
traffic_usr_reason_example = "\n事实与理由:\n2008年5月5日 时许，被告一驾驶轿车沿横滨之路行驶至凤城五路口处时，因速度过快、未注意观察，将原告撞伤，发生交通事故(写事故发生的时间、地点、经过)。后经认定被告一对事故发生负全部责任(写责任认定)。事发后，原告被送 医院接受治疗(写治疗经过)。经查证，被告一驾驶的车辆在被告二处投保了保险，事故发生在保险期内(写车辆投保情况)。事故发生后，各方就赔偿事宜协商未果，为维护原告的合法权益，特提起诉讼，请贵院依法支持诉请。"

# 机动车—上述请求提示
traffic_usr_request_example = "\n诉讼请求:\n1、请求判决两被告赔偿原告的医疗费5000元，交通费500元，住宿费2678元，财产损失2456元，残疾辅助工具费678元，伙食补助费56元，合计4567876元。残疾赔偿金、被抚养人生活费、精神损害抚慰金、误工费、护理费、营养费、鉴定费等具体赔偿数额，待司法鉴定后再行主张。\n2、请求法院判决被告二优先赔偿原告的损失;超出部分由被告一承担。\n3、请求法院依法判决本案诉讼费用、鉴定费用由被告承担。"

# 离婚—事实和理由提示
divorce_usr_reason_prompt = "事实和理由:\n原告与被告 年 月份相识，后于 年 月 日登记结婚， 年生育一子  (婚恋及家庭情况)，由于婚前双方实际相处时间不多，对彼此的了解不深，在婚后长达 年的生活中，被告时常因家庭琐事频繁殴打、辱骂原告，婚内还与多名异性保持不正当关系，给原告及家庭带来诸多的伤害。(写感情破裂的表现)\n原告认为，由于原被告在婚后没有建立稳固的夫妻感情，被告时常有家庭暴力行为，还与异性发生不正当关系，导致双方感情已经完全破裂、毫无和好可能，正常的家庭生活中原告的个人安全也得不到保障，理当结束这段婚姻。(离婚原因)\n综上所述，为维护原告的合法权益，为保护原告的婚姻自由权利，特向法院提起诉讼，请求法院依法支持原告的全部诉讼请求。"

# 离婚-诉讼请求提示
divorce_usr_request_prompt = "诉讼请求:\n1、请求法院依法判决原被告离婚;(离婚)\n2、请求判决儿女  归被告抚养，原告不承担抚养费;(子女抚养问题)\n3、请求法院依法分割位于  号 幢 单元  室的房屋;(财产分割，可以逐个列出)\n4、请求判决被告赔偿原告精神损害抚慰金  万元;(无过错方可以主张家暴精神赔偿)\n5、请求判决本案诉讼费用由被告承担。(诉讼费)"