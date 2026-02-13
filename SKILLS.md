# autopieceone - Piece One 自动移动脚本

让 OpenClaw 自动化控制 piece.one 网页游戏中的角色移动。

## 功能

- 在屏幕中心的圆周上随机移动角色
- 随机执行点击、丢道具、聊天、改色等动作
- 启动时自动设置角色名称和颜色

## 仓库

- **地址**: https://github.com/imtonyjaa/autopieceone
- **克隆**: `git clone https://github.com/imtonyjaa/autopieceone.git`
- **更新**: `git pull`

## 前置要求

### 1. 安装 Python 依赖

```bash
pip install pyautogui pyperclip python-dotenv
```

### 2. 找到 Python 路径

不同系统路径不同：
- **Windows 常见**: `C:\Users\<用户名>\AppData\Local\Programs\Python\Python312\python.exe`
- **Mac**: `/usr/bin/python3` 或 `python3`
- **Linux**: `python3`

可用命令查找：
```bash
# Windows
where python

# Mac/Linux
which python3
```

## 启动步骤

### 第一次启动

```python
# 1. 克隆仓库
exec(command="git clone https://github.com/imtonyjaa/autopieceone.git")

# 2. 检查浏览器标签页
browser(action="tabs")

# 3. 打开游戏网页（必须带 widget=2&from=claw）
browser(action="open", targetUrl="https://piece.one/?widget=2&from=claw")

# 4. 等待游戏加载
time.sleep(3)

# 5. 启动脚本（传入角色名）
# Windows 示例路径，请替换为你的实际 Python 路径
exec(command="python autopieceone/autopieceone.py 角色名")
```

### 后续启动

```python
# 1. 拉取最新代码
exec(command="git -C autopieceone pull")

# 2. 关闭旧标签页，打开新网页
browser(action="tabs")
# 记录旧标签页 ID，然后关闭
browser(action="close", targetId="<旧ID>")
browser(action="open", targetUrl="https://piece.one/?widget=2&from=claw")

# 3. 启动脚本
exec(command="python autopieceone/autopieceone.py 角色名")
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 角色名 | 启动时设置的名称 | 大钳子 |

## 命令格式

- **改名**: `name:名称`
- **改色**: `color: #RRGGBB`
- **丢物品**: `drop:🍎`

## 注意事项

1. **URL 必须带参数**: `?widget=2&from=claw`
2. **游戏窗口需在最前面**: 脚本使用系统级鼠标控制
3. **终止脚本**: 鼠标移到屏幕角落可触发 pyautogui FAILSAFE 立即停止
