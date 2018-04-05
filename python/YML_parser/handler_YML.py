import re

def categories(*data):
    """
     СПИСОК СЛОВАРЕЙ , в каждом
	 ID категории , ID - родительской категории(если есть) и текст
    """

    categor   =  re.compile(r'<categories>.+?</categories>', re.S)
    category  =  re.compile(r'<category.+?</category>',re.S)
    Id        =  re.compile(r'(?<=id=").+?(?=")',re.S)
    ParrentId =  re.compile(r'(?<=parentId=").+?(?=")',re.S)
    text      =  re.compile(r'(?<=">).+?(?=</)',re.S)

    output=[]
    if data:
        cat=categor.search(data[0]).group()
        for part in category.finditer(cat):

            part=part.group()
            if ParrentId.search(part):
                tmp=ParrentId.search(part).group()
            else:tmp=''
            output.append({'Id':Id.search(part).group(), 'parrentId':tmp,'text':text.search(part).group()})
        return output
    else: return ''


def delCategoriesPrefix(text):
    """
     в фрагменте кода Categories удаляются все на упоминания  "БУ"
     на вход весь файл, на выход тот же файл но переделанный
    """
    categories=re.compile(r'<categories>.+?</categories>',re.S)
    part_edge=categories.search(text).span()
    tmp = re.sub(r'БУ','',text[part_edge[0]:part_edge[1]])
    tmp = re.sub(r'> ','>',tmp)
    tmp = re.sub(r' <','<',tmp)
    tmp=text[:part_edge[0]]+tmp+text[part_edge[1]:]
    return tmp


def state_name(text):
    """
     Если в параметре состояние стоит БУ, добавляет префикс к атрибуту  name
    """

    offer     =  re.compile(r'<offer.+?</offer>',re.S)
    BU_finder =  re.compile(r'<param name="Состояние".+?Б/У.+?</param>',re.S)
    offers     = re.compile(r'(?<=<offers>).+?(?=</offers>)',re.S)
    part_edge  = offers.search(text).span()

    offers_text=''

    for obj in offer.finditer(text,re.S):
        x=obj.group()
        if not BU_finder.search(x,re.S):offers_text+=x
        else:offers_text+=re.sub(r'<name>','<name>Б/У ',x)

    return text[:part_edge[0]] + offers_text + text[part_edge[1]:]


def vendorCodes(*data):
    vendorCode =  re.compile(r'(?<=<vendorCode>).+?(?=</vendorCode>)',re.S)
    output=[]
    for part in vendorCode.finditer(data[0]):
        output.append(part.group());
    return output


def offers(*data):
    """
     Создает словарь для каждого предложения , КАТЕГОРИЯ, СОСТОЯНИЕ , АРТИКУЛ , Вспомогательное включить/исключить
    """
    if data:

        offer     =  re.compile(r'<offer.+?</offer>',re.S)
        vendorCode=  re.compile(r'(?<=<vendorCode>).+?(?=</vendorCode>)',re.S)
        category  =  re.compile(r'(?<=<categoryId>).+?(?=</categoryId>)',re.S)
        state     =  re.compile(r'(?<=<param name="Состояние">).+?(?=</param>)',re.S)
        offer_parse_dic={
        #Описание элемента
            'vendorCode':vendorCode,
            'category':category,
            'state':state

        }
        output=[]

        for offer_in_xml in offer.finditer(data[0],re.S):
            tmp={}
            for key in offer_parse_dic:
                if offer_parse_dic[key]:

                    if offer_parse_dic[key].findall(offer_in_xml.group(),re.S):
                        tmp[key]=offer_parse_dic[key].findall(offer_in_xml.group(),re.S)[0]
            tmp['pos']='include'
            output.append(tmp)

        return output

def filter_yml(*data):
    """
    1 - сам yml
    2 - категории
    3 - включенные
    4  - исключенные
    """
    offers     =  re.compile(r'(?<=<offers>).+?(?=</offers>)',re.S)
    offer     =  re.compile(r'<offer.+?</offer>',re.S)
    vendorCode=  re.compile(r'(?<=<vendorCode>).+?(?=</vendorCode>)',re.S)
    category  =  re.compile(r'(?<=<categoryId>).+?(?=</categoryId>)',re.S)
    offers_text=''
    if len(data) !=4:
        print('неверное количество аргументов')
    else:
        text = data[0]
        categories=data[1]
        articles_in=data[2] # vedorcode
        articles_out=data[3]
    part_edge=offers.search(text).span()

    for obj in offer.finditer(text,re.S):
        x=obj.group()
        article=vendorCode.search(x).group()
        idpattern=category.search(x).group()
        if article  in articles_in:
            offers_text+=x
        elif article in articles_out:
            pass
        elif idpattern in categories:
            offers_text+=x
        else: pass
    return text[:part_edge[0]] + offers_text + text[part_edge[1]:]