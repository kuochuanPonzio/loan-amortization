from dataclasses import dataclass
import math

@dataclass
class Group:
  id: str
  principal: float
  rate: float
  nper: int
  installment: float
  interest: float = 0

@dataclass
class Record:
  group_id: str
  principal: float
  interest: float
  payment: float

OUTPUT_FILE = "payments.csv"
TOTAL_MONTHLY_PAYMENT = 1950
GROUPS = [
  Group('fg', principal=13369.94, rate=.0379, nper=91, installment=178),
  Group('de', principal=7340.87, rate=.0399, nper=80, installment=112),
  Group('hi', principal=16756.24, rate=.0499, nper=100, installment=209), 
  Group('abc', 26670.61, .059, 113, 354)
  ]

def calcInterest(g: Group):
  g.interest = (g.rate/12)*g.principal


def pay(g: Group, payment: float):
  g.principal -= (payment-g.interest)

def payAllGroups(list_of_groups, total_monthly_payment):
  records = []
  for i in list_of_groups:
    i : Group
    calcInterest(i)

    p = min(i.installment, i.interest+i.principal)
    pay(i, p)
    total_monthly_payment-=p
    records.append(Record(group_id=i.id, principal=i.principal, interest=i.interest, payment=p))
  
  i = len(list_of_groups)-1
  while(total_monthly_payment>0 and list_of_groups[0].principal > 0):
    g: Group = list_of_groups[i]
    if(len(list_of_groups)==1 and g.principal > total_monthly_payment):
      p = total_monthly_payment
    else:
      p = min(total_monthly_payment, g.principal)

    g.principal -= p
    total_monthly_payment-=p
    records[i].principal -= p
    records[i].payment += p
    i-=1

  return records

if __name__ == "__main__":
  of = open(OUTPUT_FILE, "w")

  month = 1
  groups = GROUPS
  of.write("Month")
  for i in range(0, len(groups)):
    of.write(",Group,Outstanding Interest,Payment,Resulting Principal")
  of.write("\n")

  #every month until all groups are paid in full
  while len(groups) > 0:
    total_monthly_payment = TOTAL_MONTHLY_PAYMENT

    of.write(str(month)+",")
    month+=1

    records = payAllGroups(groups, total_monthly_payment)
    for r in records:
      r :Record
      of.write(str(r.group_id)+ ','+
               str(round(r.interest, 2))+','+ 
               str(round(r.payment, 2))+ ','+ 
               str(round(r.principal,2))+','
               )
    of.write('\n')
    #each group
    if groups[-1].principal <= 0:
      groups.pop(-1)

  of.close()



