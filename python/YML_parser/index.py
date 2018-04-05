from flask import Flask, request, render_template, send_file
from handler_YML import vendorCodes,categories,filter_yml,delCategoriesPrefix,state_name

app = Flask(__name__)

def_step=['enter','upload','filter']
def_name="delorian10"
def_pass="1111"
price = 'price.yml'
filename='price_update.yml'

@app.route('/')
def index():
    return render_template("enter.html",data = {'error':''})

@app.route('/', methods=['POST'])
def index_upload():
    step = int(request.form['step'])
    data = {}
    if step == 0:
        username =  request.form['username']
        password =  request.form['password']
        if username==def_name and password==def_pass:
            data["error"] = ''
            step = 1
        else:
            data["error"] = 'Ошибка, неверные пароль или логин'
    elif step == 1:
        file = request.files.get('fileYML')
        file.save(price)
        #Обработка файла
        temp_file=[]
        with open(price,encoding='utf-8') as file:
            try:
                temp_file=file.read()
            except Exception as ins:
                error = type(ins)
        if temp_file:
            data["categories"] = categories(temp_file)
            data["articles"] = vendorCodes(temp_file)
            step = 2
        else:
            step = 1
            data.error = error
    elif step == 2:
        cats =  request.form.getlist('categories[]')
        articles_in =  request.form.getlist('articles_in[]')
        articles_out =  request.form.getlist('articles_out[]')
        #Обработка данных по запросу из формы и вовзращение результирующего файла price_update.yml на загрузку
        temp_file=[]
        with open(price,encoding='utf-8') as file:
            try:
                temp_file=file.read()
            except Exception as ins:
                error = type(ins)
        res_file = filter_yml(temp_file,cats,articles_in,articles_out)
        res_file = delCategoriesPrefix(res_file)
        res_file = state_name(res_file)
        with open(filename,mode='w',encoding='utf-8') as file:
            file.write(res_file)
        return send_file(filename, as_attachment = True, attachment_filename = filename)
    else:
        step = 0
    data["step"] = step
    template = def_step[step]+".html"
    return render_template(template,data=data)

if __name__ == '__main__':
    app.run(debug=True)