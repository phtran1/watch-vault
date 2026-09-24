import json
from watch import Watch, Collection
from datetime import date, timedelta

if __name__ == "__main__":
    my_vault = Collection()
    watch1 = Watch("Seiko", "Selection", "SBTM325")
    watch2 = Watch("Seiko", "A904 5199")
    my_vault.add(watch1)
    my_vault.add(watch2)
    watch4 = Watch("Citizen", "Garison", movement_type="Quartz", ref_no='BM8180-03E', accuracy_month=15)
    watch4.specs()
    watch4.last_reset_date = date.today() - timedelta(days=10)
    watch4.log_drift(2, as_of=date.today() - timedelta(days=7))
    watch4.log_drift(4, as_of=date.today() - timedelta(days=4))
    watch4.log_drift(4, as_of=date.today() - timedelta(days=3))
    watch4.log_drift(5, as_of=date.today() - timedelta(days=1))
    my_vault.add(watch4)
    watch4.reset()
    watch4.log_drift(3, as_of=date.today() + timedelta(days=1))
    watch4.log_drift(3, as_of=date.today() + timedelta(days=2))
    watch4.log_drift(3, as_of=date.today() + timedelta(days=3))
    print(watch4.health_score())
    print(watch4.health_score(1))
    my_vault.export_to_json()
