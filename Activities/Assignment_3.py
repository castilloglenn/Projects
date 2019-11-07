try:
    destination_code = int(input("Destination code: "))
    time_code = input("Time code: ").lower()
    day_code = input("Day code: ").lower()
    duration = int(input("Duration (in minutes): "))
    american_region, asian_region, african_region, european_region = 0, 0, 0, 0
    total_cost = 0

    if day_code == 'x':
        if time_code == 'a':
            american_region, asian_region, african_region, european_region = 50/3, 30/2, 40/3, 35/2
            if destination_code == 1:
                total_cost = american_region * duration
            elif destination_code == 2:
                total_cost = asian_region * duration
            elif destination_code == 3:
                total_cost = african_region * duration
            elif destination_code == 4:
                total_cost = european_region * duration
        elif time_code == 'b':
            american_region, asian_region, african_region, european_region = 45/3, 27/2, 36/3, 30/2
            if destination_code == 1:
                total_cost = american_region * duration
            elif destination_code == 2:
                total_cost = asian_region * duration
            elif destination_code == 3:
                total_cost = african_region * duration
            elif destination_code == 4:
                total_cost = european_region * duration
    elif day_code == 'y':
        if time_code == 'a':
            american_region, asian_region, african_region, european_region = 40/3, 25/2, 35/3, 20/2
            if destination_code == 1:
                total_cost = american_region * duration
            elif destination_code == 2:
                total_cost = asian_region * duration
            elif destination_code == 3:
                total_cost = african_region * duration
            elif destination_code == 4:
                total_cost = european_region * duration
        elif time_code == 'b':
            american_region, asian_region, african_region, european_region = 38/3, 15/2, 22/3, 19/2
            if destination_code == 1:
                total_cost = american_region * duration
            elif destination_code == 2:
                total_cost = asian_region * duration
            elif destination_code == 3:
                total_cost = african_region * duration
            elif destination_code == 4:
                total_cost = european_region * duration

    if total_cost != 0:
        print(f"\nTotal cost: ₱{total_cost:,.2f}")
    else:
        print("\nInvalid input")
except ValueError:
    print("\nInvalid input")
