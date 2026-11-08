from hypothesis import given, strategies as st
from atm_withdrawal import notes_needed, mask_card, average_withdrawal

@given(st.text() | st.none())
def test_notes_needed_no_crash(s):

@given(st.text() | st.none())
def test_mask_card_no_crash(s):

@given(st.text() | st.none())
def test_average_withdrawal_no_crash(s):
