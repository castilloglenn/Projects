import random, getpass, os, time, sqlite3, ftplib


class UserInfo:
    def __init__(self, name, age, password, coins, user_type, coin_limit, initial_bet, reward):
        self.name = name
        self.age = age
        self.password = password
        self.coins = coins
        self.user_type = user_type
        self.coin_limit = coin_limit
        self.initial_bet = initial_bet
        self.reward = reward


#=======================================DATABASE=======================================
local_database = sqlite3.connect('lib.db')
local_cursor = local_database.cursor()
local_cursor.execute('CREATE TABLE IF NOT EXISTS Accounts (name TEXT, age INTEGER, password TEXT, coins INTEGER, user_type TEXT, coin_limit INTEGER)')
local_cursor.execute('CREATE TABLE IF NOT EXISTS Leaderboard (name TEXT, biggest_bid INTEGER, highest_coin INTEGER)')

local_cursor.execute("SELECT * FROM Accounts")
data = local_cursor.fetchall()
local_cursor.execute("SELECT * FROM Accounts WHERE name = 'Administrator'")
verify_data = local_cursor.fetchone()
if verify_data not in data:
    local_cursor.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)',
                         ('Administrator', 69420, 'Admin@123', 10000000, 'Game Master', 1000))
    local_database.commit()
else:
    pass


def register_data(user):
    local_cursor.execute('SELECT * FROM Accounts')
    data1 = local_cursor.fetchall()
    if (user.name, user.age, user.password, user.coins, user.user_type, user.coin_limit) not in data1:
        with local_database:
            local_cursor.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)',
                                 (user.name, user.age, user.password, user.coins, user.user_type, user.coin_limit))
            local_cursor.execute('INSERT INTO Leaderboard VALUES (?, ?, ?)', (user.name, 0, 0))
    else:
        print('User already exists.')


def get_data(name, password):
    local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{name}'")
    data2 = local_cursor.fetchone()
    if data2 is None:
        print(f"\n           User {name} does not exist. (Username is case-sensitive)")
        time.sleep(1.5)
    elif name == data2[0]:
        if password == data2[2]:
            return data2
        else:
            print('\n                      Incorrect password')
            time.sleep(1)


def check_data(name):
    local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{name}'")
    data3 = local_cursor.fetchone()
    if data3 is None:
        return True
    else:
        return False


def save_data(user):
    local_cursor.execute('UPDATE Accounts SET coins = ?, coin_limit = ? WHERE name = ?', (user.coins, user.coin_limit, user.name))
    local_database.commit()


def high_bid_update(user):
    local_cursor.execute(f"SELECT * FROM Leaderboard WHERE name = '{user.name}'")
    user_in_database = local_cursor.fetchone()
    if user.initial_bet > user_in_database[1]:
        local_cursor.execute("UPDATE Leaderboard SET biggest_bid = ? WHERE name = ?", (user.initial_bet, user.name))
        local_database.commit()


def high_coin_update(user):
    local_cursor.execute(f"SELECT * FROM Leaderboard WHERE name = '{user.name}'")
    coin_in_database = local_cursor.fetchone()
    if user.coins > coin_in_database[2]:
        local_cursor.execute("UPDATE Leaderboard SET highest_coin = ? WHERE name = ?", (user.coins, user.name))
        local_database.commit()


#=========================================FTP========================================
def loading_screen():
    os.system('cls')
    print('''




                                  ♠
                          ♥      ♣=♥      ♦
                                ♦=♠=♣
                       #=======♥=♦=♣=♠=======#
                       ||   L O A D I N G   ||
                       ||   (Do not close)  ||
                       #=======♠=♣=♦=♥=======#
                                ♦=♠=♣
                          ♣      ♣=♠      ♠
                                  ♥''')


def ftp_reconnecting():
    os.system('cls')
    print('''




                                  ♠
                          ♥      ♣=♥      ♦
                                ♦=♠=♣
                       #=======♥=♦=♣=♠=======#
                       || CONNECTION ERROR: ||
                       ||  Reconnecting...  ||
                       #=======♠=♣=♦=♥=======#
                                ♦=♠=♣
                          ♣      ♣=♠      ♠
                                  ♥''')
    time.sleep(2)


def error_last():
    os.system('cls')
    print('''




                                  ♠
                          ♥      ♣=♥      ♦
                                ♦=♠=♣
                       #=======♥=♦=♣=♠=======#
                       ||    DATABASE IS    ||
                       ||    NOT UPDATED    ||
                       #=======♠=♣=♦=♥=======#
                                ♦=♠=♣
                          ♣      ♣=♠      ♠
                                  ♥''')
    time.sleep(1)


def download_global():
    file_name = 'global.db'
    if os.path.exists(file_name):
        os.remove(file_name)
        add_logs("File 'global.db' has been removed in directory")
    elif not os.path.exists(file_name):
        pass

    counter = 0
    while 1:
        try:
            if counter == 3:
                error_last()
                return False
            else:
                add_logs('Connecting to FTP server')
                ftp = ftplib.FTP('')
                ftp.connect('files.000webhost.com', port=21)
                ftp.login(user='rejuvenize', passwd='glenncastillo')
                ftp.cwd('server')
                add_logs('Connected to FTP server')
                add_logs('Downloading global.db')
                write_2local = open(file_name, 'wb')
                ftp.retrbinary("RETR " + file_name, write_2local.write, 1024)
                add_logs("File 'global.db' downloaded")
                write_2local.close()
                ftp.close()
                return True
        except ftplib.all_errors as msg:
            ftp_reconnecting()
            add_logs(f'Error while downloading global.lib:\n         {msg}')
            counter += 1


def upload_global():
    counter = 0
    while 1:
        try:
            if counter == 3:
                error_last()
                return False
            else:
                file_name = 'global.db'
                add_logs('Connecting to FTP server')
                ftp = ftplib.FTP('')
                ftp.connect('files.000webhost.com', port=21)
                ftp.login(user='rejuvenize', passwd='glenncastillo')
                ftp.cwd('server')
                add_logs('Connected to FTP server')
                ftp.delete('global.db')
                add_logs("Server's 'global.db' deleted")
                ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
                add_logs("File 'global.db' uploaded")
                ftp.close()
                return True
        except ftplib.all_errors as msg:
            ftp_reconnecting()
            add_logs(f'Error while uploading global.lib:\n         {msg}')
            counter += 1


def transfer_data(sender, receiver, location):
    receiver_lib = sqlite3.connect(receiver)
    receiver_cursor = receiver_lib.cursor()
    sender_lib = sqlite3.connect(sender)
    sender_cursor = sender_lib.cursor()

    sender_cursor.execute('SELECT * FROM Accounts')
    sender_data = sender_cursor.fetchall()
    receiver_cursor.execute('SELECT * FROM Accounts')
    receiver_data = receiver_cursor.fetchall()

    for data_row in sender_data:
        account_list = []
        for s_row in receiver_data:
            account_list.append(s_row[0])

        if data_row[0] in account_list:
            receiver_cursor.execute(f"UPDATE Accounts SET coins = {data_row[3]}, user_type = '{data_row[4]}', coin_limit = {data_row[5]} WHERE name = '{data_row[0]}' and password = '{data_row[2]}'")
            receiver_lib.commit()
            add_logs(f"[{location}] User {data_row[0]}'s account has been updated")
        else:
            receiver_cursor.execute("INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)", data_row)
            receiver_lib.commit()
            add_logs(f"[{location}] User {data_row[0]}'s account has been added")

    sender_cursor.execute('SELECT * FROM Leaderboard')
    send = sender_cursor.fetchall()
    receiver_cursor.execute('SELECT * FROM Leaderboard')
    receive = receiver_cursor.fetchall()

    for data_row in send:
        lead_list = []
        for s_row in receive:
            lead_list.append(s_row[0])

        if data_row[0] in lead_list:
            receiver_cursor.execute(f"UPDATE Leaderboard SET biggest_bid = {data_row[1]}, highest_coin = {data_row[2]} WHERE name = '{data_row[0]}'")
            receiver_lib.commit()
            add_logs(f"[{location}] User {data_row[0]}'s leaderboard account has been updated")
        else:
            receiver_cursor.execute("INSERT INTO Leaderboard VALUES (?, ?, ?)", data_row)
            receiver_lib.commit()
            add_logs(f"[{location}] User {data_row[0]}'s account has been updated")

    add_logs(f"{location} database has been updated")


def download_server_database():
    loading_screen()
    boole = download_global()
    transfer_data('global.db', 'lib.db', 'Local') if boole else error_last()


def upload_local_database():
    loading_screen()
    boole = download_global()
    if boole:
        transfer_data('lib.db', 'global.db', 'Server')
        upload_global()
    else:
        error_last()


#===================================LOGS=AND=ENCRYPTION===============================
alpha = ' CBADEFGHIJKP:,.j<>?abcONMLQRSTUVWXYZdefghi/kponmlqrs!1234567890@#$%^&*()-=_+|[]{};tuvwxyz'
bravo = 'zyxwvut;}{][|+_=-)(*&^%$#@0987654321!srqlmnopk/ihgfedZYXWVUTSRQLMNOcba?><j.,:PKJIHGFEDABC '
encrypt = str.maketrans(alpha, bravo)
decrypt = str.maketrans(bravo, alpha)


def add_logs(message):
    get_time = time.strftime("%m-%d-%y %H:%M:%S", time.localtime())
    add_log = open('logs.txt', 'a')
    add_log.write(f'{get_time} - {message}\n'.translate(encrypt))
    add_log.close()


#=======================================UTILITIES=====================================
def refresh_screen():
    os.system('cls')
    time.sleep(0.3)


def new_balance(coins):
    return f'           New Balance: {int(round(coins)):,} Coins'


def password_wrong(name):
    user_ans = input(f'           You have entered the wrong {name} key.\n           Would you like to try again? (Yes/No)\n    > ').lower()
    return True if user_ans == 'yes' or user_ans == 'y' else False


def password_validator(name, password):
    verification = getpass.getpass(prompt=f'\n       Enter the {name} key: ').lower()
    is_matched = True if verification == password else False
    return is_matched


def bet_receiver(user):
    quit1 = False
    bet_list = {'a': 10, 'b': 25, 'c': 50, 'd': 100, 'e': round(user.coins * 0.5), 'f': user.coins}
    multiplier = {1: 1.1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5}
    additional = {'e': '(+10%)', 'f': '(+25%)'}
    while 1:
        prompt = input('\n           To begin, choose your bet:\n           A. 10 Coins       E. Half of my coins! (+10% Bonus)\n'
                       '           B. 25 Coins       F. All IN! (+25% Bonus)\n           C. 50 Coins       G. Quit\n'
                       '           D. 100 Coins\n\n           > ').lower()
        if prompt == 'g':
            quit1 = True
            refresh_screen()
            break
        elif prompt in bet_list:
            if user.coins >= bet_list[prompt]:
                user.initial_bet = bet_list[prompt]
                break
            else:
                print('           You cannot bet higher than your current coins.')
        else:
            print('           Please enter the letter of desired amount only.')
    if not quit1:
        multiplier_value = multiplier[random.randint(1, 5)]
        if prompt == 'e':
            user.reward = int(round(user.initial_bet * 1.1 * multiplier_value))
        elif prompt == 'f':
            user.reward = int(round(user.initial_bet * 1.25 * multiplier_value))
        else:
            user.reward = int(round(user.initial_bet * multiplier_value))
        print(f'\n           [Initial bet]: {int(user.initial_bet):,} Coins')
        time.sleep(0.5)
        print(f'           [Bonus Multiplier]: {multiplier_value}X')
        time.sleep(0.5)
        print(f"           [Total Reward]: {user.reward:,} Coins {additional[prompt] if prompt in additional else ''}")
        time.sleep(1.5)
        high_bid_update(user)
        add_logs(f'{user.name} Bet: {user.initial_bet:,} {multiplier_value}X = {user.reward:,}')
    return user, quit1


# =====================================ADD=COINS====================================
def add_coins_banner():
    print('    ==============================[ADD=COINS]=============================')


def add_coins(user):
    coins_list = {'a': 50, 'b': 100, 'c': 250, 'd': 500, 'z': 1000}
    verify_key = {'a': 'alpha', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'z': 'bonus'}
    master_key = 'castillo'
    while 1:
        display_status(user)
        add_coins_banner()
        prompt = input('\n           A. ADD COINS\n           B. ENTER COUPON CODE\n           C. BACK\n    > ').lower()
        if prompt == 'a':
            while 2:
                if user.coin_limit < 1:
                    print('           You have already reached your add-coins limit.')
                    break
                elif user.coin_limit >= 1:
                    display_status(user)
                    add_coins_banner()
                    verification = password_validator('master', master_key)
                    if verification:
                        print(f'\n           Successful!')
                        time.sleep(0.5)
                        refresh_screen()
                        while 3:
                            display_status(user)
                            add_coins_banner()
                            addition = input('\n           Now enter how many coins would you like to add:\n           A. 50 Coins\n'
                                             '           B. 100 Coins\n           C. 250 Coins\n           D. 500 Coins\n'
                                             '           > ').lower()
                            if addition in coins_list:
                                verify = getpass.getpass(prompt='           Enter verification key: ').lower()
                                if verify == verify_key[addition]:
                                    print('           Successful!')
                                    time.sleep(0.5)
                                    if user.user_type == 'Normal User':
                                        user.coins += coins_list[addition]
                                        print(f'           Your new coin balance is {user.coins}.\n')
                                        user.coin_limit -= 1
                                        save_data(user)
                                        add_logs(f'{user.name} added {coins_list[addition]} with {user.user_type}')
                                        time.sleep(2)
                                        break
                                    elif user.user_type == 'Premium User':
                                        user.coins += int(coins_list[addition] * 1.5)
                                        print(f'           Your new coin balance is {user.coins} (+50% Premium Bonus).\n')
                                        user.coin_limit -= 1
                                        save_data(user)
                                        add_logs(f'{user.name} added {coins_list[addition]} with {user.user_type}')
                                        time.sleep(2)
                                        break
                                else:
                                    prompt = password_wrong('master')
                                    if prompt:
                                        continue
                                    else:
                                        break
                            else:
                                print('           Please enter the letter of desired value only.')
                        break
                    else:
                        prompt = password_wrong('master')
                        if prompt:
                            continue
                        else:
                            break
        elif prompt == 'b':
            display_status(user)
            print('    =============================[COUPON=CODE]============================')
            coupons = {'bsit1d':10000, 'cvsuimus':20000, 'glenncastillo':30000, 'meandtheboys':50000}
            coupon_code = input('\n           Enter the coupon code:\n    > ').lower()
            if coupon_code in coupons:
                user.coins += coupons[coupon_code]
                time.sleep(1)
                print('           Congratulations!')
                print(f"\n           {coupons[coupon_code]:,} has been added to your account.")
                add_logs(f'           {user.name} redeemed coupon using {coupon_code}, {user.coins}')
                time.sleep(2)
                break
            else:
                prompt = password_wrong('coupon code')
                if prompt:
                    continue
                else:
                    break
        elif prompt == 'c':
            break
        else:
            print("           Enter 'Yes' or 'No' only.")
    print(f'           Coin Balance: {user.coins}')
    refresh_screen()
    return user


# ====================================GAME=LIST========================================
# ====================================DICE=HI=LO=======================================
def dice_hi_lo_display(user, has_bonus, bonus):
    print(f'\n           [DICE HI-LO]\n           Welcome {user.name}, Account Balance: {int(user.coins):,} Coins\n')
    if has_bonus:
        print(f'           Total Reward: {int(user.reward):,} Coins ({bonus} Bonus)')
    elif not has_bonus:
        print(f'           Total Reward: {user.reward:,} Coins')


def dice_hi_lo_win(user, bonus, choice):
    user.coins += round(user.reward * bonus[choice])
    print('           Congratulations!')
    print(f'{new_balance(user.coins)}')
    high_coin_update(user)
    add_logs(f'{user.name} Won Dice Hi-Lo with {user.reward * bonus[choice]:,} Coins, {user.coins:,} Balance')
    return user


def dice_hi_lo_lost(user):
    high_bid_update(user)
    user.coins -= user.initial_bet
    print('           You LOST!')
    print(f'{new_balance(user.coins)}')
    add_logs(f'{user.name} Lost Dice Hi-Lo with {user.initial_bet:,} Coins, {user.coins:,} Balance')
    return user


def dice_hi_lo(user):
    while 1:
        if user.coins <= 0:
            break
        else:
            refresh_screen()
            computer_dices = {1: random.randint(1, 6), 2: random.randint(1, 6),
                              3: random.randint(1, 6), 4: random.randint(1, 6)}
            player_dices = {1: random.randint(1, 6), 2: random.randint(1, 6),
                            3: random.randint(1, 6), 4: random.randint(1, 6)}
            dice_bonus = {'a': 1.0, 'b': 1.1, 'c': 1.25, 'd': 1.5}
            dice_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
            bonus_visual = {'b': '+10%', 'c': '+25%', 'd': '+50%'}
            computer_total, player_total, user.initial_bet, user.reward = 0, 0, 0, 0
            dice_hi_lo_display(user, False, 0)
            user, prompt = bet_receiver(user)
            if not prompt:
                os.system('cls')
                dice_hi_lo_display(user, False, 0)
                user_choice = input('\n           How many dices would you like to play?\n'
                                    '           A. 1 Die (No Bonus)\n'
                                    '           B. 2 Dice (10% Bonus)\n'
                                    '           C. 3 Dice (25% Bonus)\n'
                                    '           D. 4 Dice (50% Bonus)\n'
                                    '           E. Quit\n\n'
                                    '           > ').lower()
                if user_choice == 'e':
                    os.system('cls')
                    break
                elif user_choice in dice_dict:
                    user.reward = int(user.reward * dice_bonus[user_choice])
                    while 2:
                        validator = ['hi', 'high', 'lo', 'low']
                        os.system('cls')
                        dice_hi_lo_display(user, True if user_choice in bonus_visual else False,
                                           bonus_visual[user_choice] if user_choice in bonus_visual else 0)
                        hi_lo = input('\n           Do you think you will have the higher value or lower value?\n\n'
                                      '           (High/Low): ').lower()
                        if hi_lo in validator:
                            os.system('cls')
                            dice_hi_lo_display(user, True if user_choice in bonus_visual else False,
                                               bonus_visual[user_choice] if user_choice in bonus_visual else 0)
                            print(f'\n                    Computer         {user.name}')
                            for value in range(1, dice_dict[user_choice] + 1):
                                time.sleep(1.5)
                                print(
                                    f'                   Dice {value}: {computer_dices[value]}!      Dice {value}: {player_dices[value]}!')
                                computer_total += computer_dices[value]
                                player_total += player_dices[value]
                            time.sleep(1.5)
                            print(f'\n                   Computer: {computer_total}    {user.name}: {player_total}')
                            time.sleep(1)
                            print(f'\n           Your bet: {hi_lo.upper()}')
                            if hi_lo == 'high' or hi_lo == 'hi':
                                if player_total > computer_total:
                                    dice_hi_lo_win(user, dice_bonus, user_choice)
                                elif player_total < computer_total:
                                    dice_hi_lo_lost(user)
                                elif player_total == computer_total:
                                    print("           It's a tie!")
                            elif hi_lo == 'low' or hi_lo == 'lo':
                                if player_total < computer_total:
                                    dice_hi_lo_win(user, dice_bonus, user_choice)
                                elif player_total > computer_total:
                                    dice_hi_lo_lost(user)
                                elif player_total == computer_total:
                                    print("           It's a tie!")
                            save_data(user)
                            break
                        else:
                            print("           Please enter 'High' or 'Low' only.")
                else:
                    print('           Please enter the letter of your choice.')
            elif prompt:
                break
        prompt = input('           Would you like to try again? (Yes/No): ').lower()
        if prompt == 'yes' or prompt == 'y':
            continue
        elif prompt == 'no' or prompt == 'n':
            os.system('cls')
            break
        else:
            print("           Enter 'Yes' or 'No' only.")
            time.sleep(0.5)
    return user


# ===================================GUESS=THE=NUMBER===================================
def guess_the_number_display(user, secret_number, is_shown, start, end):
    print(f'\n           [GUESS THE NUMBER!]\n           Welcome {user.name}, Account Balance: {int(user.coins):,} Coins\n')
    if not is_shown:
        print(f'           Total Reward: {int(user.reward):,} Coins')
        print(f'           SECRET NUMBER: {secret_number}'.replace(str(secret_number), '##'))
        print(f'           The number ranges from {start} to {end}.')
    elif is_shown:
        print(f'           Total Reward: {int(user.reward):,} Coins')
        print(f'           SECRET NUMBER: {secret_number}')


def guess_the_number(user):
    while 1:
        if user.coins <= 0:
            break
        else:
            user.initial_bet, user.reward = 0, 0
            while 1:
                start_value = random.randint(1, 100)
                end_value = random.randint(1, 100)
                if end_value > start_value and end_value - start_value == 40:
                    break
            secret_number = random.randint(start_value, end_value)
            guess_limit = 5
            refresh_screen()
            guess_the_number_display(user, secret_number, False, start_value, end_value)
            user, prompt = bet_receiver(user)
            if not prompt:
                while guess_limit >= 0:
                    if guess_limit == 0:
                        os.system('cls')
                        guess_the_number_display(user, secret_number, True, start_value, end_value)
                        print('\n           You ran out of guesses, YOU LOST!')
                        user.coins -= user.initial_bet
                        print(f'{new_balance(user.coins)}')
                        save_data(user)
                        add_logs(f'           {user.name} Lost Guess The Number with {user.initial_bet:,} Coins, {user.coins:,} Balance')
                        break
                    else:
                        os.system('cls')
                        guess_the_number_display(user, secret_number, False, start_value, end_value)
                        print(f'           Number of tries: {guess_limit} guess left.')
                        try:
                            user_guess = int(input('\n           Enter your guess: '))
                            if user_guess != secret_number and guess_limit != 0:
                                if start_value <= user_guess <= end_value:
                                    if secret_number < user_guess:
                                        print('           Computer says: Lower!')
                                        guess_limit -= 1
                                        time.sleep(1)
                                    elif secret_number > user_guess:
                                        print('           Computer says: Higher!')
                                        guess_limit -= 1
                                        time.sleep(1)
                                else:
                                    print(f'           Enter an integer from {start_value} to {end_value} only.')
                                    time.sleep(2)
                            elif user_guess == secret_number:
                                os.system('cls')
                                guess_the_number_display(user, secret_number, True, start_value, end_value)
                                print('\n\n           Congratulations!')
                                user.coins += user.reward
                                print(f'{new_balance(user.coins)}')
                                high_coin_update(user)
                                save_data(user)
                                add_logs(f'{user.name}, Won Guess The Number with {user.reward:,}, {user.coins:,} Balance')
                                break
                        except ValueError:
                            print('           Please enter a valid integer.')
                            time.sleep(1)
                prompt = input('           Would you like to try again? (Yes/No): ').lower()
                if prompt == 'yes' or prompt == 'y':
                    continue
                elif prompt == 'no' or prompt == 'n':
                    os.system('cls')
                    break
                else:
                    print("           Enter 'Yes' or 'No' only.")
            elif prompt:
                break
    return user


# ======================================LAST=SECTION=========================================
def initial_menu(user):
    while True:
        if user.coins <= 0 and user.coin_limit <= 0:
            print('\n\n You do not have enough coins to play. Please contact developer to buy more coins.')
            time.sleep(5)
            break
        else:
            display_status(user)
            game_choice = input('    ==============================[MAIN=MENU]=============================\n\n'
                                '        Choose a game:\n'
                                '        A. Guess The Number      D. (unavailable)\n'
                                '        B. Dice (Hi-Lo)          E. Add Coins/Enter Coupon\n'
                                '        C. (unavailable)         F. Log out/Save Data\n\n'
                                '        > ').lower()
            if game_choice == 'a':
                guess_the_number(user)
            elif game_choice == 'b':
                dice_hi_lo(user)
            elif game_choice == 'c':
                pass
            elif game_choice == 'd':
                pass
            elif game_choice == 'e':
                if user.coin_limit >= 1:
                    add_coins(user)
                elif user.coin_limit < 1:
                    print('    You have already reached your add-coins limit.')
                    time.sleep(1)
            elif game_choice == 'f':
                last_prompt = input('    Are you sure? (Your data will be saved.)\n'
                                    '    (Yes/No): ').lower()
                if last_prompt == 'yes' or last_prompt == 'y':
                    save_data(user)
                    print('\n    Returning to log-in screen...')
                    time.sleep(1)
                    add_logs(f"{user.name} has logged out")
                    add_logs(f"Uploading files to update the server's database")
                    upload_local_database()
                    break
                else:
                    os.system('cls')
            else:
                print('    Enter the letter of desired option only.')
                time.sleep(1.5)
                refresh_screen()


# ==========================================HI=SCORE=UI================================================
def high_score_banner():
    os.system('cls')
    print("""
    
               #==========================================#
               ||        Welcome to CASINO GAMES         ||
               ||  This game was made by Glenn Castillo  ||
               #==========================================#""")


def high_score_ui():
    while 1:
        high_score_banner()
        print('\n               ================[LEADERBOARD]===============')
        print('                                Top Players')
        local_cursor.execute("SELECT name, coins FROM Accounts WHERE name != 'Administrator' AND coins != 0 ORDER BY coins DESC")
        high_score_data = local_cursor.fetchall()
        if not high_score_data:
            print(f'                                No Data')
        else:
            for i in range(len(high_score_data) if len(high_score_data) <= 5 else 5):
                print(f'                         {i + 1}. {high_score_data[i][1]:,} - {high_score_data[i][0]}')
        print('\n                          Highest Coins Achieved')
        local_cursor.execute("SELECT name, highest_coin FROM Leaderboard WHERE name != 'Administrator' ORDER BY highest_coin DESC")
        highest_coins_data = local_cursor.fetchall()
        if not highest_coins_data:
            print(f'                                No Data')
        else:
            for i in range(len(highest_coins_data) if len(highest_coins_data) <= 5 else 5):
                print(f'                         {i + 1}. {highest_coins_data[i][1]:,} - {highest_coins_data[i][0]}')
        print('\n                             Highest Bidders')
        local_cursor.execute("SELECT name, biggest_bid FROM Leaderboard where name != 'Administrator' ORDER BY biggest_bid DESC")
        biggest_bid_data = local_cursor.fetchall()
        if not biggest_bid_data:
            print(f'                                No Data')
        else:
            for i in range(len(biggest_bid_data) if len(biggest_bid_data) <= 5 else 5):
                print(f'                         {i + 1}. {biggest_bid_data[i][1]:,} - {biggest_bid_data[i][0]}')
        print('\n                            Bankrupt Players')
        local_cursor.execute("SELECT name, coins FROM Accounts WHERE name != 'Administrator' AND coins = 0 AND coin_limit = 0")
        bankrupt_data = local_cursor.fetchall()
        if not bankrupt_data:
            print(f'                                No Data')
        else:
            for i in range(len(bankrupt_data) if len(bankrupt_data) <= 5 else 5):
                print(f'                         {i + 1}. {bankrupt_data[i][0]}')
        print("               ============================================")
        prompt = input('                         Return to main page?\n                        >  ')
        if prompt == 'yes' or prompt == 'y':
            os.system('cls')
            break
        else:
            continue


# ======================================ADMINISTRATIVE=UI==============================================
def admin_banner():
    print(f"""    
    ===========================[ADMINISTRATOR]============================
    WARNING: This section is for the developer only. 
             Actions done here is IRREVOCABLE.\n\n""")


def admin_manage_accounts():
    while 1:
        refresh_screen()
        admin_banner()
        choice = input("    A. VIEW DATABASE\n    B. DELETE ACCOUNT\n    C. BACK\n\n    > ").lower()
        if choice == 'a':
            while 2:
                os.system('cls')
                admin_banner()
                local_cursor.execute("SELECT * FROM Accounts WHERE name != 'Administrator'")
                list_account = local_cursor.fetchall()
                print('    ORDERED BY\n    1.Name  2.Age  3.Password  4.Coins  5.User Type  6.Coin Limit'
                      '\n========================================================================')
                counter = 1
                for acc in list_account:
                    print(f'  {counter}. {acc[0]}  |  {acc[1]}  |  {acc[2]}  |  {acc[3]:,}  |  {acc[4]}  |  {acc[5]} ')
                    counter += 1
                choice1 = input(
                    '========================================================================\nReturn? ').lower()
                if choice1 == 'y' or choice1 == 'yes':
                    add_logs('Administrator checked the database files')
                    break
                else:
                    continue
        elif choice == 'b':
            while 2:
                os.system('cls')
                admin_banner()
                master_key = 'delete'
                input_name = input('    ENTER THE NAME: ')
                local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{input_name}'")
                del_data = local_cursor.fetchone()
                if del_data is None:
                    print(f'\n    USER {input_name} DOES NOT EXIST.')
                    prompt = input('    Would you like to try again?\n').lower()
                    if prompt == 'yes' or prompt == 'y':
                        continue
                    elif prompt == 'no' or prompt == 'n':
                        break
                    else:
                        print('    YES or NO only.')
                else:
                    while 3:
                        os.system('cls')
                        admin_banner()
                        last_chance = input('    ARE YOU SURE?\n    > ').lower()
                        if last_chance == 'y' or last_chance == 'yes':
                            validator = password_validator('deletion', master_key)
                            if validator:
                                print('Passwords matched!')
                                time.sleep(1)
                                print('Deleting User...')
                                local_cursor.execute(f"DELETE FROM Accounts WHERE name == '{input_name}'")
                                local_database.commit()
                                local_cursor.execute(f"DELETE FROM Leaderboard WHERE name == '{input_name}'")
                                local_database.commit()
                                time.sleep(1)
                                add_logs(f'Administrator deleted user {input_name}')
                                break
                            else:
                                prompt = input('\nPassword not matched.\nTry again?\n').lower()
                                if prompt == 'yes' or prompt == 'y':
                                    continue
                                elif prompt == 'no' or prompt == 'n':
                                    break
                                else:
                                    print('YES or NO only.')
                        elif last_chance == 'n' or last_chance == 'no':
                            break
                        else:
                            print('YES or NO only.')
        elif choice == 'c':
            break
        else:
            continue


def admin_add_coins():
    while 1:
        os.system('cls')
        admin_banner()
        master_key = 'add'
        input_name = input('    ENTER THE NAME: ')
        local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{input_name}'")
        add_coin_data = local_cursor.fetchone()
        if add_coin_data is None:
            print(f'\n    USER {input_name} DOES NOT EXIST.')
            prompt = input('    Would you like to try again?\n').lower()
            if prompt == 'yes' or prompt == 'y':
                continue
            elif prompt == 'no' or prompt == 'n':
                break
            else:
                print('YES or NO only.')
        else:
            while 2:
                os.system('cls')
                admin_banner()
                validator = password_validator('verifier', master_key)
                if validator:
                    coin_amount = int(input("    ENTER THE NUMBER OF COINS: "))
                    print(f"Adding {coin_amount} Coins to {input_name}...")
                    time.sleep(2)
                    local_cursor.execute(f"UPDATE Accounts SET coins = {coin_amount} WHERE name = '{input_name}'")
                    local_database.commit()
                    print('Added!')
                    time.sleep(1)
                    add_logs(f'Administrator added {coin_amount} Coins to {input_name}')
                    break
                else:
                    prompt = input('\n    Passwords not matched.\n    Try again?\n    ').lower()
                    if prompt == 'yes' or prompt == 'y':
                        continue
                    elif prompt == 'no' or prompt == 'n':
                        break
                    else:
                        print('YES or NO only.')


def admin_add_coin_limit():
    while 1:
        os.system('cls')
        admin_banner()
        master_key = 'change'
        input_name = input('    ENTER THE NAME: ')
        local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{input_name}'")
        add_coin_limit_data = local_cursor.fetchone()
        if add_coin_limit_data is None:
            print(f'\n    USER {input_name} DOES NOT EXIST.')
            prompt = input('    Would you like to try again?\n').lower()
            if prompt == 'yes' or prompt == 'y':
                continue
            elif prompt == 'no' or prompt == 'n':
                break
            else:
                print('YES or NO only.')
        else:
            while 2:
                os.system('cls')
                admin_banner()
                validator = password_validator('verifier', master_key)
                if validator:
                    coin_limit_amount = int(input("    ENTER NEW COIN LIMIT: "))
                    print(f"    Changing {input_name}'s coin limit to {coin_limit_amount}...")
                    time.sleep(2)
                    local_cursor.execute(f"UPDATE Accounts SET coin_limit = {coin_limit_amount} WHERE name = '{input_name}'")
                    local_database.commit()
                    print('    Changed!')
                    time.sleep(1)
                    add_logs(f"Administrator changed {input_name}'s coin-limit to {coin_limit_amount}")
                    break
                else:
                    prompt = input('\n    Password not matched.\n    Try again?\n    ').lower()
                    if prompt == 'yes' or prompt == 'y':
                        continue
                    elif prompt == 'no' or prompt == 'n':
                        break
                    else:
                        print('    YES or NO only.')


def admin_change_subscription():
    while 1:
        os.system('cls')
        admin_banner()
        master_key = 'change'
        input_name = input('    ENTER THE NAME: ')
        local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{input_name}'")
        change_sub_data = local_cursor.fetchone()
        if change_sub_data is None:
            print(f'\n    USER {input_name} DOES NOT EXIST.')
            prompt = input('    Would you like to try again?\n    ').lower()
            if prompt == 'yes' or prompt == 'y':
                continue
            elif prompt == 'no' or prompt == 'n':
                break
            else:
                print('    YES or NO only.')
        else:
            while 2:
                os.system('cls')
                admin_banner()
                validator = password_validator('verifier', master_key)
                if validator:
                    os.system('cls')
                    admin_banner()
                    local_cursor.execute(f"SELECT * FROM Accounts WHERE name = '{input_name}'")
                    new_data = local_cursor.fetchone()
                    print(f"    User {input_name} is a {new_data[4]}")
                    subs = {'a': 'Premium User', 'b': 'Normal User'}
                    new_subscription = input("    ENTER NEW SUBSCRIPTION:\n    A. Premium User\n    B. Normal User\n    > ").lower()
                    if new_subscription == 'a':
                        if new_data[4] == subs['a']:
                            print('    Subscription is same as current.')
                            time.sleep(2)
                        else:
                            print(f"    Changing {input_name}'s subscription to {subs[new_subscription]}...")
                            time.sleep(2)
                            local_cursor.execute(f"UPDATE Accounts SET user_type = '{subs[new_subscription]}' WHERE name = '{input_name}'")
                            local_database.commit()
                            print('    Changed!')
                            add_logs(f"Administrator changed {input_name}'s subscription to {subs[new_subscription]}")
                            time.sleep(1)
                            break
                    elif new_subscription == 'b':
                        if new_data[4] == subs['b']:
                            print('    Subscription is same as current.')
                            time.sleep(2)
                        else:
                            print(f"    Changing {input_name}'s subscription to {subs[new_subscription]}...")
                            time.sleep(2)
                            local_cursor.execute(f"UPDATE Accounts SET user_type = '{subs[new_subscription]}' WHERE name = '{input_name}'")
                            local_database.commit()
                            print('    Changed!')
                            add_logs(f"Administrator changed {input_name}'s subscription to {subs[new_subscription]}")
                            time.sleep(1)
                            break
                else:
                    prompt = input('\n    Password not matched.\n    Try again?\n    ').lower()
                    if prompt == 'yes' or prompt == 'y':
                        continue
                    elif prompt == 'no' or prompt == 'n':
                        break
                    else:
                        print('    YES or NO only.')


def admin_view_logs():
    while 1:
        os.system('cls')
        admin_banner()
        print('=============================[USER=LOGS]==============================')
        open_file = open('logs.txt', 'r+')
        log_file = open_file.read()
        print(log_file.translate(decrypt))
        print('======================================================================')
        prompt = input('    Exit or Clear Logs? ').lower()
        if prompt == 'exit' or prompt == 'y' or prompt == 'yes':
            open_file.close()
            add_logs(f"Administrator has viewed the logs")
            break
        elif prompt == 'clear logs' or prompt == 'clear log' or prompt == 'clear':
            file = open('logs.txt', 'w')
            file.close()
            add_logs('Administrator has cleared the logs')
            continue
        else:
            print('    Refreshing')
            refresh_screen()


def admin_manage_database():
    while 1:
        refresh_screen()
        admin_banner()
        choice = input("    A. BACKUP DATABASE\n    B. UPDATE DATABASE\n    C. DELETE DATABASE\n    D. BACK\n\n    > ").lower()
        if choice == 'a':
            refresh_screen()
            admin_banner()
            prompt = input('    ARE YOU SURE YOU WANT TO BACKUP THE DATABASE FILE?\n    > ').lower()
            if prompt == 'yes' or prompt == 'y':
                backup_file = sqlite3.connect('lib_backup.db')
                local_database.backup(backup_file)
                print('\n    DATABASE HAS BEEN BACKUP TO FILE NAME "lib_backup.db" OF THE SAME DIRECTORY.')
                time.sleep(2)
                print('Returning...')
                time.sleep(1)
                add_logs('Administrator backup the database')
                backup_file.close()
                break
            else:
                print('NO ACTIONS HAS BEEN TAKEN')
                time.sleep(1)
        elif choice == 'b':
            refresh_screen()
            admin_banner()
            prompt = input('ARE YOU SURE YOU WANT TO UPDATE THE DATABASE FILE FROM BACKUP?\n'
                           '(FILE lib_backup.db MUST BE ON THE SAME DIRECTORY)\n'
                           '> ').lower()
            if prompt == 'yes' or prompt == 'y':
                transfer_data('lib_backup.db', 'lib.db', 'Backup')
                time.sleep(2)
                print('\n    THE DATABASE HAS BEEN UPDATED.')
                time.sleep(1)
                print('    Returning...')
                time.sleep(1)
                add_logs('Administrator has updated the database')
                break
            else:
                print('    NO ACTIONS HAS BEEN TAKEN')
                time.sleep(1)
        elif choice == 'c':
            refresh_screen()
            admin_banner()
            prompt = input('    ARE YOU SURE YOU WANT TO DELETE THE DATABASE?\n    (REQUIRES RESTART OF THE GAME)\n    > ').lower()
            if prompt == 'yes' or prompt == 'y':
                add_logs('Administrator tries to delete the database...')
                another_prompt = input('\n    FINAL DECISION?\n    > ').lower()
                if another_prompt == 'yes' or 'y':
                    a = 'delete'
                    b = 'the'
                    d = 'database'
                    first_pass = getpass.getpass(prompt='    Enter the first deletion key: ').lower()
                    if first_pass == a:
                        second_pass = getpass.getpass(prompt='    Enter the second deletion key: ').lower()
                        if second_pass == b:
                            third_pass = getpass.getpass(prompt='    Enter the third deletion key: ').lower()
                            if third_pass == d:
                                local_cursor.execute('DELETE FROM Accounts')
                                local_database.commit()
                                local_cursor.execute('DELETE FROM Leaderboard')
                                local_database.commit()
                                print('    The database has been wiped out of existence.')
                                add_logs('Administrator has DELETED the DATABASE')
                                time.sleep(2)
                                break
            else:
                print('    NO ACTIONS HAS BEEN TAKEN')
                time.sleep(1)
        elif choice == 'd':
            break
        else:
            print('    CHOOSE THE LETTER WISELY.')
            time.sleep(1.5)



def admin_ui(user):
    while True:
        display_status(user)
        game_choice = input("""
    ==============================[ADMIN=UI]==============================

        1. Manage Accounts       4. Change Subscription
        2. Add Coins             5. View Logs
        3. Add Coin-Limit        6. Manage Database

    ======================================================================
        F. Log out
        > """).lower()
        if game_choice == 'f':
            last_prompt = input('\n    Are you sure? (Your data will be saved.)\n'
                                '    (Yes/No): ').lower()
            if last_prompt == 'yes' or last_prompt == 'y':
                print('\n    Returning to log-in screen...')
                time.sleep(1)
                save_data(user)
                add_logs('Administrator has logged out')
                upload_local_database()
                break
            else:
                os.system('cls')
        elif game_choice == '1':
            admin_manage_accounts()
        elif game_choice == '2':
            admin_add_coins()
        elif game_choice == '3':
            admin_add_coin_limit()
        elif game_choice == '4':
            admin_change_subscription()
        elif game_choice == '5':
            admin_view_logs()
        elif game_choice == '6':
            admin_manage_database()
        else:
            print('\n        Enter the letter of desired option only.')
            time.sleep(1.5)
            refresh_screen()


# =======================================LOG=IN=INTERFACE===============================================
def display_status(user):
    os.system('cls')
    print(f"""
    ===============================[STATUS]===============================
        Username: {user.name}
        Age: {user.age}
        Subscription: {user.user_type}
        Coins: {int(user.coins):,}
        Number of times to buy coins: {user.coin_limit}
        Password: {'*' * len(user.password)}""")


def registration_banner():
    print('    ============================[REGISTRATION]============================')


def reg_status(name, age, coins, user_type, coin_limit, password):
    os.system('cls')
    print(f"""
    ===============================[STATUS]===============================
        Username: {name}
        Age: {age}
        Subscription: {user_type}
        Coins: {'' if isinstance(coins, str) else int(round(coins))}
        Number of times to buy coins: {coin_limit}
        Password: {'*' * len(password)}""")


def get_name():
    while 1:
        reg_status('', '', '', '', '', '')
        registration_banner()
        name = input('\n    The username must be 3 to 10 alphanumeric characters and no spaces.\n'
                     '    Enter your username: ')
        if 3 <= len(name) <= 10 and ' ' not in name:
            verifier = check_data(name)
            if verifier:
                return name
            if not verifier:
                print('Username already exists.')
                time.sleep(1)
        else:
            continue


def get_age(name):
    while 1:
        reg_status(name, '', '', '', '', '')
        registration_banner()
        print('\n    Your age must be 18 or above to play gambling games.')
        try:
            age = int(input('    Enter your age: '))
            if age < 18:
                print('    You are not allowed to play gambling games.\nProgram will exit...')
                time.sleep(3)
                quit()
            elif 18 <= age <= 100:
                return age
            elif age > 100:
                print('    You seem too impossible to be alive.')
                time.sleep(1.5)
            else:
                print('    Please enter a valid age value.')
                time.sleep(1.5)
        except ValueError:
            print('    Please enter a valid age value.')
            time.sleep(1.5)


def get_user_type(name, age):
    while 1:
        subscription_list = {'a': 'Premium User', 'b': 'Normal User'}
        reg_status(name, age, '', '', '', '')
        registration_banner()
        prompt = input('\n    Enter your subscription type:\n'
                       '    A. Premium User (Requires subscription key)\n'
                       '    B. Normal User (Does not require subscription key)\n\n'
                       '    (Letter only.)\n\n'
                       '    > ').lower()
        if prompt == 'a':
            subscription_key = 'glenn'
            while 2:
                reg_status(name, age, '', '', '', '')
                registration_banner()
                verification = password_validator('subscription', subscription_key)
                if verification:
                    print('       Successful!')
                    time.sleep(1)
                    return subscription_list['a'], 500, 3
                elif not verification:
                    while 3:
                        reg_status(name, age, '', '', '', '')
                        registration_banner()
                        prompt2 = input('    You have entered the wrong subscription key. Would you like to try again?\n'
                                        '    (Yes/No):\n'
                                        '    > ')
                        if prompt2 == 'yes' or prompt2 == 'y':
                            break
                        elif prompt2 == 'no' or prompt2 == 'n':
                            return subscription_list['b'], 200, 1
                        else:
                            print("    Enter 'YES' or 'NO' only.")
        elif prompt == 'b':
            return subscription_list['b'], 200, 1
        else:
            print("    Enter 'A' or 'B' only.")


def get_pass(name, age, coins, user_type, coin_limit):
    while 1:
        reg_status(name, age, coins, user_type, coin_limit, '')
        registration_banner()
        password = getpass.getpass(
            prompt='\n    The password must be 3 to 10 alphanumeric characters and no spaces.\n'
                   '    Enter your password: ')
        if 3 <= len(password) <= 10 and ' ' not in password:
            while 2:
                reg_status(name, age, coins, user_type, coin_limit, '')
                registration_banner()
                verify = getpass.getpass(prompt='\n    Verify your password: ')
                if password == verify:
                    print('    Password matched!')
                    time.sleep(1)
                    print('    Returning to log-in screen...')
                    time.sleep(1)
                    return password
                else:
                    prompt = input('    Verification does not matched your password, would you like to try again? (Yes/No): ').lower()
                    if prompt == 'yes' or prompt == 'y':
                        continue
                    elif prompt == 'no' or prompt == 'n':
                        break
        else:
            continue


def registration_menu():
    name = get_name()
    age = get_age(name)
    user_type, coins, coin_limit = get_user_type(name, age)
    password = get_pass(name, age, coins, user_type, coin_limit)
    user = UserInfo(name, age, password, coins, user_type, coin_limit, 0, 0)
    register_data(user)
    high_coin_update(user)
    add_logs(f'User {user.name} ({user.user_type}) has registered into database')
    add_logs(f"Sending {user.name} to server's database")
    upload_local_database()


def login():
    while 1:
        os.system('cls')
        name = input(f"""
           
               #==========================================#
               ||           Welcome to CASINO            ||
               ||  This game was made by Glenn Castillo  ||
               #==========================================#
                    "Type 'Back' or 'Quit' to return"
                  
                    ============[LOG=IN]=============
                     Username: """)
        if name == 'back' or name == 'quit' or name == 'b' or name == 'q':
            return name
        else:
            password = getpass.getpass('                     Password: ')
            user_data = get_data(name, password)
            if user_data is None:
                continue
            else:
                user = UserInfo(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], 0, 0)
                return user


def initial_screen():
    while 1:
        add_logs('Game has launched')
        os.system('cls')
        prompt = input("""
           
               #==========================================#
               ||           Welcome to CASINO            ||
               ||  This game was made by Glenn Castillo  ||
               #==========================================#
    
    
                        Do you have an account?
                           Yes - User Login
                           No - Registration
                        ------------------------
                        M - Multiplayer Battle
                        C - Check Leaderboard
                        Quit - Exit App
    
    
                            > """).lower()
        if prompt == 'yes' or prompt == 'y':
            user = login()
            if user == 'back' or user == 'quit' or user == 'b' or user == 'q':
                continue
            else:
                if user.name == 'Administrator':
                    add_logs('Administrator logged in')
                    admin_ui(user)
                else:
                    add_logs(f"{user.name} has logged in")
                    initial_menu(user)
        elif prompt == 'no' or prompt == 'n':
            registration_menu()
        elif prompt == 'm' or prompt == 'multiplayer':
            pass
        elif prompt == 'c' or prompt == 'check':
            high_score_ui()
        elif prompt == 'q' or prompt == 'quit':
            print('\n               Thank you for using this app. Goodbye!')
            time.sleep(1)
            local_cursor.close()
            local_database.close()
            add_logs('User has exit the game')
            quit()
        else:
            continue


download_server_database()
initial_screen()
