import jsonrpclib

RECOMMENDATION_SREVICE_HOST = 'localhost'
RECOMMENDATION_SREVICE_PORT = '5050'
RECOMMENDATION_SREVICE_URL = 'http://' + RECOMMENDATION_SREVICE_HOST + ':' + RECOMMENDATION_SREVICE_PORT

client = jsonrpclib.ServerProxy(RECOMMENDATION_SREVICE_URL)

def get_preference_for_user(user_id):
    preference = client.get_preference_for_user(user_id)
    print("Preference list: %s" % str(preference))
    return preference
