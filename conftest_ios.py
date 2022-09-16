from os import environ
import os
import pytest
from appium import webdriver
from requests import request

@pytest.fixture(scope='function')
def test_setup_ios(request):
    test_name = request.node.name
    build = environ.get('BUILD', "Pytest iOS Sample")
    caps = {}
    caps["deviceName"] = "iPhone 11"
    caps["platformName"] = "iOS"
    caps["platformVersion"] = "14"
    caps["app"] = "APP_URL"  #add app (.ipa) url here
    caps["isRealMobile"] = True
    caps['build'] = build
    caps['name'] = test_name

    if os.environ.get("LT_USERNAME") is None:
        # Enter LT username here if environment variables have not been added
        username = "LT_USERNAME"
    else:
        username = os.environ.get("LT_USERNAME")

    if os.environ.get("LT_ACCESS_KEY") is None:
        # Enter LT accesskey here if environment variables have not been added
        accesskey = "LT_ACCESS_KEY"
    else:
        accesskey = os.environ.get("LT_ACCESS_KEY")

    url="https://"+username+":"+accesskey+"@mobile-hub.lambdatest.com/wd/hub"
    driver = webdriver.Remote(url, caps)
    request.cls.driver = driver
    
    yield driver
    
    def fin():
        #browser.execute_script("lambda-status=".format(str(not request.node.rep_call.failed if "passed" else "failed").lower()))
        if request.node.rep_call.failed:
            driver.execute_script("lambda-status=failed")
        else:
            driver.execute_script("lambda-status=passed")
            driver.quit()
    request.addfinalizer(fin)
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

