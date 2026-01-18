import re
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from Framework import *

"""
Zebraith SHELL.

Plugin Manager.
"""

@dataclass
class PluginInfo:
    """存储插件的基本信息"""
    Name: str
    Version: str
    Author: str
    Description: str

@dataclass
class PluginContext:
    """存储解析后的插件数据"""
    Info: Optional[PluginInfo] = None
    Code: Optional[str] = None
    RawContent: str = ""

class PluginParser:
    """解析 ZebraithSHELL 插件文件格式"""
    def __init__(self):
        # 正则匹配 BEGIN <BLOCK> ... END
        # re.DOTALL 让 . 匹配换行符
        self.block_pattern = re.compile(r"BEGIN\s+(\w+)\s+(.*?)\s+END", re.DOTALL)

    def parse(self, content: str) -> PluginContext:
        context = PluginContext(RawContent=content)
        matches = self.block_pattern.findall(content)
        
        for block_name, block_content in matches:
            block_content = block_content.strip()
            
            if block_name == "INFORMATION":
                context.Info = self._parse_info(block_content)
            elif block_name == "CODE":
                context.Code = block_content
                
        return context

    def _parse_info(self, content: str) -> PluginInfo:
        """解析 INFORMATION 块，提取元数据"""
        info_dict = {}
        # 匹配 self.Key = Value
        pattern = re.compile(r'self\.(\w+)\s*=\s*(.+)')
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = pattern.match(line)
            if match:
                key = match.group(1)
                val_str = match.group(2).strip()
                # 去除引号
                if (val_str.startswith('"') and val_str.endswith('"')) or \
                   (val_str.startswith("'") and val_str.endswith("'")):
                    val_str = val_str[1:-1]
                info_dict[key] = val_str

        return PluginInfo(
            Name=info_dict.get("Name", "Unknown"),
            Version=info_dict.get("Version", "0.0.0"),
            Author=info_dict.get("Author", "Unknown"),
            Description=info_dict.get("Description", "")
        )

class PluginManager:
    """
    插件管理器
    负责加载插件文件，解析并执行其中的代码，
    使插件中的 @register_command 能够注册到全局 Commands 表中。
    """
    def __init__(self):
        self.parser = PluginParser()
        self.loaded_plugins: Dict[str, PluginInfo] = {}
        self.failed_plugins_file_list: List[str] = []

    def LoadPluginFromFile(self, file_path: str, skipload):
        """从文件路径加载插件"""
        if not os.path.exists(file_path):
            error(None, f"    :: Plugin file not found: {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            returnv = self.LoadPluginFromString(content, skipload)
            if returnv == -1:
                self.failed_plugins_file_list.append(file_path)
        except Exception as e:
            error(e, f"    :: Failed to load plugin from file: {file_path}")
            self.failed_plugins_file_list.append(file_path)

    def LoadAllPlugins(self, skipload = False):
        """加载所有插件"""
        for file_name in os.listdir("plugins"):
            if file_name.endswith(".zshellext"):
                self.LoadPluginFromFile(os.path.join("plugins", file_name), skipload)

    def LoadPluginFromString(self, content: str, skipload):
        """从字符串内容加载插件"""
        context = self.parser.parse(content)
        
        if not context.Info and skipload:
            if not skipload: slowprint("         :: Plugin missing information block. Skipping.")
            return -1
        elif not context.Info: return -1
        
        name = context.Info.Name
        if name in self.loaded_plugins and skipload:
            if not skipload: slowprint(f"        :: Plugin '{name}' is already loaded. Skipping.")
            return -1
        elif name in self.loaded_plugins: return -1

        if not skipload: slowprint(f"        :: Loading plugin {name} v{context.Info.Version} by {context.Info.Author}")
        
        if context.Code:
            self._ExecutePluginCode(context.Code, skipload)
            self.loaded_plugins[name] = context.Info
            if not skipload: slowprint(f"            \\ Plugin {name} loaded successfully.")
        else:
            if not skipload: slowprint("             \\ Plugin missing code block. Skipping.")
            return -1
        return 0

    def _ExecutePluginCode(self, code_str: str, skipload = False):
        """
        执行插件代码
        核心逻辑：将全局的 register_command 注入到 exec 的环境中
        """
        import __main__
        
        exec_globals = {
            "__name__": "zebraith_plugin",
            "__builtins__": __builtins__,
            "register_command": register_command,
        }

        if "# ADVANCED TAG #" in code_str:
            if not skipload: slowprint("            \\ Advanced plugin mode detected. For security, Please check plugin code using AI or you.")
            exec_globals ["pm"] = self # 对于 BasePlugin.zshellext 特殊放权。
            exec_globals ["rich"] = rich

        try:
            exec(code_str, exec_globals)
        except Exception as e:
            if not skipload: error(e, "         \\ Failed to execute plugin code.")
            import traceback
            traceback.print_exc()
    
    def UnloadAllPlugin(self):
        """卸载所有插件"""
        self.loaded_plugins.clear()
        self.failed_plugins_file_list.clear()
        print(":: All Plugins Unloaded.")