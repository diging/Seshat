import Resources.mendeley_client as mc
import config
import Resources.oauth2 as oauth

config_file = config.seshat_root + "/Resources/mendeley_config.json"
keys_file = config.seshat_root + "/Resources/keys_api.mendeley.com.pkl"

mendeley_config = mc.MendeleyClientConfig(config_file)

host = 'api.mendeley.com'
if hasattr(mendeley_config, "host"):
    host = mendeley_config.host

client = mc.MendeleyClient(mendeley_config.api_key, mendeley_config.api_secret, {"host":host})
tokens_store = mc.MendeleyTokensStore(keys_file)

#request_token, auth_url = client.get_auth_url()

request_token_string = "oauth_token_secret=715af44c2841120ad776d56f6a5a31cf&oauth_token=0d592d13fed27288cb15015ad536de7f05194031f"
verifier = "a253f7d471"
request_token = oauth.Token.from_string(request_token_string)
print type(request_token)
print type(verifier)


print client.verify_auth(request_token, verifier)