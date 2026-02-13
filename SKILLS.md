# autopieceone - Piece One 自动移动脚本

让 OpenClaw 自动化控制 piece.one 网页游戏中的角色移动。

## 概述

本技能用于自动控制 [piece.one](https://piece.one/) 网页游戏中的角色：
- 在屏幕中心的圆周上随机移动
- 随机执行点击、丢道具、聊天等动作
- 支持传入角色名称

## 前置要求

### 1. 安装 Python 依赖

```bash
pip install pyautogui pyperclip python-dotenv
```

### 2. 启动 piece.one 网页

使用 OpenClaw 浏览器控制：

```python
# 1. 先检查是否已有 piece.one 标签页
browser(action="tabs")

# 2. 如果没有，才打开新标签页
browser(action="open", targetUrl="https://piece.one/")
```

## 使用方法

### 基本启动

```bash
python autopieceone.py 大钳子
```

参数说明：
- `argv[1]`: 角色名称（默认：大钳子）

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| IS_DEBUG | false | 设为 "true" 可模拟运行（只打印日志，不执行动作） |

### 示例

```bash
# 调试模式
IS_DEBUG=true python autopieceone.py 大钳子

# 正式运行
IS_DEBUG=false python autopieceone.py 大钳子
```

## 完整工作流

### OpenClaw Agent 标准操作流程

```python
# 1. 检查是否已有 piece.one 标签页
browser(action="tabs")

# 2. 如果没有，打开网页
browser(action="open", targetUrl="https://piece.one/")

# 3. 等待页面加载 (1-2秒)
time.sleep(2)

# 4. 启动 Python 脚本，传入角色名称
exec(command="python autopieceone/autopieceone.py 大钳子")
```

### 逻辑说明

脚本启动后会：

1. **第一动作**：设置角色名称
   - 复制 `name:大钳子` 到剪贴板
   - 粘贴并回车

2. **循环执行**（每 5 秒一次）：
   - 随机 < 0.3 (30%)：移动 + 点击（长按 0.5-2 秒）
   - 随机 < 0.6 (30%)：只移动，不点击
   - 随机 >= 0.6 (40%)：
     - 子随机 < 0.2 (8%)：调用 Chat API 发聊天
     - 子随机 0.2-0.5 (12%)：丢弃随机物品

## 参数配置

### 移动参数

```python
radius = 150          # 圆周半径（像素）
EXECUTION_INTERVAL = 5.0  # 执行间隔（秒）
```

### 可用物品列表

脚本内置了大量 emoji 物品用于丢弃命令。

## 注意事项

1. **窗口位置**：脚本假设 piece.one 窗口在主显示器上，且游戏画面居中
2. **坐标计算**：基于屏幕中心点 (width//2, height//2) 计算圆周坐标
3. **编码问题**：Windows 下使用 `pyperclip` 避免 emoji 输入问题
4. **终止脚本**：将鼠标移到屏幕角落可触发 pyautogui FAILSAFE 立即停止

## 故障排除

### 脚本启动报错 "ModuleNotFoundError"

缺少依赖，执行：
```bash
pip install pyautogui pyperclip python-dotenv
```

### 一直输入乱码

检查是否在 DEBUG 模式：
```bash
echo $IS_DEBUG  # 应该显示 "false"
```

### 浏览器标签页重复打开

务必先检查 `browser(action="tabs")`，确认没有 piece.one 标签页后再打开新标签页。

## 文件结构

```
autopieceone/
├── autopieceone.py   # 主脚本
├── .env              # 环境变量配置（可选）
├── .gitignore
└── README.md
```

## 相关命令

```bash
# 查看当前运行的 Python 进程
tasklist | findstr python

# 终止脚本
taskkill /F /PID <PID>
```
