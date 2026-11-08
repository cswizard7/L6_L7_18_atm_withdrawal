def notes_needed(amount):
    return int(amount.replace(',', '')) // 100

def mask_card(card_number):
    groups = card_number.split()
    return "XXXX XXXX XXXX " + groups[3]

def average_withdrawal(amounts_csv):
    amounts = [int(a) for a in amounts_csv.split(',')]
    return sum(amounts) // len(amounts)

def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result)

if __name__ == "__main__":
    main()
