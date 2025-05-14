from dataclasses import dataclass
import parse_VSAC
import datetime
from dateutil.relativedelta import relativedelta
from typing import List

OUTPUT_FILE = "payments.csv"
DELTA = relativedelta(months=1)

@dataclass
class Group:
  id: str
  principal: float
  rate: float
  installment: float
  interest: float

@dataclass
class RecordTotals:
  totalInterest: float
  totalPayment: float
  totalResultingPrincipal: float
  totalInitialPrincipal: float

@dataclass
class Record:
  group_id: str
  initialPrincipal: float
  principal: float
  interest: float
  payment: float
  
def consolidateGroups(groups: List[Group]):
  consolidatedGroupIds = []
  newGroups = []
  for group in groups:
    if group.id not in consolidatedGroupIds:
      likeRateGroups: List[Group] = [g for g in groups if g.rate == group.rate]
      sumPrincipal = 0
      newName = ""
      sumInstallment = 0
      sumInterest = 0
      for lg in likeRateGroups:
        sumPrincipal += lg.principal
        newName += lg.id
        sumInstallment += lg.installment
        sumInterest += lg.interest
        consolidatedGroupIds.append(lg.id)
      newGroups.append(Group(id=newName, principal=sumPrincipal, rate=group.rate, interest=sumInterest, installment=sumInstallment))
  return newGroups
    
def calcRecordTotals(records: List[Record]):
  totalInitialPrincipal = 0
  totalInterest = 0
  totalPayment = 0
  totalResultingPrincipal = 0
  for r in records:
    totalInitialPrincipal += r.initialPrincipal
    totalInterest += r.interest
    totalPayment += r.payment
    totalResultingPrincipal += r.principal
  
  return {
    "totalInitialPrincipal": totalInitialPrincipal,
    "totalInterest": totalInterest,
    "totalPayment": totalPayment,
    "totalResultingPrincipal": totalResultingPrincipal
  }
  
def convertDetailsToGroups(details):
  groups = []
  for det in details:
    groups.append(Group(det['groupId'], principal=det['principal'], rate=det['rate'], interest=det['outstanding interest'], installment=det['installment']))
  return groups

def calcInterest(g: Group):
  g.interest = (g.rate/12)*g.principal

def pay(g: Group, payment: float):
  g.principal -= (payment-g.interest)

def payAllGroups(list_of_groups: List[Group], total_monthly_payment):
  records = []
  
  # this for loop makes the installment payment on every loan group
  for i in list_of_groups:
    intitialPrincipal = i.principal
    calcInterest(i)
    # if the total amount on the loan (principal + interest) is less than the installment, just pay the remaining amount
    p = min(i.installment, i.interest+i.principal)
    pay(i, p)
    total_monthly_payment-=p
    records.append(Record(initialPrincipal=intitialPrincipal, group_id=i.id, principal=i.principal, interest=i.interest, payment=p))
  
  # this while loop spends the rest of the total monthly payment on the loans with the highest rates (the end of the array)
  i = len(list_of_groups)-1
  while(total_monthly_payment>0 and list_of_groups[0].principal > 0):
    g = list_of_groups[i]
    if(len(list_of_groups)==1 and g.principal > total_monthly_payment):
      p = total_monthly_payment
    else:
      p = min(total_monthly_payment, g.principal)

    g.principal -= p # we already paid the interest on this loan so that's why we don't use the pay() function here
    total_monthly_payment-=p
    records[i].principal -= p
    records[i].payment += p
    i-=1

  return records

def getPaymentSchedule():
  paymentSchedule = []
  monthInput = -1
  while monthInput != "":
    month = -1
    amount = -1
    while amount == -1:
      try:
        amount = float(input("Enter monthly payment:\n$"))
      except ValueError:
        print("Invalid input. Please enter a numeric value for payment amount.")
    while month == -1:
      try:
        monthInput = input("Enter duration [default: all remaining months]\nMonths:")
        month = int(monthInput) if monthInput else 1
      except ValueError:
        print("Invalid input. Please enter a numeric value for payment duration.")
    paymentSchedule += [amount]*month
  return paymentSchedule

if __name__ == "__main__":
  of = open(OUTPUT_FILE, "w")
  GROUP_DETAILS = parse_VSAC.parse("vsac.html")
  date = datetime.date.today() + DELTA
  month = 1
  groups = convertDetailsToGroups(GROUP_DETAILS)
  groups = consolidateGroups(groups)
  
  of.write("Date, Initial Balance, Total Principal, Total Interest, Total Payment, Resulting Balance")
  for i in range(0, len(groups)):
    of.write(",Group,Outstanding Interest,Payment,Resulting Principal")
  of.write("\n")
  paymentSchedule = getPaymentSchedule()
  paymentIndex = -1
  #every month until all groups are paid in full
  while len(groups) > 0:
    paymentIndex = min(paymentIndex+1, len(paymentSchedule)-1)
    total_monthly_payment = paymentSchedule[paymentIndex]

    of.write(date.strftime("%m/%d/%Y")+",")
    date += DELTA

    records: List[Record] = payAllGroups(groups, total_monthly_payment)
    recordTotals: RecordTotals = calcRecordTotals(records)
    of.write(
      str(round(recordTotals["totalInitialPrincipal"]+recordTotals["totalInterest"], 2))+','+
      str(round(recordTotals["totalInitialPrincipal"], 2))+','+
      str(round(recordTotals["totalInterest"], 2))+','+
      str(round(recordTotals["totalPayment"], 2))+','+
      str(round(recordTotals["totalResultingPrincipal"], 2))+','
    )
    for r in records:
      of.write(
        str(r.group_id)+ ','+
        str(round(r.interest, 2))+','+ 
        str(round(r.payment, 2))+ ','+ 
        str(round(r.principal,2))+','
      )
    of.write('\n')
    #each group
    if groups[-1].principal <= 0:
      groups.pop(-1)

  of.close()
  finalMonth = (date-DELTA).strftime("%B, %Y")
  print(f"Final payment made in {finalMonth}")



