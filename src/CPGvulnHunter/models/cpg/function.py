from dataclasses import dataclass
import hashlib
from typing import Optional

@dataclass
class Function:
    """
    表示一个代码函数的数据模型
    基于Joern CPG中Method节点的实际字段结构
    """
    # 必需字段
    name: str
    
    # Joern Method节点的核心字段
    ast_parent_full_name: Optional[str] = None
    ast_parent_type: Optional[str] = None
    code: Optional[str] = None
    column_number: Optional[int] = None
    column_number_end: Optional[int] = None
    filename: Optional[str] = None
    full_name: Optional[str] = None
    generic_signature: Optional[str] = None
    hash_value: Optional[str] = None
    is_external: bool = False
    line_number: Optional[int] = None
    line_number_end: Optional[int] = None
    offset: Optional[int] = None
    offset_end: Optional[int] = None
    order: Optional[int] = None
    signature: Optional[str] = None
    parameters: Optional[list['Parameter']] = None  # 函数参数列表
    useage : Optional[str] = None  # 函数调用点，用来丰富给大模型的信息
    full_signature: Optional[str] = None  # 完整的函数签名，包括返回值和参数类型



    def set_full_signature(self, signature: str):
        self.full_signature = signature
        return True

    def get_full_signature(self) -> str:
        """
        这里有点麻烦,因为语言之间的差别joern的表现不统一。
        对于c来说，内部函数有siganture，外部函数没有（这里和没有进行完整的预处理也有关系。）
        对于Java来说，内部函数和外部函数都有返回值
        我希望他们用一种相对统一的方式
        :return: 函数签名字符串
        """
        # # 如果没有signature，尝试根据参数生成
        # param_types = []
        # if self.parameters:
        #     for param in sorted(self.parameters, key=lambda p: p.index or 0):
        #         param_types.append(param.type_full_name or 'ANY')
        
        # param_str = ', '.join(param_types)
        # # 尝试从现有信息推断返回类型
        # return_type = 'ANY'
        # sigenature = f"{return_type} {self.full_name}({param_str})"
        return self.full_signature
    
    def set_parameters(self, parameters: list['Parameter']):
        self.parameters = parameters

    def set_useage(self, useage: str):
        """
        设置函数调用点信息
        :param useage: 函数调用点的Joern查询命令
        """
        self.useage = useage

    def to_dict(self):
        """转换为字典"""
        from dataclasses import asdict
        return asdict(self)
    
    def toJson(self, indent: Optional[int] = None) -> str:
        """
        将Function对象转换为JSON字符串
        :param indent: JSON缩进级别，None表示紧凑格式，数字表示缩进空格数
        :return: JSON字符串
        """
        import json
        # 获取字典表示
        data_dict = self.to_dict()
        
        # 处理可能的None值和特殊类型
        def serialize_value(value):
            if value is None:
                return None
            elif isinstance(value, list):
                return [serialize_value(item) for item in value]
            elif hasattr(value, 'to_dict'):
                return value.to_dict()
            else:
                return value
        
        # 递归处理所有值
        serialized_dict = {}
        for key, value in data_dict.items():
            serialized_dict[key] = serialize_value(value)
        
        # 转换为JSON字符串
        return json.dumps(serialized_dict, indent=indent, ensure_ascii=False)
    
    def get_location_info(self):
        """获取位置信息"""
        return {
            'filename': self.filename,
            'line_number': self.line_number,
            'column_number': self.column_number,
            'line_number_end': self.line_number_end,
            'column_number_end': self.column_number_end
        }
    
    def to_String(self):
        """返回函数的字符串表示"""
        return f"Function(name={self.name}, filename={self.filename}, line_number={self.line_number})"
    
    @classmethod
    def from_json(cls, json_data):
        """从JSON数据创建Function对象"""
        if isinstance(json_data, str):
            import json
            json_data = json.loads(json_data)
        
        # 如果json_data是列表，取第一个元素
        if isinstance(json_data, list) and len(json_data) > 0:
            json_data = json_data[0]
        
        # 创建Function对象，映射Joern返回的字段到Function属性
        kwargs = {}
        
        # 必需字段
        kwargs['name'] = json_data.get('name', '')
        
        # 直接映射的字段
        direct_mappings = {
            'code': 'code',
            'filename': 'filename', 
            'fullName': 'full_name',
            'genericSignature': 'generic_signature',
            'signature': 'signature',
            'order': 'order'
        }
        
        for json_field, func_field in direct_mappings.items():
            if json_field in json_data:
                kwargs[func_field] = json_data[json_field]
        
        # 需要特殊处理的字段
        if 'astParentFullName' in json_data:
            kwargs['ast_parent_full_name'] = json_data['astParentFullName']
        
        if 'astParentType' in json_data:
            kwargs['ast_parent_type'] = json_data['astParentType']
        
        if 'isExternal' in json_data:
            kwargs['is_external'] = json_data['isExternal']
        
        if 'hash' in json_data:
            kwargs['hash_value'] = json_data['hash']
        
        # 处理可能为Some(value)格式的字段
        optional_value_fields = {
            'columnNumber': 'column_number',
            'columnNumberEnd': 'column_number_end', 
            'lineNumber': 'line_number',
            'lineNumberEnd': 'line_number_end',
            'offset': 'offset',
            'offsetEnd': 'offset_end'
        }
        
        for json_field, func_field in optional_value_fields.items():
            if json_field in json_data:
                value = json_data[json_field]
                # 处理Some(value = x)格式
                if isinstance(value, dict) and 'value' in value:
                    kwargs[func_field] = value['value']
                elif value is not None:
                    kwargs[func_field] = value
        
        return cls(**kwargs)
    
    @classmethod
    def fromJson(cls, json_str: str) -> 'Function':
        """
        从JSON字符串创建Function对象（from_json的别名）
        
        Args:
            json_str: JSON格式的字符串
            
        Returns:
            Function: Function对象实例
        """
        return cls.from_json(json_str)
    
    def generateFunctionInfo(self) -> str:
        """
        生成函数信息,用于给大模型进行查询。
        :return: 函数信息字符串
        """
        function_info = f"Function Name: {self.name}\n"
        function_info += f"Full Name: {self.full_name}\n"
        function_info += f"Signature: {self.full_signature}\n"
        function_info += f"File: {self.filename or 'N/A'}\n"
        function_info += f"code: {self.code or 'N/A'}\n"
        function_info += f"useage: {self.useage or 'N/A'}\n"
        return function_info



    def get_function_key(self) -> str:
        """返回函数的唯一表示，可以用于缓存"""
        sig =self.get_full_signature()
        key_hash = hashlib.sha256(sig.encode('utf-8')).hexdigest()
        return key_hash

    def to_llm_info(self) -> str:
        """
        生成函数信息字符串，供LLM使用
        需要一个key指来指定函数的唯一性。
        需要有方法名签名等信息。对于c函数来说，fullname不包含参数和返回值信息。
        暂时决定key值由 fullname+sigenature组成。
        :return: 函数信息字符串
        """
        info = f"key: {self.get_function_key()}"
        info += f"full_name: {self.full_name or 'N/A'}\n"
        info += f"Signature: {self.get_full_signature() or 'N/A'}\n"
        info += f"Usage Query: {self.useage or 'N/A'}\n"
        return info

    def generateUseageQuery(self) -> str:
        """
        生成函数调用点的Joern查询命令
        :return: Joern查询命令字符串
        """
        if self.full_name:
            query = f'''cpg.method.fullNameExact("{self.full_name}").callIn.astParent.code.toJsonPretty'''
        else:
            query = f'''cpg.method.fullNameExact("{self.name}").callIn.astParent.code.toJsonPretty'''
        return query


    def generateParameterQuery(self) -> str:
        """
        生成函数参数的Joern查询命令
        :return: Joern查询命令字符串
        """
        if self.full_name:
            query = f'cpg.method.fullNameExact("{self.full_name}").parameter.toJsonPretty'
        else:
            query = f'cpg.method.name("{self.name}").parameter.toJsonPretty'
        return query


    def generateSignatureQuery(self) -> str:
        """
        生成函数签名的Joern查询命令
        :return: Joern查询命令字符串
        """
        commands = f"""cpg.method.fullNameExact("{self.full_name}").map {{ m => 
        s"${{m.methodReturn.typeFullName}} ${{m.name}}(${{m.parameter.map(_.typeFullName).mkString(", ")}})" 
        }}.toJsonPretty"""

        return commands
    
    def generateReturnTypeQuery(self) -> str:
        """
        
        """
        return ''

    def getSignature(self) -> str:
        """
        根据当前函数对象生成函数签名字符串（本地生成，不依赖Joern查询）
        :return: 函数签名字符串
        """
        # 如果已经有signature字段，直接返回
        if self.signature:
            return self.signature
        
        # 否则根据参数信息构造签名
        param_types = []
        if self.parameters:
            for param in sorted(self.parameters, key=lambda p: p.index or 0):
                param_types.append(param.type_full_name or 'ANY')
        
        param_str = ', '.join(param_types)
        
        # 尝试从现有信息推断返回类型
        return_type = 'void'  # 默认返回类型
        
        signature = f"{return_type} {self.name}({param_str})"
        return signature





    def findParameterOut(self,index) -> str:
        """
        在Joern中定位函数的参数节点
        :param function: 函数对象
        :return: 查询命令字符串
        """
        query = f'cpg.call("{self.full_name}").argument({index}).ast.l'
        return query

    def findParameterIn(self,index) -> str:
        """
        在Joern中定位函数的参数节点
        :param function: 函数对象
        :return: 查询命令字符串
        """
        query = f'cpg.methodParameterIn.where(_.method.fullNameExact("{self.full_name}")).index({index}).l'
        return query

    def findArgumentIn(self,index) -> str:
        """
        在Joern中定位函数的参数节点
        :param function: 函数对象
        :return: 查询命令字符串
        """
        query = f'cpg.call("{self.full_name}").argument({index}).l'
        return query
    

    def findReturnValue(self) -> str:
        """
        定位函数的返回值节点
        :param function: 函数对象
        :return: 查询命令字符串
        """
        query = f'cpg.method.fullName("{self.full_name}").methodReturn'
        return query
    
    def findReturnType(self) -> str:
        """
        获取函数返回类型的查询命令
        :return: 查询命令字符串
        """
        query = f'cpg.method.fullName("{self.full_name}").methodReturn.typeFullName'
        return query
    
    def findAllParameters(self) -> str:
        """
        获取函数的所有参数节点
        :return: 查询命令字符串
        """
        query = f'cpg.method.fullName("{self.full_name}").parameter'
        return query
    
    def add_parameter(self, parameter: 'Parameter'):
        """添加参数到函数"""
        if self.parameters is None:
            self.parameters = []
        self.parameters.append(parameter)
    
    def get_parameter_by_index(self, index: int) -> Optional['Parameter']:
        """根据索引获取参数"""
        if self.parameters:
            for param in self.parameters:
                if param.index == index:
                    return param
        return None
    
    def get_parameter_count(self) -> int:
        """获取参数数量"""
        return len(self.parameters) if self.parameters else 0



@dataclass
class Parameter:
    """
    表示函数参数的数据模型
    基于Joern CPG中MethodParameterIn节点的实际字段结构
    """
    # 必需字段
    name: str
    
    # Joern MethodParameterIn节点的核心字段
    closure_binding_id: Optional[str] = None
    code: Optional[str] = None
    column_number: Optional[int] = None
    dynamic_type_hint_full_name: Optional[list] = None
    evaluation_strategy: Optional[str] = None
    index: Optional[int] = None
    is_variadic: bool = False
    line_number: Optional[int] = None
    offset: Optional[int] = None
    offset_end: Optional[int] = None
    order: Optional[int] = None
    possible_types: Optional[list] = None
    type_full_name: Optional[str] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.type_full_name is None:
            self.type_full_name = 'ANY'
        if self.dynamic_type_hint_full_name is None:
            self.dynamic_type_hint_full_name = []
        if self.possible_types is None:
            self.possible_types = []
        if self.evaluation_strategy is None:
            self.evaluation_strategy = 'BY_VALUE'
    
    def to_dict(self):
        """转换为字典"""
        from dataclasses import asdict
        return asdict(self)
    
    def toJson(self, indent: Optional[int] = None) -> str:
        """
        将Parameter对象转换为JSON字符串
        :param indent: JSON缩进级别，None表示紧凑格式，数字表示缩进空格数
        :return: JSON字符串
        """
        import json
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_data):
        """从JSON数据创建Parameter对象"""
        if isinstance(json_data, str):
            import json
            json_data = json.loads(json_data)
        
        # 创建Parameter对象，映射Joern返回的字段到Parameter属性
        kwargs = {}
        
        # 必需字段
        kwargs['name'] = json_data.get('name', '')
        
        # 直接映射的字段
        direct_mappings = {
            'code': 'code',
            'index': 'index',
            'order': 'order',
            'name': 'name',
            'isVariadic': 'is_variadic',
            'evaluationStrategy': 'evaluation_strategy',
            'typeFullName': 'type_full_name'
        }
        
        for json_field, param_field in direct_mappings.items():
            if json_field in json_data:
                kwargs[param_field] = json_data[json_field]
        
        # 需要特殊处理的字段
        if 'closureBindingId' in json_data:
            kwargs['closure_binding_id'] = json_data['closureBindingId']
        
        if 'dynamicTypeHintFullName' in json_data:
            kwargs['dynamic_type_hint_full_name'] = list(json_data['dynamicTypeHintFullName'])
        
        if 'possibleTypes' in json_data:
            kwargs['possible_types'] = list(json_data['possibleTypes'])
        
        # 处理可能为Some(value)格式的字段
        optional_value_fields = {
            'columnNumber': 'column_number',
            'lineNumber': 'line_number',
            'offset': 'offset',
            'offsetEnd': 'offset_end'
        }
        
        for json_field, param_field in optional_value_fields.items():
            if json_field in json_data:
                value = json_data[json_field]
                # 处理Some(value = x)格式或None
                if isinstance(value, dict) and 'value' in value:
                    kwargs[param_field] = value['value']
                elif value is not None:
                    kwargs[param_field] = value
        
        return cls(**kwargs)
    
    def get_location_info(self):
        """获取位置信息"""
        return {
            'line_number': self.line_number,
            'column_number': self.column_number,
            'offset': self.offset,
            'offset_end': self.offset_end
        }
    
    def __str__(self):
        """返回参数的字符串表示"""
        return f"Parameter(name={self.name}, index={self.index}, type={self.type_full_name})"



