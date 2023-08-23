import json
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt,RGBColor



def json2docx(json_data, doc_file):

    document = Document()

    document.styles['Normal'].font.name = u'仿宋'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋')
    document.styles['Normal'].font.size = Pt(14)
    document.styles['Normal'].font.color.rgb = RGBColor(0,0,0)


    # 标题
    # 标题等级如1,2,3这些数字，一级标题二级标题这样
    Head = document.add_heading("",level=1)# 这里不填标题内容 
    run  = Head.add_run("民事起诉状")
    Head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run.font.name=u'宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    run.font.size = Pt(22) 
    run.font.color.rgb = RGBColor(0,0,0)
    paragraph = document.add_paragraph()


    # 添加原告信息
    for plaintiff in json_data['原告']:

        ### 公司
        if '公司名称' in plaintiff:
            
            doc = document.add_paragraph()
            doc.paragraph_format.first_line_indent = Pt(14) * 2
            doc.add_run('原告：').bold = True
            doc.add_run(f"{plaintiff['公司名称'] or '公司名称：_______'}，"
                        f"地址：{plaintiff['公司所在地'] or '________________'}。"
                        f"法定代表人/法定代理人/法人：{plaintiff['法定代表人/法定代理人/法人']['姓名'] or '法定代表人/法定代理人/法人姓名：_______'}，职务：{plaintiff['法定代表人/法定代理人/法人']['职务'] or '法定代表人/法定代理人/法人职务：______'}，联系方式：{plaintiff['法定代表人/法定代理人/法人']['联系方式'] or '法定代表人/法定代理人/法人：___________'}。")
            
            if plaintiff['委托诉讼代理人'] == '无':
                document.add_paragraph(f"无委托诉讼代理人").paragraph_format.first_line_indent = Pt(14) * 2
            else :
                document.add_paragraph(f"委托诉讼代理人：{plaintiff['委托诉讼代理人']['姓名']}，{plaintiff['委托诉讼代理人']['事务所']}。").paragraph_format.first_line_indent = Pt(14) * 2
            
        ### 个人
        else:
            doc = document.add_paragraph()
            doc.paragraph_format.first_line_indent = Pt(14) * 2
            doc.add_run('原告：').bold = True
            doc.add_run(f"{plaintiff['姓名'] or '姓名：_______'}，{plaintiff['性别'] or '性别：__'}，{plaintiff['出生日期'] or '__________'}生，"
                        f"{plaintiff['民族'] or '____' + '族'}，现住{plaintiff['住址']or '_________________'}。"
                        f"联系方式：{plaintiff['联系方式'] or '联系方式：_________'}")
            if plaintiff['委托诉讼代理人'] == '无':
                document.add_paragraph(f"无委托诉讼代理人").paragraph_format.first_line_indent = Pt(14) * 2
            else :
                document.add_paragraph(f"委托诉讼代理人：{plaintiff['委托诉讼代理人']['姓名']}，{plaintiff['委托诉讼代理人']['事务所']}。").paragraph_format.first_line_indent = Pt(14) * 2
    
    # document.add_paragraph()


    # 添加被告信息
    for defendant in json_data['被告']:

        ### 公司
        if '公司名称' in defendant:
            doc = document.add_paragraph()
            doc.paragraph_format.first_line_indent = Pt(14) * 2
            doc.add_run('被告：').bold = True
            doc.add_run(f"{defendant['公司名称'] or '公司名称：_______'}，"
                        f"地址：{defendant['公司所在地'] or '________________'}。"
                        f"法定代表人/法定代理人/法人：{defendant['法定代表人/法定代理人/法人']['姓名'] or '法定代表人/法定代理人/法人姓名：_______'}，职务：{defendant['法定代表人/法定代理人/法人']['职务'] or '法定代表人/法定代理人/法人职务：______'}，联系方式：{defendant['法定代表人/法定代理人/法人']['联系方式'] or '法定代表人/法定代理人/法人：___________'}。")
            
            if defendant['委托诉讼代理人'] == '无':
                document.add_paragraph(f"无委托诉讼代理人").paragraph_format.first_line_indent = Pt(14) * 2
            else:
                document.add_paragraph(f"委托诉讼代理人：{defendant['委托诉讼代理人']['姓名']}，{defendant['委托诉讼代理人']['事务所']}。").paragraph_format.first_line_indent = Pt(14) * 2
            
        else:
            doc = document.add_paragraph()
            doc.paragraph_format.first_line_indent = Pt(14) * 2
            doc.add_run('被告：').bold = True
            doc.add_run(f"{defendant.get('姓名', '姓名：_______')}，{defendant.get('性别', '性别：__')}，{defendant.get('出生日期', '__________')}生，"
                        f"{defendant.get('民族', '____族')}，现住{defendant['住址']or '_________________'}。"
                        f"联系方式：{defendant.get('联系方式', '联系方式：_________')}")
            if defendant['委托诉讼代理人'] == '无':
                document.add_paragraph(f"无委托诉讼代理人").paragraph_format.first_line_indent = Pt(14) * 2
            else:
                document.add_paragraph(f"委托诉讼代理人：{defendant['委托诉讼代理人']['姓名']}，{defendant['委托诉讼代理人']['事务所']}。").paragraph_format.first_line_indent = Pt(14) * 2
            
    document.add_paragraph()


    # 添加诉讼请求
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.first_line_indent = Pt(14) * 2
    paragraph.add_run('诉讼请求：').bold = True
    if json_data['诉讼请求'] == "null":
        document.add_paragraph('无诉讼请求！\n').paragraph_format.first_line_indent = Pt(14) * 2
    else:
        request_text = json_data['诉讼请求']
        # 根据"\n"拆分为多行
        lines = request_text.split('\n')
        # 对每一行进行处理
        for line in lines:
            paragraph = document.add_paragraph(line)
            paragraph.paragraph_format.first_line_indent = Pt(14) * 2
    document.add_paragraph()

    # 添加事实和理由
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.first_line_indent = Pt(14) * 2
    paragraph.add_run('事实和理由：').bold = True
    if json_data['事实理由'] == "null":
        document.add_paragraph('无事实和理由！\n').paragraph_format.first_line_indent = Pt(14) * 2
    else:
        request_text = json_data['事实理由']
        # 根据"\n"拆分为多行
        lines = request_text.split('\n')
        # 对每一行进行处理
        for line in lines:
            paragraph = document.add_paragraph(line)
            paragraph.paragraph_format.first_line_indent = Pt(14) * 2
    document.add_paragraph()

    # 添加证据和证据来源，证人姓名和住所
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.first_line_indent = Pt(14) * 2
    paragraph.add_run('证据和证据来源，证人姓名和住所：').bold = True
    if json_data['证据'] == "null":
        document.add_paragraph('无证据和证据来源，证人姓名和住所！\n').paragraph_format.first_line_indent = Pt(14) * 2
    else:
        request_text = json_data['证据']
        # 根据"\n"拆分为多行
        lines = request_text.split('\n')
        # 对每一行进行处理
        for line in lines:
            paragraph = document.add_paragraph(line)
            paragraph.paragraph_format.first_line_indent = Pt(14) * 2

    # 结尾部分
    paragraph = document.add_paragraph()
    paragraph.add_run('此致').bold = True
    paragraph.paragraph_format.first_line_indent = Pt(14) * 2

    paragraph = document.add_paragraph()
    paragraph.add_run(json_data['法院']).bold = True
    document.add_paragraph('\n附：本起诉状副本2份')
                        
    # 起诉人(签名)
    paragraph = document.add_paragraph()
    paragraph.add_run('起诉人(签名)\n').bold = True
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 日期
    if json_data['日期'] is None:
        date_paragraph = document.add_paragraph()
        date_paragraph.add_run('日期：____________').bold = True
    else:
        date_paragraph = document.add_paragraph()
        date_paragraph.add_run(json_data['日期']).bold = True
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 保存文档
    document.save(doc_file)


if __name__ == '__main__':
    json_1 = 'person.json'

    with open(json_1, 'r',encoding='utf8') as f:
        json_data = json.loads(f.read())

    json2docx(json_data, 'demo.docx')