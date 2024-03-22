from instabot import Bot
import maskpass
import os
import glob

#import pyfiglet # when creating .exe with PyInstaller, make sure to include "--collect-all pyfiglet" flag !!!

# for .exe --> "py -m PyInstaller -i example.ico --onefile .\petty-unfollower.py" ON WINDOWS SYSTEM 
# for .app (mac osx) --> "python setup.py py2app" config on MAC OSX SYSTEM

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

bot = Bot()

clear_screen()

# Petty Unfollower 
# print(pyfiglet.figlet_format('Petty Unfollower', font = 'smslant', width = 250))
print('   ___      __  __         __  __     ___     ____')
print('  / _ \___ / /_/ /___ __  / / / /__  / _/__  / / /__ _    _____ ____')
print(' / ___/ -_) __/ __/ // / / /_/ / _ \/ _/ _ \/ / / _ \ |/|/ / -_) __/')
print('/_/   \__/\__/\__/\_, /  \____/_//_/_/ \___/_/_/\___/__,__/\__/_/   ')
print('                 /___/')
print('BECAUSE IF THEY DON\'T FOLLOW YOU BACK, WHY SHOULD YOU ???')
print('\nPetty Unfollower v1.0 (Instagram) - March 21, 2024 Release')
print('To terminate program at any time, press CTRL + C \n')
print('DISCLAIMER: Please limit the amount of logins/requests you make using this program as it may cause login and cookie issues')
print('You may have to use a VPN or wait certain periods of time if you encounter login errors at any point, so PLEASE use this accordingly... \n')

username = input('Please enter your username: ')
password = maskpass.askpass('Please enter your password: ')
clear_screen()

# Deletes cookie session to prevent login errors after logging in multiple times --> ADD ERROR HANDLING 
cookie_del = glob.glob('config/*cookie.json')
if len(cookie_del) > 0:
    os.remove(cookie_del[0])

# Attempt login 
bot.login(username=username, password=password) # line 559-585 is commented out to prevent error 529 in api.py to proceed login
clear_screen()
print('Successfully logged in...')

# Your instagram user id  
user_id = bot.get_user_id_from_username(username)

# Get your Followers and your Following
followers = bot.get_user_followers(username)
following = bot.get_user_following(username)

# Get usernames of nonfollowers 
clear_screen()
print('Getting ALL current nonfollowers, please wait...')
non_follower_ids = set(following) - set(followers)
nonfollowers = {}
count = 1
for id in non_follower_ids:
    nonfollowers[count] = bot.get_username_from_user_id(id)
    count += 1

def choice_1():
    clear_screen()
    for num, user in nonfollowers.items():
        print(f'{num}: {user}')
    print(f'\n{len(nonfollowers.keys())} account(s) currently DO NOT follow you back \n')
    input('Press ENTER key to continue...')

def choice_2():
    clear_screen()  
    print('Listing ALL accounts that don\'t follow you back: \n')
    for num, user in nonfollowers.items():
        print(f'{num}: {user}')
    print(f'\n{len(nonfollowers.keys())} account(s) currently DO NOT follow you back')
    print('\nEnter 0 to exit to Main Menu')
    while True:
        number = input('\nSelect a number to unfollow or "0" for Main Menu: ')
        try:
            if int(number) == 0:
                main_menu()
            if int(number) in nonfollowers.keys():
                print(f'You selected {int(number)}: {nonfollowers[int(number)]}')
                decision = input('Are you want to unfollow this account? (y/n): ')
                if decision.casefold() == 'y':
                    decision = input('ARE YOU SURE? (y/n): ')
                    if decision.casefold() == 'y':
                        clear_screen()
                        bot.unfollow(bot.get_user_id_from_username(nonfollowers[int(number)]))
                        del nonfollowers[int(number)]
        except ValueError:
            print('Error: Input must be a number...')

def choice_3():
    clear_screen()
    for num, user in nonfollowers.items():
        print(f'{num}: {user}')
    print('\nEnter "0" to exit to Main Menu')
    while True:
        try:
            decision = input('\nAll of your nonfollowers are above, would you like to unfollow ALL OF THEM? (y/n/0): ')
            if decision.casefold() == 'y':
                decision = input('ARE YOU SURE? (y/n): ')
                if decision.casefold() == 'y':
                    clear_screen()
                    bot.unfollow_non_followers()
                    nonfollowers.clear()
            if int(decision) == 0:
                main_menu()
        except ValueError:
            print('Error: Please select a valid option')

# Main Menu 
def main_menu():
    while True:
        # Select an action
        clear_screen()
        print('1. List ALL nonfollowers \n')
        print('2. Unfollow a SPECIFIC account \n')
        print('3. Unfollow ALL nonfollowers \n')
        print('4. Exit \n')
        choice = input('Select an action above (1/2/3/4): ')
        if choice == '1':
            choice_1()
        elif choice == '2':
            choice_2()
        elif choice == '3':
            choice_3()
        elif choice == '4':
            clear_screen()
            print('Bye bye')
            quit()
main_menu()