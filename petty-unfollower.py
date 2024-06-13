from instabot import Bot
import maskpass
import pyfiglet
import glob
import os

# import pyfiglet # when creating .exe with PyInstaller, make sure to include "--collect-all pyfiglet" flag !!!
# for .exe --> "py -m PyInstaller -i example.ico --onefile .\petty-unfollower.py" ON WINDOWS SYSTEM 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

bot = Bot()

clear_screen()

# Petty Unfollower 
print(pyfiglet.figlet_format('Petty Unfollower', font = 'smslant', width = 250))
print('BECAUSE IF THEY DON\'T FOLLOW YOU BACK, WHY SHOULD YOU ???')
print('To terminate program at any time, press CTRL + C \n')
print('DISCLAIMER: Please limit the amount of logins/requests you make using this program as it may cause login session/cookie issues\n')

username = input('Please enter your username: ')
password = maskpass.askpass('Please enter your password: ')
clear_screen()

# Deletes cookie session to prevent login errors after logging in multiple times --> ADD ERROR HANDLING 
def delete_cookie():
    cookie_del = glob.glob('config/*cookie.json')
    if len(cookie_del) > 0:
        os.remove(cookie_del[0])
delete_cookie()

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

def list_all_nonfollowers():
    for num, user in nonfollowers.items():
        print(f'{num}: @{user}')

# Choice 1 - List all nonfollowers
def choice_1():
    clear_screen()
    list_all_nonfollowers()
    print(f'\n{len(nonfollowers.keys())} account(s) currently DO NOT follow you back \n')
    input('Press ENTER key to continue...')

# Choice 2 - Unfollow a specific account
def choice_2():
    while True:
        clear_screen()  
        print('Listing ALL accounts that don\'t follow you back: \n')
        list_all_nonfollowers()
        print(f'\n{len(nonfollowers.keys())} account(s) currently DO NOT follow you back')
        print('\nEnter 0 to exit to Main Menu')
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
                        bot.unfollow(nonfollowers[int(number)])
                        del nonfollowers[int(number)]
        except ValueError:
            print('Error: Input must be a number...')

# Main Menu 
def main_menu():
    while True:
        # Select an action
        clear_screen()
        print('1. List ALL nonfollowers \n')
        print('2. Unfollow an account \n')
        print('3. Exit \n')
        choice = input('Select an action above (1/2/3): ')
        if choice == '1':
            choice_1()
        elif choice == '2':
            choice_2()
        elif choice == '3':
            clear_screen()
            print('Bye bye')
            quit()
main_menu()