def _parse_amount(text):
    """Convert a string of plain ASCII digits to a positive int, else None."""
    text = text.strip()
    # isascii() rejects Unicode digits like '٣' or '²' that isdigit() allows
    if not text or not text.isascii() or not text.isdigit():
        return None
    try:
        value = int(text)
    except ValueError:  # e.g. digit strings longer than Python's int limit
        return None
    return value if value > 0 else None


def notes_needed(amount):
    if not isinstance(amount, str):
        return None
    value = _parse_amount(amount.replace(',', ''))
    if value is None or value % 100 != 0:
        return None
    return value // 100


def mask_card(card_number):
    if not isinstance(card_number, str):
        return None
    groups = card_number.split()
    if len(groups) != 4:
        return None
    for group in groups:
        if len(group) != 4 or not group.isascii() or not group.isdigit():
            return None
    return "XXXX XXXX XXXX " + groups[3]


def average_withdrawal(amounts_csv):
    if not isinstance(amounts_csv, str):
        return None
    amounts = []
    for part in amounts_csv.split(','):
        value = _parse_amount(part)
        if value is None:
            return None
        amounts.append(value)
    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    if result is None:
        print("Invalid amount: enter a positive multiple of 100")
    else:
        print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    if result is None:
        print("Invalid card number: enter 4 groups of 4 digits")
    else:
        print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    if result is None:
        print("Invalid input: enter positive whole numbers separated by commas")
    else:
        print("Average Withdrawal:", result)

if __name__ == "__main__":
    main()
