class Category:
  def __init__(self, category):
      self.category=category
      self.ledger=[]
      self.withdraw_numbers=0
      self.balance=0
      self.long_of_name=len(self.category)
  def deposit(self, amount, description=""):
      self.ledger.append({"amount": amount, "description": description})
      self.balance += amount

  def check_funds(self, amount):
      if self.balance < amount:
          return False
      return True

  def withdraw(self, amount, description=""):
      if self.check_funds(amount):
          self.deposit(-amount,description)
          self.withdraw_numbers -= amount
          return True
      print("not enought founds")
      return False 

  def get_balance(self):
      return self.balance

  def transfer(self, amount, category):

      if self.check_funds(amount):
          self.withdraw(amount, f"Transfer to {category.category}")
          category.deposit(amount,f"Transfer from {self.category}")
          return True

      return False


  def __str__(self):
      title= self.category.center(30).replace(" ","*")+"\n"
      ledger_display=""

      for ledge in self.ledger:


          amount_display = float(ledge["amount"])
          decimals = "{:.2f}"


          spaces= " "*(30-len(ledge["description"][:23:])-len(decimals.format(amount_display)))
          ledger_display += ledge["description"][:23:]+spaces+decimals.format(amount_display)[:7:]+"\n"
          total= "Total: "+ decimals.format(self.balance)
      return title+ledger_display+total

def create_spend_chart(list_of_categoris=[]):
  botom_line="    -"+"-"*len(list_of_categoris)*3+" "



  def calc_porcentajes(cat):
      return int(cat.withdraw_numbers)

  porcentages = [calc_porcentajes(i) for i in list_of_categoris]
  total_porcentages=0

  

  for a in range(len(porcentages)):
      total_porcentages+=porcentages[a]
  graph=""

  for x in range(100,-1,-10):
      graph+=" "*(3-len(str(x)))+str(x)+"| "
      for j in porcentages:
          b=(j*100)/total_porcentages
          if x<b:
              graph += "o"+"  "
          else:
              graph +="   "
          if j==len(porcentages):
              graph +=" "
      if x!=0:    
          graph+="\n"

  categorys_display="     "

  def calc_long(cat):
      return cat.long_of_name

  long = [calc_long(i) for i in list_of_categoris]
  long.sort()

  for y in range(long[-1]):
      for t in range(len(porcentages)):
          try: 
             name=list_of_categoris[t].category
             categorys_display+= name[y]+"  "
          except:
              categorys_display+="   "

          if t==len(porcentages):
            categorys_display+=" "
          
      if y != range(long[-1]):
          categorys_display+="\n     "
        
      else:
        pass
    
  total_graph="Percentage spent by category"+"\n"+graph.rstrip()+"  \n"+botom_line.rstrip()+"\n"+categorys_display.rstrip()+"  "
  return total_graph

food = Category("Food")
food.deposit(2000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)

clothing.withdraw(25.55)
clothing.withdraw(100)

auto = Category("Auto")

auto.deposit(1000, "initial deposit")
auto.withdraw(15) 

home = Category("Home")
home.deposit(1000, "initial deposit")
home.withdraw(10.15, "groceries")
print(food)
print(clothing)
print(auto)
print(create_spend_chart([food, clothing, auto, home]))



food.deposit(900, "deposit")
entertainment=Category("Entertainment")
entertainment.deposit(900, "deposit")
business=Category("Business")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
print(create_spend_chart([business, food, entertainment]))

