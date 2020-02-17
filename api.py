import json
import requests
import datetime


class BaseAPI:
    api_url = None
    url_postfix = None
    failure_message = "something wrong"

    def __call__(self, **kwargs):
        is_success, message, objects = self.make_request(**kwargs)
        if is_success:
            return self.success_trigger(objects)
        else:
            return self.failure_trigger(message)

    def get_params(self, **kwargs) -> dict:
        return kwargs or {}

    def form_url(self, **kwargs):
        params = self.get_params(**kwargs)
        params_string = ""
        for param_name, param_value in params.items():
            params_string = f"{params_string}{param_name}={param_value}&"
        return f"{self.api_url}{self.url_postfix}?{params_string[:-1]}"

    def make_request(self, **kwargs) -> tuple:
        response = requests.get(self.form_url(**kwargs))
        if response.status_code == 200:
            return True, None, {"results": json.loads(response.text)}
        else:
            return False, json.loads(response.text)["error"], None

    def success_trigger(self, objects: dict):
        return True, None, objects

    def failure_trigger(self, message):
        message = message if message else self.failure_message
        return False, message, None


class ExchangeratesAPILatest(BaseAPI):
    api_url = "https://api.exchangeratesapi.io/"
    url_postfix = "latest"

    def get_params(self, **kwargs) -> dict:
        kwargs["base"] = kwargs.pop("base", "USD")
        return kwargs

    def success_trigger(self, objects: dict):
        objects["rates"] = json.dumps(objects["results"]["rates"])
        objects["date"] = datetime.datetime.now()
        objects.pop("results")
        return super().success_trigger(objects)


class ExchangeratesAPIHistory(BaseAPI):
    api_url = "https://api.exchangeratesapi.io/"
    url_postfix = "history"

    def get_params(self, **kwargs) -> dict:
        kwargs["start_at"] = kwargs.pop("start_date", None)
        kwargs["end_at"] = kwargs.pop("end_date", str(datetime.date.today()))
        kwargs["base"] = kwargs.pop("base", None)
        kwargs["symbols"] = kwargs.pop("symbol", None)
        return kwargs

    def success_trigger(self, objects: dict):
        objects["rates"] = objects.pop("results")["rates"]
        return super().success_trigger(objects)
