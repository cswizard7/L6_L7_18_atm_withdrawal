from hypothesis import given, strategies as st
from atm_withdrawal import notes_needed, mask_card, average_withdrawal


# ---------- Fuzz tests: random / malformed input must never crash ----------

@given(st.text() | st.none())
def test_notes_needed_no_crash(s):
    try:
        notes_needed(s)
    except Exception as e:
        assert False, f"notes_needed crashed with: {e!r}"


@given(st.text() | st.none())
def test_mask_card_no_crash(s):
    try:
        mask_card(s)
    except Exception as e:
        assert False, f"mask_card crashed with: {e!r}"


@given(st.text() | st.none())
def test_average_withdrawal_no_crash(s):
    try:
        average_withdrawal(s)
    except Exception as e:
        assert False, f"average_withdrawal crashed with: {e!r}"


# ---------- Fuzz tests: crafted inputs that look valid but are not ----------

@given(st.integers())
def test_notes_needed_rejects_bad_amounts(n):
    # Zero, negative amounts and amounts that are not a multiple of 100
    # cannot be paid out in 100 notes, so they must be rejected (None).
    result = notes_needed(str(n))
    if n > 0 and n % 100 == 0:
        assert result == n // 100
    else:
        assert result is None, f"notes_needed({n!r}) returned {result!r}"


@given(st.lists(st.from_regex(r"[0-9]{1,6}", fullmatch=True), min_size=1, max_size=8))
def test_mask_card_only_accepts_four_groups_of_four(groups):
    # Only "dddd dddd dddd dddd" is a valid card number.
    card = " ".join(groups)
    result = mask_card(card)
    if len(groups) == 4 and all(len(g) == 4 for g in groups):
        assert result == "XXXX XXXX XXXX " + groups[3]
    else:
        assert result is None, f"mask_card({card!r}) returned {result!r}"


@given(st.lists(st.integers(min_value=-10**6, max_value=10**6), min_size=1, max_size=10))
def test_average_withdrawal_rejects_non_positive_amounts(amounts):
    # A withdrawal must be a positive amount, so any zero or negative
    # entry makes the whole CSV invalid.
    csv = ",".join(str(a) for a in amounts)
    result = average_withdrawal(csv)
    if all(a > 0 for a in amounts):
        assert result == sum(amounts) // len(amounts)
    else:
        assert result is None, f"average_withdrawal({csv!r}) returned {result!r}"
