# -*- encoding=utf-8 -*-
"""
AirTest 手机自动化测试脚本模板
"""

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class MobileTestCase:
    """手机自动化测试基类"""

    def __init__(self, package_name=None):
        self.package = package_name
        self.poco = None
        self.device_info = None

    def setup_class(self):
        """测试类初始化"""
        pass

    def setup_method(self):
        """测试方法初始化"""
        self.init_poco()

    def init_poco(self):
        """初始化Poco框架"""
        self.poco = AndroidUiautomationPoco(use_adb=True)

    def start_app(self, package_name=None):
        """启动APP"""
        pkg = package_name or self.package
        start_app(pkg)
        sleep(2)

    def stop_app(self, package_name=None):
        """停止APP"""
        pkg = package_name or self.package
        stop_app(pkg)

    def take_screenshot(self, save_path=None):
        """截图"""
        path = save_path or f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        snapshot(filename=path)
        return path

    def swipe_up(self, times=1):
        """上滑"""
        for _ in range(times):
            swipe([500, 1500], [500, 500])
            sleep(0.5)

    def swipe_down(self, times=1):
        """下滑"""
        for _ in range(times):
            swipe([500, 500], [500, 1500])
            sleep(0.5)

    def swipe_left(self, times=1):
        """左滑"""
        for _ in range(times):
            swipe([800, 1000], [200, 1000])
            sleep(0.5)

    def swipe_right(self, times=1):
        """右滑"""
        for _ in range(times):
            swipe([200, 1000], [800, 1000])
            sleep(0.5)


class LoginTestCase(MobileTestCase):
    """登录测试用例"""

    def test_login_success(self):
        """测试正常登录"""
        pkg = "com.example.app"

        self.start_app(pkg)
        sleep(2)

        if self.poco("com.example.app:id/username").exists():
            self.poco("com.example.app:id/username").set_text("testuser")
            sleep(0.5)
            self.poco("com.example.app:id/password").set_text("123456")
            sleep(0.5)
            self.poco("com.example.app:id/login").click()
            sleep(2)

            assert self.poco("com.example.app:id/home").exists(), "未进入首页"

    def test_login_failed_wrong_password(self):
        """测试密码错误登录"""
        pkg = "com.example.app"

        self.start_app(pkg)
        sleep(2)

        self.poco("com.example.app:id/username").set_text("testuser")
        self.poco("com.example.app:id/password").set_text("wrongpass")
        self.poco("com.example.app:id/login").click()
        sleep(1)

        assert self.poco("com.example.app:id/error_msg").exists(), "未显示错误提示"


class PaymentTestCase(MobileTestCase):
    """支付测试用例"""

    def test_payment_success(self):
        """测试正常支付"""
        pkg = "com.example.app"

        self.start_app(pkg)
        self.navigate_to_payment()

        self.poco("com.example.app:id/amount").set_text("100")
        sleep(0.5)
        self.poco("com.example.app:id/pay_btn").click()
        sleep(2)

        assert self.poco("com.example.app:id/success").exists(), "支付未成功"

    def navigate_to_payment(self):
        """导航到支付页面"""
        self.poco("com.example.app:id/home").click()
        sleep(1)
        self.swipe_up(2)
        self.poco("com.example.app:id/payment").click()
        sleep(1)


class AssertHelper:
    """断言辅助类"""

    @staticmethod
    def assert_element_exists(poco_element, msg="元素不存在"):
        """断言元素存在"""
        assert poco_element.exists(), msg

    @staticmethod
    def assert_element_not_exists(poco_element, msg="元素仍存在"):
        assert not poco_element.exists(), msg

    @staticmethod
    def assert_text_equals(actual, expected, msg=None):
        """断言文本相等"""
        msg = msg or f"期望: {expected}, 实际: {actual}"
        assert actual == expected, msg

    @staticmethod
    def assert_image_exists(image_path, msg="图像不存在"):
        """断言图像存在"""
        assert exists(Template(image_path)), msg


if __name__ == "__main__":
    print("使用示例:")
    print("from airtest.core.api import *")
    print("auto_setup(__file__)")
    print("")
    print("test = LoginTestCase('com.example.app')")
    print("test.test_login_success()")
