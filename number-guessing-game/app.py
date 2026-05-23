import sys
import random

# Import safety check
try:
    import streamlit as st
except Exception:
    print("Error: 'streamlit' is not installed or could not be imported.")
    print("Please install it using: pip install streamlit")
    print("Then run this app using: streamlit run app.py")
    sys.exit(1)

# Application web page setup
st.title("Number Guessing Game v1.2! 🎮")

# Initialize persistent game variables across webpage refreshes
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.lives = 7
    st.session_state.game_over = False
    st.session_state.feedback = "I am thinking of a number between 1 and 100."
    # NEW CONCEPT: Create an empty list to store the player's guesses
    st.session_state.guess_history = []

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
            value=None, 
            placeholder="Type a number between 1 and 100..."
        )
        submit = st.form_submit_button("Submit Guess")

    if submit:
        if guess is None:
            st.warning("Please enter a number before clicking submit!")
        else:
            # NEW CONCEPT: Use .append() to add the current guess to our list
            st.session_state.guess_history.append(guess)

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

            # Evaluate system loss limits
            if st.session_state.lives <= 0 and not st.session_state.game_over:
                st.session_state.feedback = f"💥 Game Over! The number was {st.session_state.secret_number}."
                st.session_state.game_over = True
                
            st.rerun()

# --- NEW SECTION: DISPLAY GUESS HISTORY USING A LOOP ---
if st.session_state.guess_history:
    st.write("---")
    st.write("### Your Previous Guesses:")
    
    # We use a 'for' loop to print each guess one by one
    for past_guess in st.session_state.guess_history:
        # Check if the past guess was higher, lower, or correct to give a visual clue
        if past_guess < st.session_state.secret_number:
            st.write(f"• {past_guess} (Too Low ⬇️)")
        elif past_guess > st.session_state.secret_number:
            st.write(f"• {past_guess} (Too High ⬆️)")
        else:
            st.write(f"• {past_guess} (Correct! 🎉)")


# Reset environment configuration
if st.session_state.game_over:
    if st.button("Play Again 🔄"):
        del st.session_state.secret_number
        # Make sure to clear the list when restarting the game!
        del st.session_state.guess_history
        st.rerun()
