# features/web/steps/app.steps.py
from behave import given, when, then
from src.web.app import create_app

# Ensure that create_app returns the app instance directly
app, _, _, _ = create_app()


@given("the web service is running")
def step_given_web_service_running(context):
    # Initialize app and set the context.app variable
    context.app = app
    context.client = context.app.test_client()


@when("I access the home endpoint")
def step_when_access_home_endpoint(context):
    context.response = context.client.get("/")


@then("the response status code should be {int:d}")
def step_then(context, int):
    assert (
        context.response.status_code == int
    ), f"Expected status code {int}, but got {context.response.status_code}"
