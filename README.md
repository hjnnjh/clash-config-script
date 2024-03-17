# 使用Python脚本自动为ClashX `config.yaml`文件添加自定义规则

因为本人使用了`subconvert`转化了`clash`的订阅链接，但是每次更新订阅链接后`config.yaml`中的自定义规则都会被覆盖掉，并且ClashX不支持CFW的`parser`，因此每次更新后都需要手动添加规则，所以写了这个脚本来自动添加规则。

## 脚本功能
- 新建一些`proxies groups`;
- 通过`rules.yaml`文件自定义流量转发规则并添加到`config.yaml`文件;
- 添加规则之后将自动在当前目录下保存为`{input-config-file-name}-with-rules.yaml`文件。

## 额外功能
- 同步到`OneDrive`;
- 自动上传到`RemoteServer`下的`clash`文件夹。