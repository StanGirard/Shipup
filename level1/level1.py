import json
import datetime

        
def main():
    carries = {}
    deliveries = {}
    deliveries_list = []
    with open('data/input.json') as json_file:
        data = json.load(json_file)
        # Generate dic of carriers delivery time for easy search - Redundant
        for p in data['carriers']:
            carries[p["code"]] = p["delivery_promise"]
        
        #Generate the deliveries output from packages
        for i in data['packages']:
            package_carrier = i["carrier"]
            package_shipping_date = datetime.date.fromisoformat(i["shipping_date"]) + datetime.timedelta(carries[i["carrier"]])
            deliveries_list.append({"package_id": i["id"],"expected_delivery": package_shipping_date.isoformat()})


    deliveries["deliveries"] = deliveries_list
    return deliveries
if __name__ == "__main__":
    print(main())