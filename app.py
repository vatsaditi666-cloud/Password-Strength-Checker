import streamlit as st
import re

st.set_page_config(
    page_title="Password Strength Checker",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Password Strength Checker")
st.write("Check your password strength and improve its security.")

# Common passwords list
COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "iloveyou",
    "abc123",
    "letmein",
    "monkey123"
}

# Password input
password = st.text_input(
    "Enter a sample password",
    type="password",
    placeholder="Type your password here..."
)

if password:

    # Security checks
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter (A-Z)": bool(
            re.search(r"[A-Z]", password)
        ),
        "Lowercase letter (a-z)": bool(
            re.search(r"[a-z]", password)
        ),
        "Contains a number (0-9)": bool(
            re.search(r"\d", password)
        ),
        "Contains a special character": bool(
            re.search(r"[^A-Za-z0-9]", password)
        )
    }

    # Common password detection
    is_common = password.casefold() in COMMON_PASSWORDS

    # Detect repeated and predictable patterns
    has_repeated_chars = bool(
        re.search(r"(.)\1{2,}", password)
    )

    has_sequence = any(
        pattern in password.casefold()
        for pattern in ("1234", "abcd", "qwerty", "1111")
    )

    # Calculate basic score
    score = sum(checks.values())

    # Determine password strength
    if is_common:
        strength = "Weak"
        st.error("🚨 Weak Password: This is a common password.")

    elif has_repeated_chars or has_sequence:
        strength = "Weak"
        st.error(
            "⚠️ Weak Password: A predictable pattern was detected."
        )

    elif score <= 2:
        strength = "Weak"
        st.error("Password Strength: Weak")

    elif score == 3:
        strength = "Medium"
        st.warning("Password Strength: Medium")

    elif score == 4:
        strength = "Strong"
        st.success("Password Strength: Strong")

    else:
        strength = "Very Strong"
        st.success("Password Strength: Very Strong")

    # Strength meter
    st.subheader("📊 Password Analysis")
    st.progress(score / 5)
    st.write(f"Strength result: **{strength}**")
    st.write(f"Security checks passed: {score}/5")

    # Security checklist
    st.subheader("✅ Security Checklist")

    for label, passed in checks.items():
        if passed:
            st.write(f"✅ {label}")
        else:
            st.write(f"❌ {label}")

    # Additional warnings
    if is_common:
        st.warning(
            "This password appears in the app's common-password list. "
            "Choose a unique password."
        )

    if has_repeated_chars:
        st.warning("Avoid repeating the same character many times.")

    if has_sequence:
        st.warning("Avoid predictable sequences such as 1234 or abcd.")

    # Suggestions
    st.subheader("💡 Suggestions")

    tips = []

    if len(password) < 12:
        tips.append("Use a longer password, preferably 12–16+ characters.")

    if not checks["Uppercase letter (A-Z)"]:
        tips.append("Consider adding an uppercase letter.")

    if not checks["Lowercase letter (a-z)"]:
        tips.append("Consider adding a lowercase letter.")

    if not checks["Contains a number (0-9)"]:
        tips.append("Consider adding a number.")

    if not checks["Contains a special character"]:
        tips.append("Consider adding a special character.")

    if is_common:
        tips.append("Never use a common or easily guessed password.")

    if has_repeated_chars or has_sequence:
        tips.append("Avoid repeated characters and predictable patterns.")

    if tips:
        for tip in tips:
            st.write("💡 " + tip)
    else:
        st.write("Good character variety! Keep your password unique.")

else:
    st.info("Enter a sample password to start the analysis.")

st.caption(
    "Educational project: This rule-based score is not a guarantee "
    "of security. Use sample passwords only; this app does not save them."
)