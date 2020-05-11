import json
import datetime
import math

# Calculate the Oversea threshold.
def calculate_oversea(oversea_table, source, destination, threshold):
    if source == destination:
        return 0
    distance = oversea_table[source][destination]
    return math.floor(distance / threshold)

def calculate_shipping(carries, package, data):
    # Assign value to variable for easy usage
    package_shipping_date = datetime.date.fromisoformat(package["shipping_date"])
    carrier_shipping_time = carries[package["carrier"]]["delivery_promise"]
    carrier_shipping_saturdays = carries[package["carrier"]]["saturday_deliveries"]

    # Calculate threshold
    threshold = calculate_oversea(data['country_distance'], package["origin_country"], package["destination_country"], carries[package["carrier"]]["oversea_delay_threshold"])

    # Iterate one day at a time and add days to the shipping date     
    for _ in range(carrier_shipping_time + threshold):
        weekday = package_shipping_date.weekday()
        
        # If Friday and ships on Saturday
        if weekday == 4 and carrier_shipping_saturdays:
            package_shipping_date = package_shipping_date + datetime.timedelta(1)

        # If Friday and no shipping on Saturday 
        elif weekday == 4 and not carrier_shipping_saturdays:
            package_shipping_date = package_shipping_date + datetime.timedelta(3)
        # If Saturday
        elif weekday == 5:
            package_shipping_date = package_shipping_date + datetime.timedelta(2)
        # If Sunday
        elif weekday == 6:
            package_shipping_date = package_shipping_date + datetime.timedelta(1)
        # Any other day
        else:
            package_shipping_date = package_shipping_date + datetime.timedelta(1)
    # Returns the package id and shipping date
    return {"package_id": package["id"],"expected_delivery": package_shipping_date.isoformat()}
              
        
def main():
    carries = {}
    deliveries = {}
    deliveries_list = []

    # Load the input file
    with open('data/input.json') as json_file:
        data = json.load(json_file)

        # Generate dic of carriers delivery time for easy search and saturday shipping with carries as key
        # Helps with faster search
        for p in data['carriers']:
            carries[p["code"]] = {"delivery_promise":p["delivery_promise"], "saturday_deliveries":p["saturday_deliveries"], "oversea_delay_threshold": p["oversea_delay_threshold"]}
        
        #Generate the deliveries output from packages
        for package in data['packages']:

            # Returns the package shipping time formated = {"package_id": package["id"],"expected_delivery": package_shipping_date.isoformat()}
            shipping = calculate_shipping(carries, package, data)
            
            # Adds to the list the shipping time calculated
            deliveries_list.append(shipping)

    deliveries["deliveries"] = deliveries_list
    return deliveries
    
if __name__ == "__main__":
    print(main())
    