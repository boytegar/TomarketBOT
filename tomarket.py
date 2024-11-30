from colorama import Fore, Style
from datetime import datetime
from fake_useragent import FakeUserAgent
from time import sleep, time
from urllib.parse import parse_qs, unquote
import json
import random
import requests

def print_timestamp(message):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(
        f"{Fore.BLUE + Style.BRIGHT}[ {now} ]{Style.RESET_ALL}"
        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
        f"{message}"
    )


class Tomarket:
    def __init__(self):
        self.headers = {
            "host": "api-web.tomarket.ai",
            "connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://mini-app.tomarket.ai",
            "x-requested-with": "tw.nekomimi.nekogram",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://mini-app.tomarket.ai/",
            "accept-language": "en-US,en;q=0.9",
        }

    def parse_query(self, query: str):
        parsed_query = parse_qs(query)
        parsed_query = {k: v[0] for k, v in parsed_query.items()}
        user_data = json.loads(unquote(parsed_query['user']))
        parsed_query['user'] = user_data
        return parsed_query

    def user_login(self, query):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
        try:
            while True:
                payload = {
                    'init_data': query,
                    'invite_code': '',
                    'is_bot': False
                }
                response = requests.post(url=url, headers=self.headers, json=payload)
                data = self.response_data(response)
                token = f"{data['data']['access_token']}"
                return token
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def user_balance(self, token, random_number, auto_convert):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
        try:
            self.headers.update({
                'Authorization': token
            })
            response = requests.post(url=url, headers=self.headers)
            data = self.response_data(response)
            if data is not None:
                balances = data['data']['available_balance']
                print_timestamp(
                    f"{Fore.YELLOW + Style.BRIGHT}[ Available Balance {balances} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}[ Play Passes {data['data']['play_passes']} ]{Style.RESET_ALL}"
                )
                if auto_convert == 'y':
                    if balances > 20000:
                        sleep(2)
                        self.convert_star(token)
                        
                while data['data']['play_passes'] > 0:
                    sleep(2)
                    point = 600
                    if random_number =='y':
                        point = random.randint(300,500)
                    self.play_game(token=token, point=point)
                    data['data']['play_passes'] -= 1
            else:
                print_timestamp('user balance data not found')
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def play_game(self, token, point):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
        try:
            self.headers.update({
                'Authorization': token
            })
            
            payload = {
                'game_id': '59bcd12e-04e2-404c-a172-311a0084587d'
            }
            response = requests.post(url=url, headers=self.headers, json=payload)
            data = self.response_data(response)
            if data is not None:
                if data['status'] == 0:
                    start_time = datetime.fromtimestamp(data['data']['start_at'])
                    end_time = datetime.fromtimestamp(data['data']['end_at'])
                    total_time = end_time - start_time
                    total_seconds = total_time.total_seconds()
                    print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Game Started Please Wait {int(total_seconds)} Seconds ]{Style.RESET_ALL}")
                    datas = data.get('data',{})
                    stars = datas.get('stars',0)
                    slp = random.randint(30, 35)
                    sleep(slp)
                    self.claim_game(token=token, points=point, stars=stars)
                elif data['status'] == 500:
                    print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ No Chance To Play Game ]{Style.RESET_ALL}")
                else:
                    print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
            else:
                print_timestamp('Data play game is None')
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def convert_star(self, token):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/tomatoToStar'
        try:
            self.headers.update({
                'Authorization': token
            })
            response = requests.post(url=url, headers=self.headers)
            data = self.response_data(response)
            if data is not None:
                if data['status'] == 0:
                    datas = data.get('data')
                    success = datas.get('success')
                    if success:
                        print_timestamp("Convert To Star Done")
                else:
                    print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
            else:
                print_timestamp('Data play game is None')
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def claim_game(self, token: str, points: int, stars: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
        try:
            self.headers.update({
                'Authorization': token
            })
            payload = {
                'game_id': '59bcd12e-04e2-404c-a172-311a0084587d',
                'points': points,
                'stars': stars
            }
            response = requests.post(url=url, headers=self.headers, json=payload)
            data = self.response_data(response)
            if data is not None:
                if data['status'] == 0:
                    print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Game Claimed {data['data']['points']} Tomato & {data['data']['stars']} Stars ]")
                elif data['status'] == 500:
                    print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Game Not Start ]")
                    self.play_game(token=token, point=points)
                else:
                    print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
            else:
                print_timestamp('Data play game is None')
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def claim_daily(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
        
        self.headers.update({
                'Authorization': token
        })
        payload = {
                'game_id': 'fa873d13-d831-4d6f-8aee-9cff7a1d0db1'
        }
        while True:
            response = requests.post(url=url, headers=self.headers, json=payload)
            data = self.response_data(response)
            if data is not None:
                if data['status'] == 0:
                    return print_timestamp(
                            f"{Fore.GREEN + Style.BRIGHT}[ Daily Claim ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Day {data['data']['today_game']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Points {data['data']['today_points']} ]{Style.RESET_ALL}"
                    )
                    
                elif data['status'] == 400:
                    return print_timestamp(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Already Check Daily Claim ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Day {data['data']['today_game']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Points {data['data']['today_points']} ]{Style.RESET_ALL}"
                        )
                else:
                    return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
            else:
                print_timestamp('data claim daily not found')
            sleep(2)            

    def start_farm(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
        try:
            self.headers.update({
                'Authorization': token
            })
            payload = {
                'game_id': '53b22103-c7ff-413d-bc63-20f6fb806a07'
            }
            while True:
                response = requests.post(url=url, headers=self.headers, json=payload)
                data = self.response_data(response)
                if data is not None:
                    end_time = datetime.fromtimestamp(data['data']['end_at'])
                    now = datetime.now()
                    remaining_time = end_time - now
                    if data['status'] == 0:
                        print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Start Farm ]{Style.RESET_ALL}")
                        if remaining_time.total_seconds() > 0:
                            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Please Wait {int(hours)} Hours {int(minutes)} Minutes {int(seconds)} Seconds To Claim Farm ]{Style.RESET_ALL}")
                            break
                        else:
                            self.claim_farm(token=token)
                            break
                    elif data['status'] == 500:
                        print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farm Already Started ]{Style.RESET_ALL}")
                        if remaining_time.total_seconds() > 0:
                            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Please Wait {int(hours)} Hours {int(minutes)} Minutes {int(seconds)} Seconds To Claim Farm ]{Style.RESET_ALL}")
                            break
                        else:
                            self.claim_farm(token=token)
                            break
                    else:
                        print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
                else:
                    print_timestamp('data start farm not found')
                sleep(2)
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def claim_farm(self, token: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/claim'
        try:
            self.headers.update({
                'Authorization': token
            })
            payload = {
                'game_id': '53b22103-c7ff-413d-bc63-20f6fb806a07'
            }
            while True:
                response = requests.post(url=url, headers=self.headers, json=payload)
                data = self.response_data(response)
                if data is not None:
                    if data['status'] == 0:
                        print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed {data['data']['points']} From Farm ]")
                        self.start_farm(token=token)
                        break
                    else:
                        print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
                else:
                    print_timestamp('data claim not found')
                sleep(2)
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def list_tasks(self, token: str, query: str):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/list'
        try:
            payload = {
                'language_code': 'en'
            }
            data = json.dumps(payload)
            self.headers.update({
            'Authorization': token,
            # 'Content-Length': str(len(data)),
            # 'Content-Type': 'application/json'
                })
            response = requests.post(url=url, headers=self.headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            data = response_json.get('data')
            special = data.get('special',[])
            standard = data.get('standard', [])
            expire = data.get('expire', [])
            default = data.get('default', [])
            free_tomato = data.get('free_tomato',[])
            thirds = data.get('3rd',{})
            default = thirds.get('default',[])
            # invite_star_group = data.get('invite_star_group',[])
            invite_star_group = []
            for task in default:
                if task['status'] == 0 and task['type'] == "mysterious":
                    current_time = datetime.now()
                    date_part = current_time.strftime("%Y-%m-%d")
                    split_time  = task.get('startTime')
                    end_time = split_time.split(" ")[0]
                    if date_part == end_time:
                        print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming {task['title']} ]{Style.RESET_ALL}")
                        self.claim_tasks(token=token, task_id=task['taskId'])
                        sleep(2)
            
            for task in special:
                self.clear_task(query, token, task)

            for task in free_tomato:
                self.clear_task(query, token, task)

            for task in invite_star_group:
                self.clear_task(query, token, task)

            for task in standard:
                self.clear_task(query, token, task)
            
            for task in expire:
                self.clear_task(query, token, task)
            
            for task in default:
                self.clear_task(query, token, task)

        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def clear_task(self, query, token, task):
        if task['status'] == 1:
            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finish Or Start This {task['title']} Task ]{Style.RESET_ALL}")
            trys = 9
            while True:
                if trys <= 0:
                    break
                sleep(5)
                data = self.check_tasks(token=token, task_id=task['taskId'], init_data=query)
                if data['data']['status'] == 2:
                    self.claim_tasks(token=token, task_id=task['taskId'])
                    break
                trys -= 1

        elif task['status'] == 2:
            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming {task['title']} ]{Style.RESET_ALL}")
            self.claim_tasks(token=token, task_id=task['taskId'])
            sleep(2)

        elif task['status'] == 0:
            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting {task['title']} ]{Style.RESET_ALL}")
            self.start_tasks(query=query, token=token, task_id=task['taskId'])
            sleep(5)
            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finish Or Start This {task['title']} Task ]{Style.RESET_ALL}")
            trys = 9
            while True:
                if trys <= 0:
                    break
                sleep(3)
                data = self.check_tasks(token=token, task_id=task['taskId'],init_data=query)
                if data['data']['status'] == 2:
                    self.claim_tasks(token=token, task_id=task['taskId'])
                    break
                trys -= 1

    def start_tasks(self,query: str, token: str, task_id: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/start'
        try:
            
            payload = {
                'task_id': task_id,
            }
            data = json.dumps(payload)
            self.headers.update({
            'Authorization': token,
                })
            response = requests.post(url=url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except (Exception) as e:
            return print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {e} ]{Style.RESET_ALL}")

    def check_tasks(self, token: str, task_id: int, init_data):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/check'
        
        payload = {
                'task_id': task_id,
                'init_data': init_data
        }
        data = json.dumps(payload)
        self.headers.update({
            'Authorization': token,
                })
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        return data
            

    def claim_tasks(self, token: str, task_id: int):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/claim'
        
        self.headers.update({
            'Authorization': token
        })
        payload = {
           'task_id': task_id
        }
        response = requests.post(url=url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 0:
            print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed ]{Style.RESET_ALL}")
        elif data['status'] == 500:
            print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ You Haven't Finish Or Start This Task ]{Style.RESET_ALL}")
        elif data['status'] == 401:
            print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Invalid Task ]")
        else:
            print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {data['message']} ]{Style.RESET_ALL}")
    
    def validate(self, token):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/rank/evaluate'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers)
        data = self.response_data(response)
        return data
        

    def create(self, token):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/rank/create'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers)
        data = self.response_data(response)
        return data

    def upgrade_rank(self, token, payload):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/rank/upgrade'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        return data

    def share_tg(self, token):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/rank/sharetg'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers)
        data = self.response_data(response)
        return data

    def raffle(self, token, payload):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/spin/raffle'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers,json=payload)
        data = self.response_data(response)
        return data

    def rank_data(self, token, selector):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/rank/data'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers)
        data = self.response_data(response)
        if data is not None:
            if data.get('status',400) == 0:
                dat = data.get('data',{})
                isCreated = dat.get('isCreated')
                if isCreated:
                    currentRank = dat.get('currentRank')
                    nextRank = dat.get('nextRank')
                    unusedStars = dat.get('unusedStars')
                    print_timestamp(f"[ Rank : {currentRank.get('name')} | Level : {currentRank.get('level')} | Stars: {unusedStars} ]")
                    stars = currentRank.get('stars')
                    ranges  = currentRank.get('range')
                    butuh = ranges-stars
                    minStar = nextRank.get('minStar',0)
                    range = nextRank.get('range', 0)
                    if selector == '1':
                        if unusedStars >= butuh:
                            print_timestamp('[ Upgraded Rank... ]')
                            sleep(2)
                            payload = {'stars': unusedStars}
                            upgrade_data = self.upgrade_rank(token=token, payload=payload)
                            if upgrade_data is not None:
                                data = upgrade_data.get('data',{})
                                currentRank = data.get('currentRank')
                                sleep(1)
                                data_share_tg = self.share_tg(token=token)
                                if data_share_tg is not None:
                                    print_timestamp(f"[ Upgrade to rank {currentRank.get('name')} Done ]")
                        else:
                            print_timestamp(f"[ Need {range-unusedStars} stars to upgrade rank {nextRank.get('name', 'none')} ]")
                            
                    elif selector == '2':
                        if unusedStars > 0:
                            print_timestamp('[ Playing raffle... ]')
                            payload = {'category': "tomarket"}
                            data_raffle = self.raffle(token=token, payload=payload)
                            if data_raffle is not None:
                                status = data_raffle.get('status', 0)
                                if status == 0:
                                    data = data_raffle.get('data',{})
                                    result = data.get('results',[])
                                    for res in result:
                                        print_timestamp(f"[ Raffle Done, Reward {res.get('amount',0)} {res.get('type')} ]")
                                else:
                                    print_timestamp("error")
                        else:
                            print_timestamp('[ No stars to play raffle ]')
                else:
                    sleep(2)
                    data_validate = self.validate(token)
                    if data_validate is not None:
                        if data_validate.get('status',400) == 0:
                            print_timestamp("Validate Rank...")
                            sleep(2)
                            data_create = self.create(token)
                            if data_create is not None:
                                if data_create.get('status',400) == 0:
                                    dats = data_create.get('data')
                                    curRank = dats.get('currentRank')
                                    print_timestamp(f"Rank : {curRank.get('name')} | Level : {curRank.get('level')}")

            else:
                print_timestamp(data.get('message','Data Rank Not Found'))

    def free_spin(self, token, query):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/tickets'
        payload = {"language_code":"en","init_data":query}
        self.headers.update({
            'Authorization': token
        })
        
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            payloads = {"category":"ticket_spin_1"}
            status = data.get('status')
            if status == 0:
                dats = data.get('data')
                ticket_spin_1 = dats.get('ticket_spin_1',0)
                while True:
                    if ticket_spin_1 > 0:
                        print_timestamp('Open Free Raffle')
                        sleep(2)
                        data_raffle = self.raffle(token=token, payload=payloads)
                        if data_raffle is not None:
                            status = data_raffle.get('status', 0)
                            if status == 0:
                                ticket_spin_1 -= 1
                                data = data_raffle.get('data',{})
                                result = data.get('results',[])
                                for res in result:
                                    print_timestamp(f"[ Raffle Done, Reward {res.get('amount',0)} {res.get('type')} ]")
                            else:
                                print_timestamp("error")
                    else:
                        break

        return data

    def get_combo_puzzle(self):
        url = 'https://raw.githubusercontent.com/boytegar/TomarketBOT/refs/heads/master/combo.json'
        response = requests.get(url)
        data = self.response_data(response)
        return data

    def checked(self, token, query, round):
        self.headers.update({
            'Authorization': token
        })
        payload = {"language_code":"en","init_data":query,"round":round}
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/check'
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                print_timestamp(f"Checked Reward {round}")
                datas = data.get('data',{})
                tomaAirDrop = datas.get('tomaAirDrop')
                amount = tomaAirDrop.get('amount')
                claimed = datas.get('claimed')
                if claimed:
                    print_timestamp(f"Claimed Airdrop Done, Reward {amount} $TOMA")
                    sleep(2)
                    if round == 'One':
                        self.season(token, query)
                else:
                    self.toma_claim(token, round)
    
    def season(self, token, query):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/season'
        self.headers.update({
            'Authorization': token
        })
        payload = {"language_code":"en","init_data":query}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                print_timestamp("Check Season Reward")
                datas = data.get('data',{})
                
                claimed = datas.get('claimed', True)
                round = datas.get('round')
                name = round.get('name')
                isBoost = datas.get('isBoost', False)
                if claimed == False:
                    tomaAirDrop = datas.get('tomaAirDrop')
                    amount = tomaAirDrop.get('amount')
                    status = tomaAirDrop.get('status')
                    print_timestamp(f"Claiming Round {name}")
                    self.toma_claim(token, name)
                else:
                    print_timestamp(f"Season Reward Claimed Done")




    def check_elig(self, token, query):
        self.headers.update({
            'Authorization': token
        })
        payload = {"language_code":"en","init_data":query,"round":"One"}
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/check'
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                datas = data.get('data', {})
                tomaAirDrop = datas.get('tomaAirDrop', {})
                rank = datas.get('rank', 'Not Found')
                amount = tomaAirDrop.get('amount', 0)
                claimed = datas.get('claimed', False)
                print_timestamp(f"tomaAirDrop Amount:{amount}")
                print_timestamp(f"Rank: {rank}")
                if claimed == False:
                    sleep(2)
                    self.toma_claim(token, "One")
    
    def airdrop_task(self, token, query):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/airdropTasks'
        self.headers.update({
            'Authorization': token
        })
        payload = {"language_code":"en","init_data":query,"round":"One"}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                items_data = data.get('data', [])
                for item in items_data[:2]:
                    taskId = item.get('taskId', 0)
                    name = item.get('name','')
                    print_timestamp(f"Open Task {name}")
                    status_ = item.get('status',0)
                    if status_ == 0:
                        sleep(2)
                        self.start_task(token, taskId)
                    elif status_ == 1:
                        sleep(2)
                        self.check_task(token, taskId)
                    elif status_ == 2:
                        sleep(2)
                        self.claim_task(token, taskId)
                    else:
                        print_timestamp(f"Task {name} Done!!")


    def start_task(self, token, id):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/startTask'
        self.headers.update({
            'Authorization': token
        })
        payload = {"task_id": id,"round":"One"}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                datas = data.get('data',None)
                status = datas.get('status')
                print_timestamp('Starting Task')
                if status == 1:
                    sleep(3)
                    self.check_task(token, id)
    
    def check_task(self, token, id):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/checkTask'
        self.headers.update({
            'Authorization': token
        })
        payload = {"task_id": id,"round":"One"}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                datas = data.get('data',None)
                status = datas.get('status')
                print_timestamp('Checked Task')
                if status == 2:
                    sleep(3)
                    self.claim_task(token, id)
                else:
                    print_timestamp('Checked Task Failed')

    def claim_task(self, token, id):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/claimTask'
        self.headers.update({
            'Authorization': token
        })
        payload = {"task_id": id,"round":"One"}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                datas = data.get('data','')
                print_timestamp(f"Claim Task {datas}")
                

    def toma_claim(self, token, round):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/claim'
        self.headers.update({
            'Authorization': token
        })
        payload = {"round":round}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                datas = data.get('data',{})
                tomarketReward = datas.get('tomarketReward')
                print_timestamp(f"{tomarketReward} $TOMA claimed done")

    def puzzle_task(self, token, query):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/puzzle'
        self.headers.update({
            'Authorization': token
        })
        payload = {"language_code":"en","init_data": query}
        response = requests.post(url=url, headers=self.headers, json=payload)
        data = self.response_data(response)
        if data is not None:
            status = data.get('status')
            if status == 0:
                list_data = data.get('data')
                for dats in list_data:
                    taskId = dats.get('taskId')
                    statuss = dats.get('status')
                    star = dats.get('star')
                    games = dats.get('games')
                    score = dats.get('score')
                    if statuss == 0:
                        list_combo = self.get_combo_puzzle()
                        combo = self.find_by_id(list_combo, str(taskId))
                        if combo is not None:
                            payload = {'task_id': taskId, 'code': combo}
                            data_puzzle_claim = self.puzzle_claim(token, payload)
                            if data_puzzle_claim.status_code == 200:
                                jsons = data_puzzle_claim.json()
                                data = jsons.get('data',{})

                                if len(data) == 0:
                                    print_timestamp(f"Puzzle Done, Reward : {star} Star, {games} Tiket Games, {score} Tomato")
                                else:
                                    message = data.get('message','')
                                    print_timestamp(message)

                                        


    def puzzle_claim(self, token, payload):
        url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/puzzleClaim'
        self.headers.update({
            'Authorization': token
        })
        response = requests.post(url=url, headers=self.headers, json=payload)
        return response

    def response_data(self, response):
        if response.status_code >= 500:
            print_timestamp(f"Error {response.status_code}")
            return None
        elif response.status_code >= 400:
            print_timestamp(f"Error {response.status_code} : msg {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()
        else:
            return None
        
    def find_by_id(self, json_data, id):
        for key, value in json_data.items():
            if key == id:
                return value
        return None

