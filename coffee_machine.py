class CoffeeMachine():
    # accessible resources
    app_state = {
        'water': 400,
        'milk': 540,
        'coffee': 120,
        'cups': 9,
        'money': 550,
    }
    state_change = {
        'water': 0,
        'milk': 0,
        'coffee': 0,
        'cups': 0,
        'money': 0,
    }
#    interface_states = ['root', 'root1', 'buy', 'take', 'fill', 'fill1', 'fill2', 'fill3', 'off']  # possible states of machine
    interface_state = 'root'  # current state of machine
    # db record
    prod_db = [
        {'name': 'espresso',
         'water': 250,
         'milk': 0,
         'coffee': 16,
         'cups': 1,
         },
        {'name': 'latte',
         'water': 350,
         'milk': 75,
         'coffee': 20,
         'cups': 1,
         },
        {'name': 'cappuccino',
         'water': 200,
         'milk': 100,
         'coffee': 12,
         'cups': 1,
         }
    ]
    # prices_db -> dict for elements ( str(name) : int(price)
    prices_db = {
        'espresso': 4,
        'latte': 7,
        'cappuccino': 6,
         }
    def __init__(self):
        print('Write action (buy, fill, take, remaining, exit):\n')

    def res_print(self):    # res_print() - print app_state data
        print('The coffee machine has:')
        print(f"{self.app_state['water']} of water")
        print(f"{self.app_state['milk']} of milk")
        print(f"{self.app_state['coffee']} of coffee beans")
        print(f"{self.app_state['cups']} of disposable cups")
        print(f"{self.app_state['money']} of money")
        self.interface_state = 'root'
        print('Write action (buy, fill, take, remaining, exit):\n')
        return

    # prod_make(name) - production make procedure:
    # - find in prod db components for product with name
    # - prepare changes for app_state
    # - change app_state

    def prod_make(self, name):
        state_change = {
            'water': 0,
            'milk': 0,
            'coffee': 0,
            'cups': 0,
            'money': 0,
            }
        for i in range(len(self.prod_db)):
            if self.prod_db[i]['name'] == name:
                for statevar in state_change.keys():
                    if statevar == 'money':
                        state_change['money'] += self.prices_db[name]
                    else:
                        state_change[statevar] -= self.prod_db[i][statevar]
        possible_to_make = 10000
        req_res = ''
        #   print(f'we need {state_change}')
        for key in state_change.keys():
            if key != 'money':
                if state_change[key] != 0:
                     poss = self.app_state[key] // abs(state_change[key])
                     if poss <= possible_to_make:
                          possible_to_make = poss
                     if poss == 0:
                          req_res = key
        if possible_to_make >= 1:
            for statevar in self.app_state.keys():
                self.app_state[statevar] += state_change[statevar]
            print('I have enough resources, making you a coffee!')
        else:
            print(f'Sorry, not enough {req_res}!')
        self.interface_state = 'root'
        print('Write action (buy, fill, take, remaining, exit):\n')
        return

    def sell_proc(self, querry=''):
        if self.interface_state == 'root':
            print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
            self.interface_state = 'buy'
            return
        elif self.interface_state == 'buy':
            if querry == '1':
                self.prod_make('espresso')
            elif querry == '2':
                self.prod_make('latte')
            elif querry == '3':
                self.prod_make('cappuccino')
            elif querry == 'back':
                self.interface_state = 'root'
                print('Write action (buy, fill, take, remaining, exit):\n')
            return
        return

    def fill_proc(self, querry = ''):
        if self.interface_state == 'root':
            print('Write how many ml of water you want to add:\n')
            self.interface_state = 'fill'
            return
        elif self.interface_state == 'fill':
            self.state_change['water'] += int(querry)
            print('Write how many ml of milk you want to add:\n')
            self.interface_state = 'fill1'
            return
        elif self.interface_state == 'fill1':
            self.state_change['milk'] += int(querry)
            print('Write how many grams of coffee beans you want to add:\n')
            self.interface_state = 'fill2'
            return
        elif self.interface_state == 'fill2':
            self.state_change['coffee'] += int(querry)
            print('Write how many disposable coffee cups you want to add:\n')
            self.interface_state = 'fill3'
            return
        elif self.interface_state == 'fill3':
            self.state_change['cups'] += int(querry)
            for statevar in self.app_state.keys():
                self.app_state[statevar] += self.state_change[statevar]
            self.interface_state = 'root'
            print('Write action (buy, fill, take, remaining, exit):\n')
        return

    def take_proc(self):
        print(f"I gave you ${self.app_state['money']}\n")
        self.app_state['money'] -= self.app_state['money']
        self.interface_state = 'root'
        print('Write action (buy, fill, take, remaining, exit):\n')
        return

    def process(self, querry):
        if self.interface_state == 'root':
            if querry == 'buy':
                self.sell_proc()
            elif querry == 'fill':
                self.fill_proc()
            elif querry == 'take':
                self.take_proc()
            elif querry == 'remaining':
                self.res_print()
            elif querry == 'exit':
                self.interface_state = 'off'
            return
        elif self.interface_state == 'buy':
            self.sell_proc(querry)
        elif self.interface_state == 'fill':
            self.fill_proc(querry)
        elif self.interface_state == 'fill1':
            self.fill_proc(querry)
        elif self.interface_state == 'fill2':
            self.fill_proc(querry)
        elif self.interface_state == 'fill3':
            self.fill_proc(querry)
        return

machine=CoffeeMachine()
while machine.interface_state != 'off':
    machine.process(input())
