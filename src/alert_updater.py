from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alerts_to_update = Alert.find_needing_update()
print(alerts_to_update)
for alert in alerts_to_update:
    alert.do_price_check()
    alert.send_email_if_price_reached()
