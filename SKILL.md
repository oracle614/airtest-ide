# AirTest IDE 手机自动化脚本 Skill

## 概述

AirTest 是一个基于图像识别和Poco框架的自动化测试工具，支持 Android、iOS 和 Windows 平台的自动化测试。本 Skill 提供 AirTest IDE 的使用指导和手机自动化脚本创建方法。

## 适用场景

当用户表达以下意图时使用本 Skill：

- 创建手机自动化测试脚本
- 使用 AirTest IDE 进行 APP 自动化测试
- 编写基于图像识别的自动化用例
- 配置 Android/iOS 真机或模拟器测试环境

## 核心功能

### 1. 环境准备

#### Android 真机配置

- 开启手机的开发者选项和 USB 调试
- 使用数据线连接电脑，确保 `adb devices` 能识别设备
- 安装手机驱动（必要时）

#### 模拟器配置

- 夜神模拟器、雷电模拟器等
- 确保模拟器与 AirTest IDE 连接正常

#### iOS 配置

- 需要安装 WebDriverAgent
- 支持 Xcode 配合使用

### 2. 脚本结构

AirTest 脚本基本结构如下：

```python
# -*- encoding=utf-8 -*-
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# 初始化 Poco
poco = AndroidUiautomationPoco(use_adb=True)

# 初始化设备
auto_setup(__file__)

# 测试用例
def test_login():
    # 启动 APP
    start_app("com.example.app")
    sleep(2)
    
    # 点击登录按钮
    touch(Template(r"tpl/login_btn.png"))
    sleep(1)
    
    # 输入用户名
    poco("com.example.app:id/username").set_text("testuser")
    
    # 输入密码
    poco("com.example.app:id/password").set_text("123456")
    
    # 点击确认
    poco("com.example.app:id/login").click()
    
    # 断言
    assert exists(Template(r"tpl/home_page.png")), "登录失败"
```

### 3. 常用 API

#### 图像识别 API

| 方法 | 说明 | 示例 |
|------|------|------|
| touch | 点击图像或坐标 | `touch(Template("tpl/btn.png"))` |
| exists | 判断图像是否存在 | `exists(Template("tpl/btn.png"))` |
| wait | 等待图像出现 | `wait(Template("tpl/btn.png"))` |
| wait_until_not_exist | 等待图像消失 | `wait_until_not_exist(Template("tpl/loading.png"))` |
| swipe | 滑动操作 | `swipe((x1, y1), (x2, y2))` |
| text | 输入文本 | `text("hello")` |

#### Poco 框架 API

| 方法 | 说明 | 示例 |
|------|------|------|
| poco() | 选择元素 | `poco("android:id/title")` |
| click | 点击元素 | `poco("btn").click()` |
| set_text | 设置文本 | `poco("input").set_text("text")` |
| get_text | 获取文本 | `poco("text").get_text()` |
| wait | 等待元素 | `poco("loading").wait()` |
| child | 子元素 | `poco("container").child("btn")` |

#### 断言 API

```python
# 图像断言
assert exists(Template("tpl/success.png")), "未找到成功图标"

# 文本断言
assert poco("username").get_text() == "testuser"

# 超时断言
assert wait(Template("tpl/loading.png")).timeout(10), "加载超时"
```

### 4. 脚本组织

#### 项目目录结构

```
TestProject/
├── air/
│   ├── test_case1.air/      # 图像资源包
│   ├── test_case2.air/
│   └── ...
├── script/
│   ├── test_login.py        # 测试脚本
│   ├── test_checkout.py
│   └── ...
├── report/                  # 测试报告
├── config.py                # 配置文件
└── main.py                  # 入口文件
```

#### 批量执行脚本

```python
# main.py
import airtest.report
from airtest.core.api import *

# 执行多个测试用例
def run_tests():
    cases = [
        "script/test_login.py",
        "script/test_payment.py",
        "script/test_profile.py"
    ]
    
    for case in cases:
        exec(open(case).read())

if __name__ == "__main__":
    run_tests()
```

### 5. 报告生成

```python
from airtest.report.report import LogToHtml

# 生成 HTML 报告
log = LogToHtml(script_root=r".", log_file=r"air/log.txt", output_dir=r"report")
log.report()
```

## 最佳实践

### 图像识别优化

- 截图时选择特征明显的区域
- 避免截图包含文字（不同分辨率可能识别失败）
- 阈值设置合理值（默认 0.7）

### 元素定位优化

- 优先使用稳定的唯一标识符
- 避免使用索引定位
- 使用相对路径定位动态元素

### 等待策略

- 设置合理的等待时间
- 使用条件等待而非固定等待
- 处理加载动画和弹窗

### 异常处理

```python
from airtest.core.api import *

try:
    touch(Template("tpl/btn.png"))
except TargetNotFoundError:
    # 处理未找到元素
    log("按钮未找到")
except Exception as e:
    log(f"错误: {e}")
finally:
    # 清理操作
    pass
```

## 常见问题

### 连接问题

- 检查 adb 是否正常：`adb devices`
- 重启 adb 服务：`adb kill-server && adb start-server`
- 检查手机 USB 调试是否开启

### 图像识别失败

- 调整截图范围，避免背景干扰
- 提高匹配阈值
- 尝试多种图像识别模式

### 脚本运行慢

- 减少不必要的等待
- 使用 Poco 替代图像识别
- 优化元素定位方式

## 相关工具

- AirTest IDE：可视化脚本编辑器
- Poco：UI 元素定位框架
- AirTest：底层自动化框架
- STF：设备管理平台

## 使用示例

用户：帮我创建一个APP登录测试脚本

```python
# 按照以下步骤创建脚本
1. 连接手机设备
2. 启动 AirTest IDE
3. 创建新项目
4. 使用Poco或图像识别编写登录流程
5. 保存并运行测试
```