import random, getpass, os, time, sqlite3


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

    def initiate_name(self):
        print(f"Hello {self.name}.")


#======================================DATABASE======================================
conn = sqlite3.connect('lib.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Accounts (name TEXT, age INTEGER, password TEXT, coins INTEGER, user_type TEXT, coin_limit INTEGER)')

c.execute("SELECT * FROM Accounts")
data = c.fetchall()
c.execute("SELECT * FROM Accounts WHERE name = 'Administrator'")
verify_data = c.fetchone()
if verify_data not in data:
    c.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)', ('Administrator', 99, 'Admin@123', 10000000, 'Premium User', 1000))
    conn.commit()
else:
    pass

def register_data(user):
    c.execute('SELECT * FROM Accounts')
    data1 = c.fetchall()
    if (user.name, user.age, user.password, user.coins, user.user_type, user.coin_limit) not in data1:
        with conn:
            c.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?, ?)', (user.name, user.age, user.password, user.coins, user.user_type, user.coin_limit))
    else:
        print('User already exists.')


def get_data(name, password):
    c.execute(f"SELECT * FROM Accounts WHERE name = '{name}'")
    data2 = c.fetchone()
    if data2 is None:
        print(f"\n                        User {name} does not exist.")
        time.sleep(1)
    elif name == data2[0]:
        if password == data2[2]:
            return data2
        else:
            print('\n                        Wrong password')
            time.sleep(1)


def check_data(name):
    c.execute(f"SELECT * FROM Accounts WHERE name = '{name}'")
    data3 = c.fetchone()
    if data3 is None:
        return True
    else:
        return False


def save_data(user):
    c.execute('UPDATE Accounts SET coins = ?, coin_limit = ? WHERE name = ?', (user.coins, user.coin_limit, user.name))
    conn.commit()


#======================================UTILITIES=====================================
def refresh_screen():
    os.system('cls')
    time.sleep(0.3)


def review_coins(user):
    print(f'Coins: {user.coins} ({user.user_type})')


def new_balance(coins):
    return f'New Balance: {coins} Coins'

def password_wrong(name):
    user_ans = input(f'You have entered the wrong {name} key.\nWould you like to try again? (Yes/No)\n> ').lower()
    return True if user_ans == 'yes' or user_ans == 'y' else False


def password_validator(name, password):
    verification = getpass.getpass(prompt=f'\nEnter the {name} key: ').lower()
    is_matched = True if verification == password else False
    return is_matched


def bet_receiver(user):
    quit1 = False
    bet_list = {'a':10, 'b':25, 'c':50, 'd':100, 'e':round(user.coins*0.5, 0), 'f':user.coins}
    multiplier = {1:1.1, 2:1.2, 3:1.3, 4:1.4, 5:1.5}
    while 1:
        prompt = input('\nTo begin, choose your bet:\nA. 10 Coins\nB. 25 Coins\nC. 50 Coins\nD. 100 Coins\nE. Half of my coins! (10% Bonus)\nF. All IN! (+25% if won)\nG. Quit\n\n> ').lower()
        if prompt == 'g':
            quit1 = True
            refresh_screen()
            break
        elif prompt in bet_list:
            if user.coins >= bet_list[prompt]:
                user.initial_bet = bet_list[prompt]
                break
            else:
                print('You cannot bet higher than your current coins.')
        else:
            print('Please enter the letter of desired amount only.')
    if not quit1:
        multiplier_value = multiplier[random.randint(1, 5)]
        if prompt == 'e':
            user.reward = int(round(user.initial_bet * 0.5 * multiplier_value, 0))
        elif prompt == 'f':
            user.reward = int(round(user.initial_bet * 1.25 * multiplier_value, 0))
        else:
            user.reward = int(round(user.initial_bet * multiplier_value, 0))
        print(f'\n[Initial bet]: {int(user.initial_bet)} Coins (Only this will be deducted if lost)')
        print(f'[Bonus Multiplier]: {multiplier_value}X')
        print(f'[Total Reward]: {user.reward} Coins.')
        time.sleep(2.5)
    return user, quit1



#=====================================ADD=COINS====================================
def add_coins(user):
    coins_list = {'a':50, 'b':100, 'c':250, 'd':500, 'z':1000}
    verify_key = {'a':'alpha', 'b':'beta', 'c':'charlie', 'd':'delta', 'z':'bonus'}
    master_key = 'castillo'
    while 1:
        display_status(user.name, user.age, user.coins, user.user_type, user.coin_limit, user.password)
        print('==============================[ADD=COINS]=============================')
        prompt = input('\nWould you like to add coins? (Yes/No)\n> ').lower()
        if prompt == 'yes' or prompt == 'y':
            while 2:
                if user.coin_limit < 1:
                    print('You have already reached your add-coins limit.')
                    break
                elif user.coin_limit >= 1:
                    display_status(user.name, user.age, user.coins, user.user_type, user.coin_limit, user.password)
                    print('==============================[ADD=COINS]=============================')
                    verification = password_validator('master', master_key)
                    if verification:
                        time.sleep(1)
                        print(f'\nSuccessful!')
                        time.sleep(0.3)
                        refresh_screen()
                        while 3:
                            display_status(user.name, user.age, user.coins, user.user_type, user.coin_limit, user.password)
                            print('==============================[ADD=COINS]=============================')
                            addition = input('\nNow enter how many coins would you like to add:\nA. 50 Coins\nB. 100 Coins\nC. 250 Coins\nD. 500 Coins\n> ').lower()
                            if addition in coins_list:
                                verify = getpass.getpass(prompt='Enter verification key: ').lower()
                                if verify == verify_key[addition]:
                                    time.sleep(1)
                                    print('Successful!')
                                    time.sleep(0.3)
                                    if user.user_type == 'Normal User':
                                        user.coins += coins_list[addition]
                                        print(f'Your new coin balance is {user.coins}.\n')
                                        user.coin_limit -= 1
                                        save_data(user)
                                        time.sleep(2)
                                        break
                                    elif user.user_type == 'Premium User':
                                        user.coins += int(coins_list[addition] * 1.5)
                                        print(f'Your new coin balance is {user.coins} (+50% Premium Bonus).\n')
                                        user.coin_limit -= 1
                                        save_data(user)
                                        time.sleep(2)
                                        break
                                else:
                                    time.sleep(1)
                                    prompt = password_wrong('master')
                                    if prompt:
                                        continue
                                    else:
                                        break
                            else:
                                print('Please enter the letter of desired value only.')
                        break
                    else:
                        prompt = password_wrong('master')
                        if prompt:
                            continue
                        else:
                            break
        elif prompt == 'no' or prompt == 'n':
            break
        else:
            print("Enter 'Yes' or 'No' only.")
    print(f'Coin Balance: {user.coins}')
    refresh_screen()
    return user


#====================================GAME=LIST========================================
#====================================DICE=HI=LO=======================================
def dice_hi_lo_display(user, has_bonus, bonus):
    print(f'[DICE HI-LO]\nWelcome {user.name}, you still have {user.coins} coins to play with this game.\n')
    if has_bonus:
        print(f'Total Reward: {user.reward} coins ({bonus} Bonus)')
    elif not has_bonus:
        print(f'Total Reward: {user.reward} coins')


def dice_hi_lo_win(user, bonus, choice):
    user.coins += round(user.reward * bonus[choice], 0)
    print('\nCongratulations!')
    print(f'{int(new_balance(user.coins))}')
    return user


def dice_hi_lo_lost(user):
    user.coins -= user.initial_bet
    print('\nYou LOST!')
    print(f'{new_balance(user.coins)}')
    return user


def dice_hi_lo(user):
    while 1:
        if user.coins <= 0:
            break
        else:
            refresh_screen()
            computer_dices = {1:random.randint(1, 6), 2:random.randint(1, 6), 3:random.randint(1, 6), 4:random.randint(1, 6)}
            player_dices = {1:random.randint(1, 6), 2:random.randint(1, 6), 3:random.randint(1, 6), 4:random.randint(1, 6)}
            dice_bonus = {'a':1.0, 'b':1.2, 'c':1.4, 'd':1.6}
            dice_dict = {'a':1, 'b':2, 'c':3, 'd':4}
            bonus_visual = {'b':'+20%', 'c':'+40%', 'd':'+60%'}
            computer_total, player_total, user.initial_bet, user.reward = 0, 0, 0, 0
            dice_hi_lo_display(user, False, 0)
            user, prompt = bet_receiver(user)
            if not prompt:
                os.system('cls')
                dice_hi_lo_display(user, False, 0)
                user_choice = input('\nHow many dices would you like to play?\nA. 1 Die (No Bonus)\nB. 2 Dice (20% Bonus)\nC. 3 Dice (40% Bonus)\nD. 4 Dice (60% Bonus)\nE. Quit\n\n> ').lower()
                if user_choice == 'e':
                    os.system('cls')
                    break
                elif user_choice in dice_dict:
                    user.reward = int(user.reward * dice_bonus[user_choice])
                    while 2:
                        validator = ['hi', 'high', 'lo', 'low']
                        os.system('cls')
                        dice_hi_lo_display(user, True if user_choice in bonus_visual else False, bonus_visual[user_choice] if user_choice in bonus_visual else 0 )
                        hi_lo = input('\nDo you think you will have the higher value or lower value?\n\n(High/Low): ').lower()
                        if hi_lo in validator:
                            os.system('cls')
                            dice_hi_lo_display(user, True if user_choice in bonus_visual else False, bonus_visual[user_choice] if user_choice in bonus_visual else 0)
                            print(f'\n         Computer         {user.name}')
                            for value in range(1, dice_dict[user_choice] + 1):
                                time.sleep(1.5)
                                print(f'        Dice {value}: {computer_dices[value]}!      Dice {value}: {player_dices[value]}!')
                                computer_total += computer_dices[value]
                                player_total += player_dices[value]
                            time.sleep(1.5)
                            print(f'\nComputer: {computer_total} Overall\n{user.name}: {player_total} Overall')
                            time.sleep(1)
                            if hi_lo == 'high' or hi_lo == 'hi':
                                if player_total > computer_total:
                                    dice_hi_lo_win(user, dice_bonus, user_choice)
                                elif player_total < computer_total:
                                    dice_hi_lo_lost(user)
                                elif player_total == computer_total:
                                    print("It's a tie!")
                            elif hi_lo == 'low' or hi_lo == 'lo':
                                if player_total < computer_total:
                                    dice_hi_lo_win(user, dice_bonus, user_choice)
                                elif player_total > computer_total:
                                    dice_hi_lo_lost(user)
                                elif player_total == computer_total:
                                    print("It's a tie!")
                            save_data(user)
                            break
                        else:
                            print("Please enter 'High' or 'Low' only.")
                else:
                    print('Please enter the letter of your choice.')
            elif prompt:
                break
        prompt = input('Would you like to try again? (Yes/No): ').lower()
        if prompt == 'yes' or prompt == 'y':
            continue
        elif prompt == 'no' or prompt == 'n':
            os.system('cls')
            break
        else:
            print("Enter 'Yes' or 'No' only.")
    return user


#===================================GUESS=THE=NUMBER===================================
def guess_the_number_display(user, secret_number, is_shown, start, end):
    print(f'[GUESS THE NUMBER!]\nWelcome {user.name}, you still have {user.coins} coins to play with this game.\n')
    if not is_shown:
        print(f'Total Reward: {user.reward} coins')
        print(f'SECRET NUMBER: {secret_number}'.replace(str(secret_number), '##'))
        print(f'The number ranges from {start} to {end}.')
    elif is_shown:
        print(f'Total Reward: {user.reward} Coins')
        print(f'SECRET NUMBER: {secret_number}')



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
                        print('\nYou ran out of guesses, YOU LOST!')
                        user.coins -= user.initial_bet
                        print(f'{new_balance(user.coins)}')
                        save_data(user)
                        break
                    else:
                        os.system('cls')
                        guess_the_number_display(user, secret_number, False, start_value, end_value)
                        print(f'Number of tries: {guess_limit} guess left.')
                        try:
                            user_guess = int(input('\nEnter your guess: '))
                            if user_guess != secret_number and guess_limit != 0:
                                if start_value <= user_guess <= end_value:
                                    if secret_number < user_guess:
                                        print('Computer says: Lower!')
                                        guess_limit -= 1
                                        time.sleep(1)
                                    elif secret_number > user_guess:
                                        print('Computer says: Higher!')
                                        guess_limit -=1
                                        time.sleep(1)
                                else:
                                    print(f'Enter an integer from {start_value} to {end_value} only.')
                                    time.sleep(2)
                            elif user_guess == secret_number:
                                os.system('cls')
                                guess_the_number_display(user, secret_number, True, start_value, end_value)
                                print('\n\nCongratulations!')
                                user.coins += user.reward
                                print(f'{new_balance(user.coins)}')
                                save_data(user)
                                break
                        except ValueError:
                            print('Please enter a valid integer.')
                            time.sleep(1)

                prompt = input('Would you like to try again? (Yes/No): ').lower()
                if prompt == 'yes' or prompt == 'y':
                    continue
                elif prompt == 'no' or prompt == 'n':
                    os.system('cls')
                    break
                else:
                    print("Enter 'Yes' or 'No' only.")
            elif prompt:
                break
    return user


#======================================LAST=SECTION=========================================
def initial_menu(user):
    while True:
        if user.coins <= 0:
            print('\n\nYou do not have enough coins to play. Please contact developer to buy more coins.')
            time.sleep(5)
            quit()
        else:
            display_status(user.name, user.age, user.coins, user.user_type, user.coin_limit, user.password)
            game_choice = input('==============================[MAIN=MENU]=============================\n   Choose a game:\n    A. Guess The Number      D. (unavailable)\n    B. Dice (Hi-Lo)          E. Add Coins (requires master key)\n    C. (unavailable)         F. Quit\n\n> ').lower()
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
                    print('You have already reached your add-coins limit.')
                    time.sleep(1)
                    refresh_screen()
            elif game_choice == 'f':
                last_prompt = input('Are you sure? (Your data will be saved.)\n(Yes/No): ').lower()
                if last_prompt == 'yes' or last_prompt == 'y':
                    save_data(user)
                    quit()
                else:
                    os.system('cls')
            else:
                print('Enter the letter of desired option only.')
                time.sleep(1.5)
                refresh_screen()


#=======================================LOG=IN=INTERFACE===============================================
def registration_banner():
    print('============================[REGISTRATION]============================')


def display_status(name, age, coins, user_type, coin_limit, password):
    os.system('cls')
    print(f"""===============================[STATUS]===============================
        Username: {name}
        Age: {age}
        Subscription: {user_type}
        Coins: {coins}
        Number of times to buy coins: {coin_limit}
        Password: {'' if password == '' else '*' * len(password)}""")


def get_name():
    while 1:
        display_status('', '', '', '', '', '')
        registration_banner()
        name = input('\nThe username must be 3 to 10 alphanumeric characters and no spaces.\nEnter your username: ')
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
        display_status(name, '', '', '', '', '')
        registration_banner()
        print('\nYour age must be 18 or above to play gambling games.')
        try:
            age = int(input('Enter your age: '))
            if age < 18:
                print('You are not allowed to play gambling games.\nProgram will exit...')
                time.sleep(3)
                quit()
            elif 18 <= age <= 100:
                return age
            elif age > 100:
                print('You seem too impossible to be alive.')
                time.sleep(1.5)
            else:
                print('Please enter a valid age value.')
                time.sleep(1.5)
        except ValueError:
            print('Please enter a valid age value.')
            time.sleep(1.5)


def get_user_type(name, age):
    while 1:
        subscription_list = {'a':'Premium User', 'b':'Normal User'}
        display_status(name, age, '', '', '', '')
        registration_banner()
        prompt = input('\nEnter your subscription type:\n\nA. Premium User (Requires subscription key)\nB. Normal User (Does not require subscription key)\n\n(Letter only.)\n> ').lower()
        if prompt == 'a':
            subscription_key = 'glenn'
            while 2:
                display_status(name, age, '', '', '', '')
                registration_banner()
                verification = password_validator('subscription', subscription_key)
                if verification:
                    print('Password matched!')
                    time.sleep(1)
                    return subscription_list['a'], 500, 3
                elif not verification:
                    while 3:
                        display_status(name, age, '', '', '', '')
                        registration_banner()
                        prompt2 = input('You have entered the wrong subscription key. Would you like to try again?\n(Yes/No): ')
                        if prompt2 == 'yes' or prompt2 == 'y':
                            break
                        elif prompt2 =='no' or prompt2 == 'n':
                            return subscription_list['b'], 200, 1
                        else:
                            print("Enter 'YES' or 'NO' only.")
        elif prompt == 'b':
            return subscription_list['b'], 200, 1
        else:
            print("Enter 'A' or 'B' only.")


def get_pass(name, age, coins, user_type, coin_limit):
    while 1:
        display_status(name, age, coins, user_type, coin_limit, '')
        registration_banner()
        password = getpass.getpass(prompt='\nThe password must be 3 to 10 alphanumeric characters and no spaces.\nEnter your password: ')
        if 3 <= len(password) <= 10 and ' ' not in password:
            while 2:
                display_status(name, age, coins, user_type, coin_limit, '')
                registration_banner()
                verify = getpass.getpass(prompt='\nVerify your password: ')
                if password == verify:
                    print('Password matched!')
                    time.sleep(1)
                    print('Returning to log-in screen...')
                    time.sleep(1)
                    return password
                else:
                    prompt = input('Verification does not matched your password, would you like to try again? (Yes/No): ').lower()
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


def login():
    while 1:
        os.system('cls')
        name = input(f"""
            
            
                        Username: """)
        password = getpass.getpass('                        Password: ')
        user_data = get_data(name, password)
        if user_data is None:
            continue
        else:
            user = UserInfo(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], 0, 0)
            return user


def initial_screen():
    while 1:
        os.system('cls')
        prompt = input("""
        
        
                    Do you have an account?
                              """).lower()
        if prompt == 'yes' or prompt == 'y':
            user = login()
            initial_menu(user)
        elif prompt == 'no' or prompt == 'n':
            registration_menu()
        else:
            continue


initial_screen()
