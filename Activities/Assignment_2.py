try:
    studname = input("Enter Student Name: ")
    korscode = input("Course Code: ").lower()
    yercode = int(input("Year Code: "))
    totallec = int(input("Total number of Lecture units enrolled: "))
    totallab = int(input("Total number of Laboratory units enrolled: "))
    korsname, lecrate, labrate, down = '', 0, 0, 0

    if korscode == 'a':
        korsname = "Engineering"
    elif korscode == 'b':
        korsname = "Business Administration"
    elif korscode == 'c':
        korsname = "Secretarial"
    elif korscode == 'd':
        korsname = "Architecture"
    else:
        print("Course name not found")

    if yercode == 1:
        lecrate, labrate = 345.75, 420.45
    elif yercode == 2:
        lecrate, labrate = 320.45, 400.50
    elif yercode == 3:
        lecrate, labrate = 298.75, 389.75
    elif yercode == 4 or yercode == 5:
        lecrate, labrate = 275.85, 360.65
    else:
        print("Year code not found")

    totalunits = totallec + totallab

    if 1 <= totalunits <= 8:
        down = 800
    elif 9 <= totalunits <= 14:
        down = 1000
    elif 15 <= totalunits <= 18:
        down = 1500
    elif totalunits >= 19:
        down = 1800

    lecfee = totallec * lecrate
    labfee = totallab * labrate
    tuition = lecfee + labfee
    balanse = tuition - down

    print(f"\nStudent Name: {studname}")
    print(f"Course Name: {korsname}")
    print(f"Tuition Fee: ₱{tuition:,.2f}")
    print(f"Balance: ₱{balanse:,.2f}")
except ValueError:
    print("Enter integers only")


