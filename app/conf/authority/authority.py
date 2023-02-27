import yaml
import os

class Authority:
    _authorities = {}

    @classmethod
    def _load_config(cls, config_path):
        def flatten_list(nested_list):
            """
            将嵌套列表展开成一个列表
            """
            result = []
            for item in nested_list:
                if isinstance(item, list):
                    result.extend(flatten_list(item))
                else:
                    result.append(item)
            return result
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._authorities = config.get('authorities', {})
            for group_id, group_permissions in cls._authorities.items():
                for qq_id, qq_permissions in group_permissions.items():
                    permissions = []
                    for perm_list in qq_permissions['permission']:
                        permissions.extend(flatten_list(perm_list))
                    qq_permissions['permission'] = permissions

    @classmethod
    def get_permission(cls, group_id, qq_id):
        if not cls._authorities:
            cls._load_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'authority.yaml'))
        if group_id not in list(cls._authorities.keys()):
            return None
        try:
            return cls._authorities[group_id][qq_id]['permission']
        except KeyError:
            return cls._authorities[0][0]['permission']

    @classmethod
    def check_command_permission(cls, command, group_id, qq_id):
        permission = cls.get_permission(group_id, qq_id)
        if permission:
            if command in list(permission.keys()):
                return permission[command]
        return None
