from channels.routing import ProtocolTypeRouter, URLRouter
import app_channelmeter_live_test_scores.routing

application = ProtocolTypeRouter({
    'http': URLRouter(app_channelmeter_live_test_scores.routing.urlpatterns),
})
