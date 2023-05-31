import requests
import json
import os
import subprocess
from datetime import datetime

class YapiRequestBody:  
    def __init__(self, required, name, type, desc):
        self.required = required
        self.name = name
        self.type = type
        self.desc = desc
    
    #将JSON类型转换为swift的类型
    def get_type_string(self):
            
        if self.type == 'integer' or self.type == 'number':
            return 'Int' if self.required == '1' else 'Int? = nil'
        elif self.type == 'string' or self.type == 'text':
            return 'String' if self.required == '1' else 'String? = nil'
        elif self.type == 'boolean':
            return 'Bool' if self.required == '1' else 'Bool? = nil'
        elif self.type == 'array':  
            return '[String]' if self.required == '1' else '[String]? = nil'
        elif self.type == 'object':
            return '[String: Any]'
        else:
            return 'Any'
    
    #获取swift的参数字符串(id: String, locate: Int)
    def get_swift_params(self):
        return self.name + ': ' + self.get_type_string()

class YapiModel:
    def __init__(self, title, path, method, desc, req_body_form, case_name):
        self.title = title
        self.path = path
        self.method = method
        self.desc = desc
        self.req_body_form = req_body_form
        self.case_name = case_name
        
    #获取case 后面的参数字符串    
    def get_case_params_string(self):
        params_arr = []
        for param in self.req_body_form:
            params_arr.append(param.get_swift_params())
        return '(' + ', '.join(params_arr) + ')' if params_arr else ''
    #获取parameters 后面的参数字符串
    def get_parameters_string(self):
        params_arr = []
        for param in self.req_body_form:
            params_arr.append(keyworks_transform(param.name))
        return '(' + ', '.join(params_arr) + ')' if params_arr else ''
         
#关键词和操作符转换
def keyworks_transform(param_name):
    keyworksAndOperators = ["class", "deinit", "enum", "extension", "func", "import", "init", "internal", "let", "operator", "private", "protocol", "public", "static", "struct", "subscript", "typealias", "var", "break", "case", "continue", "default", "do", "else", "fallthrough", "for", "if", "in", "repeat", "return", "switch", "where", "while"]
    if param_name in keyworksAndOperators:
        param_name = param_name + "Param"
    return param_name
        
#格式化接口名
def format_api_title(input_string):
    if input_string.startswith('/'):
        input_string = input_string[1:]
    parts = input_string.split('/')
    output_string = parts[0] + ''.join([s[:1].upper() + s[1:] for s in parts[1:]])

    return output_string

#请求json并解析
def request():
    # 读取 JSON 文件
    with open('conf.json') as file:
        data = json.load(file)

    url = data.get('url')
    global file_name
    file_name = data.get('file_name')
    global public_key_word
    is_method_public = data.get('is_method_public')
    public_key_word = 'public ' if is_method_public else ''
    fold_names = data.get('fold_names')
    response = requests.get(url)
    data = json.loads(response.text)
    # api列表
    
    filtered_data = []
    for obj in data:
        if obj['name'] in fold_names:
            filtered_data += obj['list']

    return filtered_data
    
#解析api到模型
def parse_model(apis):
    models = []
    for api in apis:
        title = api['title']
        path = api['path']
        req_body_form = api.get('req_body_form')
        method = api['method'].lower()
        apiDesc = api['desc']
        case_name = format_api_title(path)
        req_body_other = api.get('req_body_other')
        paramModels = []
        
        if req_body_form:
            #直接取模型
            for param in req_body_form:
                reqBody = YapiRequestBody(param['required'], param['name'], param['type'], param['desc'])    
                paramModels.append(reqBody)
        elif req_body_other:
            if type(req_body_other) != '':
                data = json.loads(req_body_other)
                #type有array和object，可能还有其他？
                properties = None
                if data.get('type') == 'array':
                    requireds = data.get('items').get('required')
                    properties = data.get('items').get('properties')
                elif data.get('type') == 'object':
                    requireds = data.get('required',[])
                    properties = data['properties']
                    #TODO:这里有个递归，需要处理
                if properties:
                    for key in properties:  
                        value = properties[key]
                        isReq = '1' if key in requireds else '0'
                        reqBody = YapiRequestBody(isReq, key, value['type'], value.get('description'))    
                        paramModels.append(reqBody)
            
        model = YapiModel(title,path,method,apiDesc,paramModels,case_name)
        models.append(model)
    return models

#创建swift文件
def create_swift_file(models, class_name):
    
    now = datetime.now().strftime("%Y/%m/%d")
    year = datetime.now().strftime("%Y")
    fName = class_name + '.swift'
    with open(fName, "w") as file:
        file.write("//\n")
        file.write("//  %s.swift\n" % (class_name))
        file.write("//  yupao\n")
        file.write("//\n")
        file.write("//  Created by AutoScript on %s.\n" % (now))
        file.write("//  Copyright © %s AutoScript. All rights reserved.\n" % (year))
        file.write("//\n\n")
        file.write("import YPNetKit\n\n")
        file.write("%senum %s {\n" % (public_key_word,class_name))
        for model in models:
            file.write("\t/// %s\n" % (model.title))
            file.write("\tcase %s%s\n" % (model.case_name,model.get_case_params_string()))
        file.write("}\n\n")
        file.write('extension %s: YPBaseTargetType {\n' % (class_name))
        file.write('\t%svar parameters: [String: Any]? {\n' % (public_key_word))
        file.write('\t\tvar params: [String: Any] = [:]\n')
        file.write('\t\tswitch self {\n')
        for model in models:
            if model.get_parameters_string() != '':
                file.write('\t\tcase let .%s%s:\n' % (model.case_name,model.get_parameters_string()))
                for param in model.req_body_form:
                    file.write('\t\t\tparams["%s"] = %s\n' % (param.name,param.name))
                    
        if 0 in list(map(lambda x: len(x.req_body_form),models)):
            file.write('\t\tdefault: break\n')
        file.write('\t\t}\n')
        file.write('\t\treturn params\n')
        file.write('\t}\n')
        file.write('\n')
        file.write("\tvar path: String {\n")
        file.write("\t\tswitch self {\n")
        for model in models:
            file.write("\t\tcase .%s:\n" % (model.case_name))
            file.write("\t\t\treturn \"%s\"\n" % (model.path))
        file.write("\t\t}\n")
        file.write("\t}\n")
        file.write("\n")
        file.write("\tvar method: Method {\n")
        file.write("\t\tswitch self {\n")
        for model in models:
            file.write("\t\tcase .%s:\n" % (model.case_name))
            file.write("\t\t\treturn .%s\n" % (model.method))
        file.write("\t\t}\n")
        file.write("\t}\n")
        file.write("\n")
        file.write("\tvar serviceType: ServiceType {\n")
        file.write("\t\treturn .JAVA\n")
        file.write("\t}\n")
        file.write("\n")
        file.write("\tvar showLog: Bool {\n")
        file.write("\t\treturn true\n")
        file.write("\t}\n")
        file.write("\n")
        file.write("\n")
        file.write("}\n")

def open_curren_file():

    current_dir = os.getcwd()

    # 构建文件路径
    file_path = os.path.join(current_dir, file_name + '.swift')

    # 使用subprocess模块打开文件
    subprocess.call(["open", file_path])
    
def main():
    apis = request()    
    models = parse_model(apis)
    create_swift_file(models,file_name)
    open_curren_file()

if __name__ == '__main__':
    main()
