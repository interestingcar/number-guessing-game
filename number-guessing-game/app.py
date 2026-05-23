import sys
import random
from typing import TYPE_CHECKING

# Import Streamlit with a runtime safety check.
try:
    import streamlit as st
except Exception:
    print("Error: 'streamlit' is not installed or could not be imported.")
    print("Please install it using: pip install streamlit")
    print("Then run this app using: streamlit run app.py")
    sys.exit(1)

# Application web page setup
st.title("Number Guessing Game v1.1! 🎮")

# Initialize persistent game variables across webpage refreshes
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.lives = 7
    st.session_state.game_over = False
    st.session_state.feedback = "I am thinking of a number between 1 and 100."

# Display status dashboards
st.write(f"### Lives remaining: {st.session_state.lives}")
st.write(st.session_state.feedback)

# Core game interface loop
if not st.session_state.game_over:
    # Form keeps the layout static until the user submits a selection
    with st.form(key="guess_form", clear_on_submit=True):
        guess = st.number_input(
            "Take a guess:", 
            min_value=1, 
            max_value=100, 
            step=1, 
            value=1,
            placeholder="Type a number between 1 and 100..."
        )
        submit = st.form_submit_button("Submit Guess")

    if submit:
        # Game logic evaluations
        if guess < st.session_state.secret_number:
            st.session_state.lives -= 1
            st.session_state.feedback = "Too low! ⬇️"
        elif guess > st.session_state.secret_number:
            st.session_state.lives -= 1
            st.session_state.feedback = "Too high! ⬆️"
        else:
            st.session_state.feedback = f"🎉 Correct! You won with {st.session_state.lives} lives left!"
            st.session_state.game_over = True

        # If the player has run out of lives, end the game and reveal the number.
        if st.session_state.lives <= 0 and not st.session_state.game_over:
            st.session_state.feedback = f"💥 Game Over! The number was {st.session_state.secret_number}."
            st.session_state.game_over = True

        st.rerun()

# Reset environment configuration
if st.session_state.game_over:
    if st.button("Play Again 🔄"):
        del st.session_state.secret_number
        st.rerun()
