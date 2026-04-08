---
name: airtest-ide
version: 1.0.0
description: AirTest IDE 手机自动化脚本创建工具
author: Sisyphus
trigger:
  - airtest
  - 手机自动化
  - app自动化测试
  - 移动端自动化
  - airtest ide
  - 图像识别测试
  - poco框架
capabilities:
  - 环境配置指导
  - 脚本结构模板
  - 常用API参考
  - 最佳实践建议
  - 常见问题解决
category: testing
---

# AirTest IDE 手机自动化脚本 Skill

## 概述

AirTest 是一个基于图像识别和 Poco 框架的自动化测试工具，支持 Android、iOS 和 Windows 平台的自动化测试。

## 触发词

airtest、手机自动化、app自动化测试、移动端自动化、airtest ide、图像识别测试、poco框架

## 核心功能

### 环境准备

- Android 真机配置（USB 调试、adb 连接）
- 模拟器配置（夜神、雷电等）
- iOS 配置（WebDriverAgent）

### 脚本结构

```python
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_adb=True)
auto_setup(__file__)

def test_login():
    start_app("com.example.app")
    sleep(2)
    poco("com.example.app:id/username").set_text("testuser")
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

### 工具

`tools/airtest_helper.py` 提供：
- 环境检查
- 设备列表
- 项目创建

## 安装

```bash
npx skills add oracle614/airtest-ide -g -y
```

## 最佳实践

- 优先使用 Poco 替代图像识别
- 合理设置等待时间
- 使用条件等待而非固定等待

## 版本

v1.0.0