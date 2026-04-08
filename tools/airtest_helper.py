#!/usr/bin/env python3
import subprocess
import os
import sys


class AirTestIDE:
    def __init__(self, workspace_path=None):
        self.workspace = workspace_path or os.getcwd()
        self.project_path = None
        self.devices = []

    def check_environment(self):
        print("检查 AirTest IDE 环境...")

        results = {
            "airtest": self._check_airtest(),
            "adb": self._check_adb(),
            "poco": self._check_poco(),
        }

        print("\n环境检查结果:")
        for name, status in results.items():
            icon = "✓" if status else "✗"
            print(f"  {icon} {name}: {'已安装' if status else '未安装'}")

        return all(results.values())

    def _check_airtest(self):
        try:
            import airtest

            print(f"  AirTest 版本: {airtest.__version__}")
            return True
        except ImportError:
            return False

    def _check_adb(self):
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            print(f"  ADB: {version}")
            return True
        return False

    def _check_poco(self):
        try:
            import poco

            print(f"  Poco 版本: {poco.__version__}")
            return True
        except ImportError:
            return False

    def list_devices(self):
        print("\n获取已连接设备...")
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]

        self.devices = []
        for line in lines:
            if line.strip():
                parts = line.split("\t")
                if len(parts) == 2:
                    device = {"serial": parts[0], "status": parts[1]}
                    self.devices.append(device)
                    print(f"  设备: {device['serial']} ({device['status']})")

        return self.devices

    def create_project(self, project_name, platform="android"):
        print(f"\n创建项目: {project_name}")

        project_path = os.path.join(self.workspace, project_name)
        os.makedirs(project_path, exist_ok=True)

        dirs = ["air", "script", "report", "tpl"]
        for d in dirs:
            os.makedirs(os.path.join(project_path, d), exist_ok=True)

        config_content = f"""# -*- encoding=utf-8 -*-
DEVICES = {{
    "Android": {{
        "host": "127.0.0.1",
        "port": 5037,
        "platform": "Android",
        "uuid": "",
        "package": "com.example.app",
        "activity": ".MainActivity"
    }},
    "iOS": {{
        "host": "127.0.0.1",
        "port": 5037,
        "platform": "iOS",
        "uuid": ""
    }}
}}

CURRENT_DEVICE = "Android"

PROJECT_NAME = "{project_name}"
PROJECT_PATH = "{project_path}"
"""

        with open(os.path.join(project_path, "config.py"), "w", encoding="utf-8") as f:
            f.write(config_content)

        main_script = f"""# -*- encoding=utf-8 -*-
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

auto_setup(__file__)

def main():
    poco = AndroidUiautomationPoco(use_adb=True)
    start_app("com.example.app")
    sleep(2)
    print("测试完成")

if __name__ == "__main__":
    main()
"""

        with open(
            os.path.join(project_path, "script", "main.py"), "w", encoding="utf-8"
        ) as f:
            f.write(main_script)

        self.project_path = project_path
        print(f"项目创建成功: {project_path}")
        return project_path

    def run_test(self, script_path, device_serial=None):
        print(f"\n运行测试: {script_path}")

        cmd = ["python", script_path, "--device", device_serial or "Android"]

        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"错误: {result.stderr}")

        return result.returncode == 0

    def generate_report(self, log_file, output_dir="report"):
        print(f"\n生成测试报告...")

        try:
            from airtest.report.report import LogToHtml

            log = LogToHtml(
                script_root=self.project_path or ".",
                log_file=log_file,
                output_dir=output_dir,
            )
            log.report()
            print(f"报告生成成功: {output_dir}")
            return True
        except Exception as e:
            print(f"报告生成失败: {e}")
            return False


def main():
    ide = AirTestIDE("/Users/zhangjian/Desktop/AirTestProjects")

    print("=" * 50)
    print("AirTest IDE 自动化工具")
    print("=" * 50)

    if not ide.check_environment():
        print("\n请先安装 AirTest 相关依赖:")
        print("  pip install airtest poco")
        return

    ide.list_devices()

    project = input("\n请输入项目名称 (直接回车跳过): ").strip()
    if project:
        ide.create_project(project)

    print("\n完成!")


if __name__ == "__main__":
    main()
