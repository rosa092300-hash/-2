import streamlit as st
import math

st.set_page_config(page_title="Multi-Function Calculator", layout="centered")
st.title("Multi-Function Calculator")

st.sidebar.header("Calculator Options")
operation = st.sidebar.selectbox(
    "Select Operation",
    [
        "Arithmetic ( + , - , * , / )",
        "Modular",
        "Exponential",
        "Logarithmic",
    ]
)

st.write("---")

# Show inputs depending on operation so we don't request unnecessary fields
if operation == "Arithmetic ( + , - , * , / )":
    st.subheader("Arithmetic")
    a = st.number_input("Enter first number (a):", value=0.0, format="%f")
    b = st.number_input("Enter second number (b):", value=0.0, format="%f")
    op = st.selectbox("Select arithmetic operator", ["+", "-", "*", "/"]) 
    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            result = a / b
        st.success(f"Result: {result}")
    except ZeroDivisionError:
        st.error("Error: Division by zero is not allowed.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

elif operation == "Modular":
    st.subheader("Modular (remainder)")
    # For modulo it's common to work with integers; give user a choice
    use_ints = st.checkbox("Treat inputs as integers (use floor for floats)", value=True)
    a_raw = st.number_input("Enter dividend (a):", value=0.0, format="%f")
    b_raw = st.number_input("Enter divisor (b):", value=1.0, format="%f")
    try:
        if b_raw == 0:
            raise ZeroDivisionError("Modulo by zero")
        if use_ints:
            a = int(math.floor(a_raw))
            b = int(math.floor(b_raw))
            result = a % b
            st.info(f"Using integers a={a}, b={b}")
        else:
            a = a_raw
            b = b_raw
            result = a % b
        st.success(f"Result: {result}")
    except ZeroDivisionError:
        st.error("Error: Modulo by zero is not allowed.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

elif operation == "Exponential":
    st.subheader("Exponential (a^b)")
    a = st.number_input("Enter base (a):", value=0.0, format="%f")
    b = st.number_input("Enter exponent (b):", value=0.0, format="%f")
    try:
        # Protect against extremely large exponents
        if abs(b) > 1e6:
            st.warning("Exponent magnitude is very large; result may overflow or take long to compute.")
        result = a ** b
        st.success(f"Result: {result}")
    except OverflowError:
        st.error("Error: numerical overflow occurred for a ** b.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

elif operation == "Logarithmic":
    st.subheader("Logarithm")
    a = st.number_input("Enter value (a) (must be > 0):", value=1.0, format="%f")
    base_option = st.selectbox("Base:", ["e (natural)", "10", "custom"])
    if base_option == "custom":
        base = st.number_input("Enter custom base (must be > 0 and ≠ 1):", value=math.e, format="%f")
    elif base_option == "10":
        base = 10.0
    else:
        base = math.e

    try:
        if a <= 0:
            raise ValueError("Logarithm argument must be > 0")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be > 0 and ≠ 1")
        # Use math.log with a single or two arguments
        result = math.log(a, base)
        st.success(f"Result: log base {base} of {a} = {result}")
    except ValueError as ve:
        st.error(f"Error: {ve}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

st.write("---")
st.caption("Calculator supports arithmetic, modular, exponential and logarithmic operations. Use the sidebar to switch modes.")
