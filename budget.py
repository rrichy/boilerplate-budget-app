class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def __repr__(self):
        ledger = self.name.center(30, '*')
        for item in self.ledger:
            ledger += '\n{:<23}{:>7}'.format(item['description'][0:23], '{:.2f}'.format(item['amount']))
    
        ledger += '\nTotal: ' + str(sum([a['amount'] for a in self.ledger]))
        return ledger
        

    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -1 * amount, 'description': description})
            self.balance -= amount
            return True
        else: return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to ' + category.name)
            category.deposit(amount, 'Transfer from ' + self.name)
            return True
        else: return False

    def check_funds(self, amount):
        return amount <= self.balance

def create_spend_chart(categories):
    chart = 'Percentage spent by category'

    total_withdrawal = 0.00
    percentage = {}

    for category in categories:
        for transaction in category.ledger:
            if transaction['amount'] < 0:
                percentage[category.name] = percentage.get(category.name, 0) - transaction['amount']
                total_withdrawal -= transaction['amount']
        # percentage[category.name] = round(percentage[category.name], 2)
    # total_withdrawal = round(total_withdrawal, 2)

    lookup = []
    for category, amount in percentage.items():
        lookup.append((category, ((100 * amount / total_withdrawal) // 10) * 10))

    for x in range(100, -1, -10):
        chart += '\n{:>3}|'.format(x)
        for y in range(len(lookup)):
            chart += ' o ' if lookup[y][1] >= x else '   '
        chart += ' '
    chart += '\n    ' + '---'*len(categories) + '-'

    for x in range(max([len(a[0]) for a in lookup])):
        chart += '\n    '
        for y in range(len(lookup)):
            chart += ' {} '.format(lookup[y][0][x]) if x < len(lookup[y][0]) else '   '
        chart += ' '
    
    return chart