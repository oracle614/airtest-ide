# AirTest IDE 手机自动化脚本 Skill

## 概述

AirTest 是一个基于图像识别和 Poco 框架的自动化测试工具，支持 Android、iOS 和 Windows 平台的自动化测试。本 Skill 提供 AirTest IDE 的使用指导和手机自动化脚本创建方法。

## 安装

```bash
npx skills add 你的用户名/airtest-ide -g -y
```

## 适用场景

- 创建手机自动化测试脚本
- 使用 AirTest IDE 进行 APP 自动化测试
- 编写基于图像识别的自动化用例
- 配置 Android/iOS 真机或模拟器测试环境

## 触发词

airtest、手机自动化、app自动化测试、移动端自动化、airtest ide、图像识别测试、poco框架

## 核心功能

### 环境准备

- Android 真机配置（USB 调试、adb 连接）
- 模拟器配置（夜神、雷电等）
- iOS 配置（WebDriverAgent）

### 脚本结构

```python
# -*- encoding=utf-8 -*-
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_adb=True)
auto_setup(__file__)

def test_login():
    start_app("com.example.app")
    sleep(2)
    poco("com.example.app:id/username").set_text("testuser")
    poco("com.example.app:id/password").set_text("123456")
    poco("com.example.app:id/login").click()
    assert exists(Template(r"tpl/home_page.png"))
```

### 常用 API

- touch / click - 点击操作
- exists / wait - 图像识别
- swipe - 滑动操作
- text / set_text - 文本输入

### 模板文件

`templates/test_template.py` 包含：
- MobileTestCase 基类
- LoginTestCase 登录测试
- PaymentTestCase 支付测试
- AssertHelper 断言辅助

### 工具

`tools/airtest_helper.py` 提供：
- 环境检查
- 设备列表
- 项目创建
- 报告生成

## 最佳实践

- 优先使用 Poco 替代图像识别
- 合理设置等待时间
- 使用条件等待而非固定等待

## 版本

v1.0.0 - 初始版本

## 作者

Sisyphus AI