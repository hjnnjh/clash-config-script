#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   add-my-config.py
@Time    :   2024/03/10 14:47:59
@Author  :   Jinnan Huang 
@Contact :   jinnan_huang@stu.xjtu.edu.cn
@Desc    :   None
"""
import yaml
from loguru import logger

# 读取配置文件和规则文件
CONFIG_FILE_NAME = "IPLC-Converted-2024"  # 自己按照配置文件名修改
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
    proxy["name"] for proxy in proxies if not proxy["name"].startswith("香港")
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

# 保存为新文件
updated_config_file = f"{CONFIG_FILE_NAME}-with-rules.yaml"
with open(
    updated_config_file,
    "w",
    encoding="utf-8",
) as f:
    yaml.dump(config_data, f, allow_unicode=True)

logger.success(f"配置文件已经更新为 {updated_config_file}!")
