try:
    diskette_code = int(input("Enter diskette code: "))

    if diskette_code == 1:
        print("3M Coporation")
    elif diskette_code == 2:
        print("Maxell Corporation")
    elif diskette_code == 3:
        print("Sony Corporation")
    elif diskette_code == 4:
        print("Verbatim Corporation")
    else:
        print("Diskette code not found")
except ValueError:
    print("Enter integers only")
