from screenshotFileName import get_screenshot_new_file_name
from behave.model_core import Status


def before_scenario(context, scenario):
    if context.config.userdata.get("mobile"):
        print("mobile")
        from sut.model.mobileMainPage import MainPage
    else:
        print("desktop")
        from sut.model.mainPage import MainPage
    context.main_page = MainPage("default")


def after_step(context, step):
    context.failed_step_name = ""
    if step.status == Status.failed:
        context.failed_step_name = step.keyword + ' ' + step.name


def after_scenario(context, scenario):
    if context.failed:
        screenshot_name = get_screenshot_new_file_name(scenario.name, context.failed_step_name)
        screenshot = context.current_page.get_screenshot(screenshot_name)
        #
        # Workaround for https://github.com/behave/behave/issues/906
        # --> context.attach issue "list index out of range".
        #
        context._runner.formatters[0]._step_index -= 1
        ## Workaround END
        context.attach("image/png", screenshot)
    context.current_page.close()
