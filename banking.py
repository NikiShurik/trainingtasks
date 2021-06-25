# Write your code here
import random
import sqlite3

class Bank():
    name = 'Kulibin Bank'
    IIN = ''
    db_name = 'card.s3db'

    def CreateNewCard(self):
        number = random.randint(0, 999999999)
        number = str(number).zfill(9)
        card_no = self.IIN + number
        temp_1 = list(card_no)
        tmp1 = 0  # will be summ
        for i in range(len(temp_1)):
            if ((i + 1) % 2) != 0:
                tmp2 = int(temp_1[i]) * 2
                # print(int(temp_1[i]))
            else:
                tmp2 = int(temp_1[i])
                # print(int(temp_1[i]))
            if tmp2 > 9:
                tmp2 = tmp2 - 9
            tmp1 += tmp2
            # print(tmp1, tmp2)
        if (tmp1 % 10) != 0:
            cs = str(10 - (tmp1 % 10))
        else:
            cs = '0'
        card_no = card_no + cs
        PIN = str(random.randint(0000, 9999)).zfill(4)
        return [card_no, PIN]

    def last_id_init(self):
        cur.execute("SELECT max(id) FROM card;")
        answer = ''
        answer = str(cur.fetchone()).strip('()')
        ans_list = answer.split(',')
        if ans_list[0] == 'None':
            self.last_id = 1
        else:
            self.last_id = int(ans_list[0]) + 1

    def accountCreate(self):
        accountrecord = {
            'Card': '',
            'PIN': '',
            'Balance': 0,
        }
        self.last_id_init()
        card_info = self.CreateNewCard()
        accountrecord['Card'] = card_info[0]
        accountrecord['PIN'] = card_info[1]
        cur.execute(f"INSERT INTO card VALUES ({self.last_id}, {accountrecord['Card']}, {accountrecord['PIN']}, {accountrecord['Balance']});")
        conn.commit()
        print(f"Your card has been created\nYour card number:\n{accountrecord['Card']}\n"
              f"Your card PIN:\n{accountrecord['PIN']}")

    def user_validate(self, card_no, pin):
        cur.execute(f'SELECT pin FROM card WHERE number={card_no};')
        answer = str(cur.fetchone()).strip('()')
        ans_list = answer.split(',')
        ans_list[0] = ans_list[0].strip("'")
        ans_list[0] = str(ans_list[0]).zfill(4)
        print(ans_list[0], ' ', pin)
        if pin == ans_list[0]:
            uservalidated = True
            #print(pin == ans_list[0])
        else:
            uservalidated = False
        return uservalidated

    def account_state_check(self, card_no):
        cur.execute(f'SELECT balance FROM card WHERE number={card_no};')
        answer = str(cur.fetchone()).strip('()')
        ans_list = answer.split(',')
        #print(ans_list)
        print(f'Balance: {ans_list[0]}')

    def add_income(self, card_no, value):
        cur.execute(f'SELECT balance FROM card WHERE number={card_no};')
        answer = str(cur.fetchone()).strip('()')
        ans_list = answer.split(',')
        cur.execute(f'UPDATE card SET balance={int(ans_list[0]) + int(value)} WHERE number={card_no};')
        conn.commit()
        print('Income was added!')
        pass

    def card_check(self, card_no):
        card_no_state = 0
        # 0 - card num right, card persist in db
        # 1 - wrong num
        # 2 - card num right, there is no such card in db
        # step 1 - check card num
        temp_1 = list(card_no)
        tmp1 = 0  # will be summ
        for i in range(len(temp_1) - 1):
            if ((i + 1) % 2) != 0:
                tmp2 = int(temp_1[i]) * 2
                # print(int(temp_1[i]))
            else:
                tmp2 = int(temp_1[i])
                # print(int(temp_1[i]))
            if tmp2 > 9:
                tmp2 = tmp2 - 9
            tmp1 += tmp2
            # print(tmp1, tmp2)
        if (tmp1 % 10) != 0:
            cs = str(10 - (tmp1 % 10))
        else:
            cs = '0'
        if cs != temp_1[len(temp_1)-1]:
            card_no_state = 1
            return card_no_state
        else:
            cur.execute(f'SELECT id FROM card WHERE number={card_no};')
            answer = str(cur.fetchone()).strip('()')
            ans_list = answer.split(',')
            if str(ans_list[0]) == 'None':
                card_no_state = 2
                return card_no_state
            else:
                card_no_state = 0
                return card_no_state


    def do_transfer(self, s_card, t_card, summ):
        cur.execute(f'SELECT balance FROM card WHERE number={s_card};')
        answer = str(cur.fetchone()).strip('()')
        ans_list = answer.split(',')
        if int(ans_list[0]) < int(summ) :
            print('Not enough money!')
            return
        else:
            cur.execute(f'SELECT balance FROM card WHERE number={s_card};')
            answer = str(cur.fetchone()).strip('()')
            ans_list = answer.split(',')
            cur.execute(f'UPDATE card SET balance={(int(ans_list[0]) - int(summ))} WHERE number={s_card};')
            conn.commit()
            cur.execute(f'SELECT balance FROM card WHERE number={t_card};')
            answer = str(cur.fetchone()).strip('()')
            ans_list = answer.split(',')
            cur.execute(f'UPDATE card SET balance={(int(ans_list[0]) + int(summ))} WHERE number={t_card};')
            conn.commit()
            print('Success!')

    def account_close(self, card_no):
        cur.execute(f'DELETE FROM card WHERE number={card_no};')
        conn.commit()
        print('The account has been closed!')
        return

    def __init__(self):
        self.IIN = '400000'


class Terminal():
    number = ''
    address = ''
    states = ['OnLine', 'LogIn1', 'LogIn2', 'LoggedIn', 'Income1', 'Transfer1', 'Transfer2', 'OffLine']
    state = ''
    display_messages = {
        'OnLine': '1. Create an account\n2. Log into account\n0. Exit\n',
        'OffLine': 'Bye!',
        'LogIn1': 'Enter your card number',
        'LogIn2': 'Enter your PIN',
        'Income1': 'Enter income:',
        'Transfer1': 'Enter card number:',
        'Transfer2': 'Enter how much money you want to transfer:',
        'LoggedIn': '1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit'
    }
    display_message = ''
    currentUserId = {
        'card': '',
        'pass': '',
        'loggedIn': False,
    }
    t_target = {
        'card': '',
        'summ': '',
    }

    # here will be realized main part of interface
    def interface_proc(self, querry = ''):
        if self.state == 'OnLine':
            if querry == '1':
                # self.display_message = 'We will create account'
                # print(self.display_message)
                bs.accountCreate()
                self.state = 'OnLine'
            elif querry == '2':
                self.state = 'LogIn1'
            elif querry == '0':
                self.state = 'OffLine'
        elif self.state == 'LogIn1':
            self.currentUserId['card'] = querry
            self.state = 'LogIn2'
        elif self.state == 'LogIn2':
            self.currentUserId['pass'] = querry
            # then we will login
            self.currentUserId['loggedIn'] = bs.user_validate(self.currentUserId['card'], self.currentUserId['pass'])
            # print(f"Message - {self.currentUserId['loggedIn']}")
            if self.currentUserId['loggedIn']:
                self.display_message = 'You have successfully logged in!'
                print(self.display_message)
                self.state = 'LoggedIn'
            else:
                self.display_message = 'Wrong card number or PIN!'
                print(self.display_message)
                self.state = 'OnLine'
        elif self.state == 'LoggedIn':
            if querry == '1':
                #self.display_message = 'We will show account state'
                #print(self.display_message)
                bs.account_state_check(self.currentUserId['card'])
                self.state = 'LoggedIn'
            elif querry == '2':
                # update value of balance
                # so print message and go out with state 'income1'
                self.state = 'Income1'
                # we must take data from user by input
                # so - go out from interface routine to input
            elif querry == '3':
                self.state = 'Transfer1'
            elif querry == '4':
                bs.account_close(self.currentUserId['card'])
                self.currentUserId['card'] = ''
                self.currentUserId['pass'] = ''
                self.currentUserId['loggedIn'] = False
                self.state = 'OnLine'
                pass
            elif querry == '5':
                self.display_message = 'You have successfully logged out!\n'
                self.currentUserId['card'] = ''
                self.currentUserId['pass'] = ''
                self.currentUserId['loggedIn'] = False
                print(self.display_message)
                self.state = 'OnLine'
            elif querry == '0':
                self.state = 'OffLine'
        elif self.state == 'Income1':
            bs.add_income(self.currentUserId['card'], querry)
            self.state = 'LoggedIn'
        elif self.state == 'Transfer1':
            result = bs.card_check(querry)
            if result == 0:
                self.state = 'Transfer2'
                self.t_target['card'] = querry
            elif result == 1:
                print('Probably you made a mistake in the card number. \nPlease try again!')
                self.state = 'LoggedIn'
            else:
                print('Such a card does not exist.')
                self.state = 'LoggedIn'
        elif self.state == 'Transfer2':
            self.t_target['summ'] = querry
            bs.do_transfer(self.currentUserId['card'], self.t_target['card'], self.t_target['summ'])
            self.state = 'LoggedIn'

        self.display_message = self.display_messages[self.state]

    def __init__(self, address, number):
        self.number = number
        self.address = address
        self.state = 'OnLine'
        self.display_message = self.display_messages[self.state]


bs = Bank()
conn = sqlite3.connect(bs.db_name)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()
terminal = Terminal('Mars', '0001')
print(terminal.display_message)
while terminal.state != 'OffLine':
    querry = input()
    terminal.interface_proc(querry)
    print(terminal.display_message)
