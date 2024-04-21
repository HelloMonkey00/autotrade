import os
import configparser

class ConfigManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self, config_file='config.ini'):
        if not hasattr(self, 'config'):
            # 获取 config.py 文件的绝对路径
            config_py_path = os.path.dirname(os.path.abspath(__file__))
            # 获取上一级目录的路径
            parent_dir = os.path.dirname(config_py_path)
            # 构造 config.ini 文件的绝对路径
            config_ini_path = os.path.join(parent_dir, config_file)
            self.config_file = config_ini_path
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file, encoding="UTF-8")

    def get(self, key, default=None, namespace='DEFAULT'):
        # 先从环境变量中获取
        value = os.environ.get(namespace+'.'+key)
        if value is not None:
            return value

        # 然后从配置文件中获取
        if self.config.has_option(namespace, key):
            return self.config[namespace][key]

        # 如果都没有找到，那么返回默认值
        return default

    def get_bool(self, key, default=False, namespace='DEFAULT'):
        value = self.get(key, None, namespace)
        if value is None:
            return default
        return value.lower() in ['true', 'yes', '1']
    
    def get_int(self, key, default=0, namespace='DEFAULT'):
        value = self.get(key, None, namespace)
        if value is None:
            return default
        return int(value)
    
    def is_simulate(self):
        return self.get_bool('simulate', True)

if __name__ == "__main__":
    config_manager = ConfigManager()
    value = config_manager.get('simulate', None)
    print(value)
    print(type(value))
    print(config_manager.get_bool('simulate', False))
    value = config_manager.get('pwd_unlock', None, 'MOOMOO')
    print(value)
    print(type(value))
    print(config_manager.is_simulate())