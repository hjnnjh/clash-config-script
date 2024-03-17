#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   add-my-config.py
@Time    :   2024/03/10 14:47:59
@Author  :   Jinnan Huang 
@Contact :   jinnan_huang@stu.xjtu.edu.cn
@Desc    :   None
"""
import re
import os

import paramiko
import yaml
from loguru import logger


def upload_clash_config_file_to_server(local_file: str, hostname: str):
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    host_config = ssh_config.lookup(hostname)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=host_config["hostname"],
        username=host_config["user"],
        key_filename=host_config["identityfile"],
        port=host_config.get("port", 22),
    )
    sftp = ssh.open_sftp()
    clash_config_file = f"/home/{host_config['user']}/.config/clash/config.yaml"
    logger.info(
        f"将配置文件{local_file}上传到服务器{hostname}下的{clash_config_file}"
    )
    sftp.put(local_file, clash_config_file)
    sftp.close()
    ssh.close()
    logger.success("上传成功！")


# 读取配置文件和规则文件
CONFIG_FILE_NAME = input("请输入配置文件名（不包括后缀.yaml）：")
ONEDRIVE_SAVE_PATH = (
    "your-onedrive-path/ClashConfigs/your-config-folder-name"
)
os.makedirs(ONEDRIVE_SAVE_PATH, exist_ok=True)

with open(f"{CONFIG_FILE_NAME}.yaml", "r", encoding="utf-8") as f:
    config_data = yaml.safe_load(f)

with open("rules.yaml", "r", encoding="utf-8") as f:
    rules_data = yaml.safe_load(f)

# 获取proxies列表
proxies = config_data.get("proxies", [])

# 创建新的proxy-groups
new_groups = []

# ♻️ 自动选择(日美)
daily_proxies = [
    proxy["name"]
    for proxy in proxies
    if proxy["name"].startswith("日本") or proxy["name"].startswith("美国")
]
daily_group = {
    "name": "♻️ 自动选择(日美)",
    "type": "select",
    "proxies": daily_proxies,
}
new_groups.append(daily_group)

# 📧 Apple Mail
mail_proxies = [
    proxy["name"] for proxy in proxies if proxy["name"].startswith("香港")
]
mail_group = {
    "name": "📧 Apple Mail",
    "type": "select",
    "proxies": mail_proxies,
}
new_groups.append(mail_group)

# 🤖️ ChatGPT
chatgpt_proxies = [
    proxy["name"]
    for proxy in proxies
    if re.match(r"(日本|美国)\d+", proxy["name"]) and proxy["name"][2:] > "05"
]
chatgpt_group = {
    "name": "🤖️ ChatGPT",
    "type": "select",
    "proxies": chatgpt_proxies,
}
new_groups.append(chatgpt_group)

# 📹 HBOGO-Asia
hbogo_proxies = mail_proxies
hbogo_group = {
    "name": "📹 HBOGO-Asia",
    "type": "select",
    "proxies": hbogo_proxies,
}
new_groups.append(hbogo_group)

# 将新的proxy-groups追加到原有配置中
existing_groups = config_data.get("proxy-groups", [])
config_data["proxy-groups"] = existing_groups + new_groups

# 添加规则
rules = rules_data.get("rules", [])
config_data["rules"] = rules

updated_config_file = f"{CONFIG_FILE_NAME}-with-rules.yaml"
onedrive_config_file = f"{ONEDRIVE_SAVE_PATH}/{updated_config_file}"
# 更新本地文件
with open(
    updated_config_file,
    "w",
    encoding="utf-8",
) as f:
    yaml.dump(config_data, f, allow_unicode=True)
logger.success(f"配置文件保存到：{updated_config_file}")
# 将文件同步到OneDrive
with open(
    onedrive_config_file,
    "w",
    encoding="utf-8",
) as f:
    yaml.dump(config_data, f, allow_unicode=True)
logger.success(f"配置文件保存到：{onedrive_config_file}")

# 上传到服务器
remote_servers = ["you", "server", "names"]
for remote_server_name in remote_servers:
    upload_clash_config_file_to_server(
        updated_config_file,
        remote_server_name,
    )
