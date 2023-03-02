from slack_sdk import WebClient

signing_secret_mock = "secret"
valid_token = "xoxb-valid"
mock_api_server_base_url = "http://localhost:8888"

web_client_mock = WebClient(
    token=valid_token,
    base_url=mock_api_server_base_url,
)
