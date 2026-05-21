from mcdreforged.api.all import *

metadata = {
    'id': 'player_scale',
    'version': '1.0',
    'name': '玩家缩放',
    'description': '体型缩放插件',
    'author': 'Miraitowa-alt'
}

def on_load(server: PluginServerInterface, old_module):
    server.register_help_message("!!size", "改变自己的体型大小")

def on_user_info(server: PluginServerInterface, info: Info):
    content = info.content.strip()

    # 只识别 !!size 指令
    if not content.startswith("!!size"):
        return

    command = content.split()
    player_name = getattr(info, 'player', None)

    # 确保是玩家在游戏内执行
    if not player_name:
        server.reply(info, "§c[!] 该指令只能由游戏内玩家执行")
        return

    # 1. 帮助菜单
    if len(command) == 1:
        server.reply(info, "§b--- [ 玩家缩放 ] ---")
        server.reply(info, "§e!!size <数字> §7- 变大或变小 (如 0.5 或 2)")
        server.reply(info, "§e!!size reset  §7- 恢复正常体型")
        return

    sub_cmd = command[1]

    # 2. 恢复默认大小
    if sub_cmd == "reset":
        server.execute(f'attribute {player_name} minecraft:scale base set 1.0')
        server.reply(info, "§a 已恢复正常体型")

    # 3. 设置具体倍数
    else:
        try:
            scale_val = float(sub_cmd)
            # 限制范围：0.1 (超小) 到 10.0 (超大)
            if 0.1 <= scale_val <= 10.0:
                server.execute(f'attribute {player_name} minecraft:scale base set {scale_val}')
                server.reply(info, f"§a 成功将你的体型设为 §f{scale_val} §a倍")
            else:
                server.reply(info, "§c[!] 请输入 0.1 到 10.0 之间的数字")
        except ValueError:
            server.reply(info, "§c[!] 请输入有效的数字，例如: !!size 0.5")