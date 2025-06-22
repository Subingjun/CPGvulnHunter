from dataclasses import dataclass
import logging
from typing import List, Optional, Dict, Any
from enum import Enum
import json





# DataFlowResult表示查询的结果，对应单独的source和sink查询的结果
# DataFlowResult包含多个FlowPath，每个FlowPath表示一条数据流路径
# FlowPath包含多个FlowNode，每个FlowNode表示数据流路径中的一个节点

class NodeType(Enum):
    """节点类型枚举"""
    METHOD_PARAMETER_IN = "METHOD_PARAMETER_IN"      # 方法输入参数节点 - 表示函数/方法的输入参数
    METHOD_PARAMETER_OUT = "METHOD_PARAMETER_OUT"    # 方法输出参数节点 - 表示函数/方法的输出参数（引用传递）
    METHOD_RETURN = "METHOD_RETURN"                  # 方法返回值节点 - 表示函数/方法的返回值
    CALL = "CALL"                                    # 函数调用节点 - 表示对函数或方法的调用
    IDENTIFIER = "IDENTIFIER"                        # 标识符节点 - 表示变量名、函数名等标识符
    LITERAL = "LITERAL"                              # 字面量节点 - 表示常量值（如字符串、数字等）
    LOCAL = "LOCAL"                                  # 局部变量节点 - 表示局部变量的声明或定义
    BLOCK = "BLOCK"                                  # 代码块节点 - 表示代码块（如if块、循环体等）
    CONTROL_STRUCTURE = "CONTROL_STRUCTURE"          # 控制结构节点 - 表示控制流语句（如if、for、while等）
    UNKNOWN = "UNKNOWN"                              # 未知类型节点 - 无法识别或不在上述类型中的节点

@dataclass
class FlowNode:
    """数据流节点，表示数据流路径中的一个节点"""
    
    # 基本信息
    node_id: int                          # 节点ID (_id)
    label: str                           # 节点标签 (_label)
    code: str                            # 节点代码
    
    # 位置信息
    line_number: Optional[int] = None     # 行号
    column_number: Optional[int] = None   # 列号
    
    # 类型信息
    type_full_name: Optional[str] = None  # 完整类型名
    possible_types: List[str] = None      # 可能的类型列表
    dynamic_type_hint_full_name: List[str] = None
    
    # 节点特定属性
    name: Optional[str] = None            # 节点名称
    order: Optional[int] = None           # 顺序
    
    # 参数相关（如果是参数节点）
    index: Optional[int] = None           # 参数索引
    evaluation_strategy: Optional[str] = None  # 求值策略
    is_variadic: Optional[bool] = None    # 是否可变参数
    argument_index: Optional[int] = None  # 参数索引
    
    # 方法相关（如果是方法调用）
    signature: Optional[str] = None       # 方法签名
    method_full_name: Optional[str] = None # 方法全名
    dispatch_type: Optional[str] = None   # 调度类型
    
    # 流路径相关
    call_site_stack: List[Any] = None     # 调用站点栈
    visible: bool = True                  # 是否可见
    is_output_arg: bool = False           # 是否为输出参数
    out_edge_label: str = ""              # 输出边标签
    

    #所属方法的名称
    method_name : str = None
    #所属方法的代码
    method_code = None  
    # 其他属性
    properties: Dict[str, Any] = None     # 其他属性

    methodContext: Optional[str] = None  # 父代码块（如果有）

    classContext: Optional[str] = None  # 方法代码（如果是方法节点）
    
    def get_node_info(self) -> str:
        """
        获取节点信息字符串
        :return: 节点信息字符串
        """
        node_info = f"Node ID: {self.node_id}, Label: {self.label}, Code: {self.code}"
        if self.line_number is not None:
            node_info += f", Location: {self.line_number}:{self.column_number}"
        if self.type_full_name:
            node_info += f", Type: {self.type_full_name}"
        if self.name:
            node_info += f", Name: {self.name}"
        return node_info


    def set_method_code(self, method_code: str):
        """
        设置方法代码
        :param method_code: 方法代码字符串
        """
        self.method_code = method_code

    def set_method_name(self, method_name: str):
        """
        设置方法名称
        :param method_name: 方法名称字符串
        """
        self.method_name = method_name

    def __post_init__(self):
        if self.possible_types is None:
            self.possible_types = []
        if self.dynamic_type_hint_full_name is None:
            self.dynamic_type_hint_full_name = []
        if self.call_site_stack is None:
            self.call_site_stack = []
        if self.properties is None:
            self.properties = {}
    
    @classmethod
    def from_path_node(cls, path_node_data: Dict[str, Any]) -> 'FlowNode':
        """从Joern路径节点数据创建FlowNode实例"""
        node_data = path_node_data.get('node', {})
        
        return cls(
            # 基本信息
            node_id=node_data.get('_id', 0),
            label=node_data.get('_label', ''),
            code=node_data.get('code', ''),
            
            # 位置信息
            line_number=node_data.get('lineNumber'),
            column_number=node_data.get('columnNumber'),
            
            # 类型信息
            type_full_name=node_data.get('typeFullName'),
            possible_types=node_data.get('possibleTypes', []),
            dynamic_type_hint_full_name=node_data.get('dynamicTypeHintFullName', []),
            
            # 节点特定属性
            name=node_data.get('name'),
            order=node_data.get('order'),
            
            # 参数相关
            index=node_data.get('index'),
            evaluation_strategy=node_data.get('evaluationStrategy'),
            is_variadic=node_data.get('isVariadic'),
            argument_index=node_data.get('argumentIndex'),
            
            # 方法相关
            signature=node_data.get('signature'),
            method_full_name=node_data.get('methodFullName'),
            dispatch_type=node_data.get('dispatchType'),
            
            # 流路径相关
            call_site_stack=path_node_data.get('callSiteStack', []),
            visible=path_node_data.get('visible', True),
            is_output_arg=path_node_data.get('isOutputArg', False),
            out_edge_label=path_node_data.get('outEdgeLabel', ''),
            
            # 其他属性
            properties={k: v for k, v in node_data.items() 
                       if k not in ['_id', '_label', 'code', 'lineNumber', 'columnNumber',
                                   'typeFullName', 'possibleTypes', 'dynamicTypeHintFullName',
                                   'name', 'order', 'index', 'evaluationStrategy', 'isVariadic',
                                   'argumentIndex', 'signature', 'methodFullName', 'dispatchType']}
        )
    
    @property
    def node_type(self) -> NodeType:
        """获取节点类型"""
        try:
            return NodeType(self.label)
        except ValueError:
            return NodeType.UNKNOWN
    
    def is_source(self) -> bool:
        """判断是否为数据源节点"""
        return self.node_type in [NodeType.METHOD_PARAMETER_IN, NodeType.CALL, NodeType.METHOD_RETURN]
    
    def is_sink(self) -> bool:
        """判断是否为数据汇聚节点"""
        return self.node_type in [NodeType.CALL, NodeType.METHOD_PARAMETER_IN]
    
    def get_display_name(self) -> str:
        """获取显示名称"""
        if self.name:
            return self.name
        elif self.method_full_name:
            return self.method_full_name
        else:
            return self.code[:20] + "..." if len(self.code) > 20 else self.code
    
    def get_location_str(self) -> str:
        """获取位置字符串"""
        if self.line_number:
            location = f":{self.line_number}"
            if self.column_number:
                location += f":{self.column_number}"
            return location
        return ""
    
    def __str__(self) -> str:
        display_name = self.get_display_name()
        location = self.get_location_str()
        edge_info = f" -> {self.out_edge_label}" if self.out_edge_label else ""
        
        return f"{display_name}({self.label}){location}{edge_info}"
    
    def to_dict(self) -> Dict[str, Any]:
        """将FlowNode转换为字典格式"""
        from dataclasses import asdict
        return asdict(self)
    
    def toJson(self, indent: Optional[int] = None) -> str:
        """
        将FlowNode对象转换为JSON字符串
        
        Args:
            indent: JSON缩进级别，None表示紧凑格式
            
        Returns:
            str: JSON格式的字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent, default=str)
    
    @classmethod
    def fromJson(cls, json_str: str) -> 'FlowNode':
        """
        从JSON字符串创建FlowNode对象
        
        Args:
            json_str: JSON格式的字符串
            
        Returns:
            FlowNode: FlowNode对象实例
        """
        data = json.loads(json_str)
        return cls(**data)

class FlowPath:
    """数据流路径，表示从源到汇的完整数据流"""
    def __init__(self, nodes: List[FlowNode], source=None, sink=None):
        self.nodes = nodes
        self.source = source                  # 数据源
        self.sink = sink                      # 数据汇聚点
        
        if not self.nodes:
            logging.warning("FlowPath initialized with no nodes.")


    def _get_function_chain(self) -> str:
        """获取路径中所有节点的函数调用链"""
        function_chain = []
        seen = set()
        for node in self.nodes:
            if node.method_name:
                if node.method_code not in seen:
                    function_chain.append(node.method_code)
                    seen.add(node.method_code)
            else:
                logging.warning(f"Node {node.get_display_name()} does not have a method full name.")
        return " -> ".join(function_chain)

    def to_dict(self) -> Dict[str, Any]:
        """将FlowPath转换为字典格式"""
        return {
            "nodes": [node.to_dict() for node in self.nodes],
        }

    @classmethod
    def from_joern_path(cls, path_data: Dict[str, Any],source,sink) -> 'FlowPath':
        """从Joern路径数据创建FlowPath实例"""
        path_nodes = path_data.get('path', [])
        nodes = [FlowNode.from_path_node(node_data) for node_data in path_nodes]
        
        return cls(nodes=nodes,source=source,sink=sink)
    
    def get_path_summary(self) -> str:
        """获取路径摘要"""
        try:
            summary = self._get_function_chain()
            logging.debug(f"Path summary: {summary}")
            return summary
        except Exception as e:
            logging.error(f"获取方法代码链失败: {e}")
            return "Error in path summary"
    

class DataFlowResult:
    """数据流分析结果"""
    flows: List[FlowPath]                 # 所有发现的数据流路径
    source: Any = None                    # 数据源
    sink: Any = None                      # 数据汇聚点
    
    def  __init__(self, flows: List[FlowPath], source=None, sink=None):
        self.flows = flows
        self.source = source
        self.sink = sink
    
    @classmethod
    def from_joern_result(cls, json: dict,source,sink) -> 'DataFlowResult':
        """从Joern的JSON结果创建DataFlowResult实例"""
        flows = []            
        if isinstance(json, list):
            for flow_data in json:
                if isinstance(flow_data, dict) and 'path' in flow_data:
                    flow = FlowPath.from_joern_path(flow_data,source,sink)
                    flows.append(flow)
                    logging.debug(f"添加数据流路径: {flow.get_path_summary()}")
        
        return cls(flows=flows,source=source,sink=sink)
    
            
    def to_dict(self) -> Dict[str, Any]:
        """将数据流结果转换为字典格式"""
        
        return {
            "flows": [flow.to_dict() for flow in self.flows],
            "source": self.source.to_dict(),
            "sink": self.sink.to_dict()
        }
    

