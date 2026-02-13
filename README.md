# Auto Piece One - 自动化脚本使用说明

## 1. 环境准备

本脚本基于 Python 开发，依赖于 `pyautogui` 库进行鼠标键盘模拟。

### 1.1 安装 Python 3
请确保系统已安装 Python 3。

### 1.2 创建虚拟环境 (推荐)
为了避免污染全局环境，建议使用虚拟环境运行。

```bash
# 在项目根目录下执行
python3 -m venv venv
```

### 1.3 激活虚拟环境

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```cmd
  venv\Scripts\activate
  ```

### 1.4 安装依赖
激活虚拟环境后，安装所需依赖（包含 `pyautogui` 和 `python-dotenv`）：

```bash
pip install pyautogui python-dotenv
```

---

## 2. 配置说明

### 2.1 调试模式 (Debug Mode)
项目使用了 `.env` 文件进行配置。首次运行时，请确保根目录下存在 `.env` 文件。

在 `.env` 文件中设置：
```env
IS_DEBUG=true
```
- **IS_DEBUG=true**: 仅打印日志，不执行操作（推荐首次运行测试）。
- **IS_DEBUG=false**: 启用实际鼠标键盘操作。

### 2.2 安全机制 (Fail-Safe)
`pyautogui.FAILSAFE = True`
- 启用后，由于程序失控，你可以**把鼠标快速移动到屏幕的四个角落之一**，脚本会立即抛出异常并停止运行。

### 2.3 执行间隔 (Execution Interval)
`EXECUTION_INTERVAL = 5.0`
- 设置每次循环执行后的等待时间（秒）。默认设置为 5 秒。

### 2.4 掉落物列表 (AVAILABLE_DROPS)
`AVAILABLE_DROPS` 是一个列表，包含了所有可能的掉落物 emoji。你可以根据需要增删改。

---

## 3. 运行脚本

确保终端已激活虚拟环境，然后执行：

```bash
python autopieceone.py
```

### 运行时逻辑
脚本启动后会无限循环执行，按 `Ctrl+C` 终止。

逻辑分支（基于随机数）：
1. **< 30%**: 移动鼠标并按住左键 (0.5-2秒)。
2. **30% - 60%**: 仅移动鼠标。
3. **>= 60%**: 特殊操作
    - **20% (子概率)**: 请求 Chat API，自动输入返回的内容。
    - **30% (子概率)**: 输入 `drop:` 并随机选择一个掉落物。
    - **50% (子概率)**: 跳过。

---

## 4. 常见问题

- **权限问题 (macOS)**: 首次运行如果是非 Debug 模式，macOS 可能会提示终端需要“辅助功能”权限以控制鼠标键盘。请在 `系统设置 -> 隐私与安全性 -> 辅助功能` 中勾选你的终端应用 (如 Terminal 或 iTerm)。
- **Chat API 403 错误**: 如果遇到 HTTP 403，通常是因为 API 需要浏览器标识 (User-Agent)。这在后续版本中会进行优化。
