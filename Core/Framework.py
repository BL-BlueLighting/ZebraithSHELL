import re
import shlex
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from Core.Define import *

"""
Zebraith SHELL.

Developing main framework.
"""

#region DataStructure
# ==========================================
# 数据结构
# ==========================================

@dataclass
class CParams:
    """存储位置参数"""
    items: List[str] = field(default_factory=list)

@dataclass
class CArgs:
    """存储键值对参数"""
    items: Dict[str, str] = field(default_factory=dict)

@dataclass
class Command:
    """解析后的命令对象"""
    Head: str
    Params: CParams
    Args: CArgs

    def Eval(self, commands_registry: Dict[str, Dict[str, Any]]) -> Any:
        """
        执行命令
        :param commands_registry: 全局命令注册表
        :return: 回调函数的返回值
        """
        if self.Head not in commands_registry:
            rich.print("[bold cyan][ TIP ][/bold cyan] Command not found.")
            return

        cmd_info = commands_registry[self.Head]
        callback = cmd_info.get("callback")
        if not callback:
            error(Any, f"Command {self.Head} has no callback.")
            raise BreakException

        # 创建 API 对象传给回调函数
        api = CommandAPI(self, cmd_info)
        return callback(api)

@dataclass
class CommandAPI:
    """提供给回调函数的 API 对象"""
    command: Command
    cmd_info: Dict[str, Any]

    def GetArg(self, name: str, default: Any = None) -> Any:
        """
        获取参数
        逻辑：
        1. 首先尝试从 Params (位置参数) 中获取，根据 cmd_info['params'] 的定义顺序映射
        2. 如果在 Params 中找不到，尝试从 Args (命名参数) 中获取
        3. 如果都找不到，返回 default
        """
        # 1. 尝试从位置参数获取
        param_defs = self.cmd_info.get("params", [])
        if name in param_defs:
            # 找到该参数在定义列表中的索引
            try:
                idx = param_defs.index(name)
                if idx < len(self.command.Params.items):
                    return self.command.Params.items[idx]
            except ValueError:
                pass
        
        # 2. 尝试从命名参数获取
        if name in self.command.Args.items:
            return self.command.Args.items[name]

        # 3. 返回默认值
        return default
    
#endregion

#region Parser Core

# ==========================================
# 解析器
# ==========================================

class CommandParser:
    def __init__(self):
        pass

    def parse(self, input_str: str) -> Command:
        """
        解析字符串为 Command 对象
        """
        # 使用 shlex 进行标准的 shell 风格分割 (处理引号和转义)
        try:
            tokens = shlex.split(input_str)
        except ValueError as e:
            error(e, "Invalid command format. Do you forgot close the string?")
            raise BreakException()

        if not tokens:
            error(Any, "Empty command.")

        head = tokens[0]
        params = CParams()
        args = CArgs()

        # 遍历剩余的 token
        i = 1
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("--"):
                # 处理键值对 --key value
                key = token[2:]
                if i + 1 < len(tokens) and not tokens[i+1].startswith("-"):
                    value = tokens[i+1]
                    i += 2
                else:
                    value = "True" # 如果是 flag 类型 (如 --verbose)，默认设为 True
                    i += 1
                args.items[key] = value
            elif token.startswith("-"):
                # 处理短参数 -k value (简单处理，暂不支持 -abc 组合)
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i+1].startswith("-"):
                    value = tokens[i+1]
                    i += 2
                else:
                    value = "True"
                    i += 1
                args.items[key] = value
            else:
                # 处理位置参数
                params.items.append(token)
                i += 1

        return Command(Head=head, Params=params, Args=args)
#endregion

#region Decorator and Register

# ==========================================
# 装饰器与注册表
# ==========================================

# 全局命令注册表
Commands: Dict[str, Dict[str, Any]] = {}

# 注册命令的装饰器
def register_command(name: str, params: List[str], Commands: Dict[str, Dict[str, Any]] = Commands):
    def decorator(func: Callable):
        Commands[name] = {
            "params": params,
            "callback": func
        }
        return func
    return decorator

#endregion