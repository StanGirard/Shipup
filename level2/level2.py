import json
import datetime

        
def main():
    carries = {}
    deliveries = {}
    deliveries_list = []
    with open('data/input.json') as json_file:
        data = json.load(json_file)
        # Generate dic of carriers delivery time for easy search and saturday shipping
        for p in data['carriers']:
            carries[p["code"]] = {"delivery_promise":p["delivery_promise"], "saturday_deliveries":p["saturday_deliveries"]}
        
        #Generate the deliveries output from packages
        for package in data['packages']:
            package_shipping_date = datetime.date.fromisoformat(package["shipping_date"])
            carrier_shipping_time = carries[package["carrier"]]["delivery_promise"]
            carrier_shipping_saturdays = carries[package["carrier"]]["saturday_deliveries"]

            for _ in range(carrier_shipping_time):
                weekday = package_shipping_date.weekday()
                if weekday == 4 and carrier_shipping_saturdays:
                   package_shipping_date = package_shipping_date + datetime.timedelta(1)
                elif weekday == 4 and not carrier_shipping_saturdays:
                    package_shipping_date = package_shipping_date + datetime.timedelta(3)
                elif weekday == 5:
                    package_shipping_date = package_shipping_date + datetime.timedelta(2)
                elif weekday == 6:
                    package_shipping_date = package_shipping_date + datetime.timedelta(1)
                else:
                    package_shipping_date = package_shipping_date + datetime.timedelta(1)
            
            deliveries_list.append({"package_id": package["id"],"expected_delivery": package_shipping_date.isoformat()})


    deliveries["deliveries"] = deliveries_list
    return deliveries
if __name__ == "__main__":
    print(main())