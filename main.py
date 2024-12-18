import json
import random
from urllib.parse import parse_qs, unquote
from colorama import Fore, Style, init
import time
from tomarket import Tomarket, print_timestamp
import sys

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return [  ]
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def load_cex():
     data = json.loads(open("cex.json").read())
     return data

def generate_token():
    tom = Tomarket()
    queries = load_credentials()
    sum = len(queries)
    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
        token = get(user['id'])
        if token == None:
            print_timestamp("Generate token...")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print_timestamp("Generate Token Done!")
        

                

def main():
    init(autoreset=True)
    tom = Tomarket()
    auto_task = input("auto clear task y/n  : ").strip().lower()
    auto_game = input("auto play game  y/n  : ").strip().lower()
    auto_combo = input("auto claim combo puzzle y/n : ").strip().lower()
    auto_convert = input("auto convert star y/n : ").strip().lower()
    random_number = input("set random score in game 300-500  y/n  : ").strip().lower()
    free_raffle = input("enable free raffle  y/n  : ").strip().lower()
    used_stars = input("use star for : 1. upgrade rank | 2.auto spin | n.(skip all) (1/2/n): ").strip().lower()
    while True:
        queries = load_credentials()
        sum = len(queries)
        delay = int(6 * random.randint(3700, 3750))
        # generate_token()
        start_time = time.time()
                
        for index, query in enumerate(queries):
            mid_time = time.time()
            total = delay - (mid_time-start_time)
            parse = parse_query(query)
            user = parse.get('user')
            token = get(user['id'])
            if token == None:
                token = tom.user_login(query)
                save(user.get('id'), token)
                time.sleep(2)
            print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
            tom.rank_data(token=token, selector=used_stars)
            time.sleep(2)
            tom.claim_daily(token=token)
            time.sleep(2)
            tom.start_farm(token=token)
            time.sleep(2)
            if free_raffle == "y":
                tom.free_spin(token=token, query=query)
            time.sleep(2)
        
        if auto_task == 'y':
            for index, query in enumerate(queries):
                mid_time = time.time()
                total = delay - (mid_time-start_time)
                if total <= 0:
                    break
                parse = parse_query(query)
                user = parse.get('user')
                token = get(user['id'])
                if token == None:
                    token = tom.user_login(query)
                print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
                tom.list_tasks(token=token,query=query)
                if auto_combo == 'y':
                    tom.puzzle_task(token, query)
                # tom.rank_data(token=token)
                time.sleep(2)   
                
        if auto_game == 'y':
            for index, query in enumerate(queries):
                mid_time = time.time()
                total = delay - (mid_time-start_time)
                if total <= 0:
                    break
                parse = parse_query(query)
                user = parse.get('user')
                token = get(user['id'])
                if token == None:
                    token = tom.user_login(query)
                print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
                tom.user_balance(token=token, random_number=random_number, auto_convert=auto_convert)
                time.sleep(2)

        

        end_time = time.time()
        total = delay - (end_time-start_time)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Restarting In {int(hours)} Hours {int(minutes)} Minutes {int(seconds)} Seconds ]{Style.RESET_ALL}")
        if total > 0:
            time.sleep(total)


def check_elig():
    tom = Tomarket()
    queries = load_credentials()
    sum = len(queries)
    selector_weekly = input("auto claim $TOMA weekly y/n : ").strip().lower()
    selector_og = 'n'
    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
        token = get(user['id'])
        if token == None:
            print_timestamp("Generate token...")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print_timestamp("Generate Token Done!")
        time.sleep(3)
        tom.check_elig(token, query)
        time.sleep(2)
        tom.airdrop_task(token, query)
        time.sleep(2)
        if selector_og == 'y':
            tom.checked(token=token, query=query, round='OG')
        if selector_weekly == "y":
            tom.checked(token=token, query=query, round='One')

def check_og():
    tom = Tomarket()
    queries = load_credentials()
    sum = len(queries)

    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
        token = get(user['id'])
        if token == None:
            print_timestamp("Generate token...")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print_timestamp("Generate Token Done!")
        time.sleep(3)
        # tom.checked(token=token, query=query, round='OG')
        

def predeposit():
    tom = Tomarket()
    queries = load_credentials()
    sum = len(queries)

    for index, query in enumerate(queries):
        parse = parse_query(query)
        user = parse.get('user')
        print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Account {index+1}/{sum} {user.get('first_name','')} ]{Style.RESET_ALL}")
        token = get(user['id'])
        if token == None:
            print_timestamp("Generate token...")
            time.sleep(2)
            token = tom.user_login(query)
            save(user.get('id'), token)
            print_timestamp("Generate Token Done!")
        time.sleep(3)
        data_cex = load_cex()
        list = data_cex.get('list')
        data = random.choice(list)
        data_pre = tom.predeposit(token, query)
        cex = data_pre.get('cex')
        availableToma = data_pre.get('availableToma')
        totalToma = data_pre.get('totalToma')
        if len(cex) == 0:
            payload = {
                'amount': availableToma,
                'chain': 'aptos',
                'cex_name': data.get('cex_name'),
                'cex_uid': data.get('uid'),
                'wallet_address': data.get('address')
            }
            tom.predepositupdate(token, payload)
        else:
            data = cex[0]
            print_timestamp(f"Cex : {data.get('cexName')} | UID : {data.get('cexUid')}")
            print_timestamp(f"Amount : {data.get('lockToma')} | Address : {data.get('walletAddress')}")

def start():
    print(r"""
        
                    TOMARKET BOT
    find new airdrop & bot here: t.me/sansxgroup
              
        select this one :
        1. claim daily
        2. generate token
        3. check eligibility & claim season reward
        4. check reward early adopter
        5. predeposit
          """)
    selector = input("Select the one  : ").strip().lower()

    if selector == '1':
        main()
    elif selector == '2':
        generate_token()
    elif selector == '3':
        check_elig()
    elif selector == '4':
        check_og()
    elif selector == '5':
        predeposit()
    else:
        exit()

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)