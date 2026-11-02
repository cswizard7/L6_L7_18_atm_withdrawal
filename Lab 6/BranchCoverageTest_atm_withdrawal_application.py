import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------- withdraw ----------

def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account_type():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "fixed", True)


def test_amount_not_multiple_of_100():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_zero_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_negative_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -500, "savings", True)


def test_daily_limit_exceeded():
    assert withdraw(100000, 30000, "savings", True) == "limit exceeded"


def test_amount_equal_to_daily_limit():
    # limit check is strictly greater-than, so exactly 25000 is allowed
    assert withdraw(30000, 25000, "savings", True) == 5000


def test_current_account_higher_limit():
    assert withdraw(60000, 40000, "current", True) == 20000


def test_other_bank_large_amount_fee():
    # other bank: 20 fee + 10 extra since amount > 10000
    assert withdraw(50000, 20000, "current", False) == 29970


def test_other_bank_small_amount_fee():
    # other bank, amount <= 10000: only the 20 fee
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_other_bank_amount_exactly_10000():
    assert withdraw(20000, 10000, "savings", False) == 9980


def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_insufficient_funds_due_to_fee():
    # balance covers the amount but not amount + fee
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_balance_exactly_covers_amount_and_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


# ---------- pin_check ----------

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_card_already_blocked():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_wrong_pin_on_last_attempt():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_correct_pin_on_last_attempt():
    assert pin_check(1234, 1234, 2) == "ok"


def test_wrong_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_wrong_pin_second_attempt_retry():
    assert pin_check(1111, 1234, 1) == "retry"


# ---------- note_breakup ----------

def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)


def test_note_breakup_with_200_notes():
    assert note_breakup(1700) == (3, 1, 0)


def test_note_breakup_without_200_notes():
    assert note_breakup(600) == (1, 0, 1)


def test_note_breakup_with_200_and_100_notes():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_only_500s():
    assert note_breakup(1500) == (3, 0, 0)


def test_note_breakup_zero():
    assert note_breakup(0) == (0, 0, 0)
