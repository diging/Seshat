import Resources.mendeley_client as mc
import config

config_file = config.seshat_root + "/Resources/mendeley_config.json"
keys_file = config.seshat_root + "/Resources/keys_api.mendeley.com.pkl"

mendeley_config = mc.MendeleyClientConfig(config_file)

host = 'api.mendeley.com'
if hasattr(mendeley_config, "host"):
    host = mendeley_config.host

client = mc.MendeleyClient(mendeley_config.api_key, mendeley_config.api_secret, {"host":host})
tokens_store = mc.MendeleyTokensStore(keys_file)

request_token, auth_url = client.get_auth_url()

print request_token
print auth_url
