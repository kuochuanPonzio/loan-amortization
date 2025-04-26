from bs4 import BeautifulSoup

def parse(fileName):
        
    with open(fileName, "r") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    groupDetails = []

    loanBlocks = soup.find_all(class_ = 'loan-block')
    for l in loanBlocks:
        details = l.find_all(class_ = "details")
        principal = 0
        outsInterest = 0
        rate = 0
        installment = 0
        groupId = ""
        for d in details:
            divs = d.find_all("div")
            for div in divs:
                label = div.find_next(class_ = "detail__title").string
                value = div.find_next(class_ = "detail__value").string
                match label:
                    case "Principal":
                        principal = float(value.replace('$', '').replace(',', ''))
                    case "Outstanding Interest":
                        outsInterest = float(value.replace('$', '').replace(',', ''))
                    case "Weighted Interest Rate":
                        rate = round(float(value.replace('%', ''))/100, 3)
                    case "Group ID":
                        groupId = value
                    case "Installment":
                        installment = float(value.replace('$', '').replace(',', ''))
        
        groupDetails.append({"principal": principal, "outstanding interest": outsInterest, "rate": rate, "groupId": groupId, "installment": installment})

    sortedGroups = sorted(groupDetails, key=lambda det: det["rate"])
    return sortedGroups
