import streamlit as st


# =========================================================
# CRC CALCULATION FUNCTION
# =========================================================

def calculate_crc(data, generator):
    data = list(data)
    generator = list(generator)

    # Append zeros according to generator degree
    data.extend(["0"] * (len(generator) - 1))

    # Modulo-2 division using XOR
    for i in range(len(data) - len(generator) + 1):

        if data[i] == "1":

            for j in range(len(generator)):

                data[i + j] = str(
                    int(data[i + j]) ^ int(generator[j])
                )

    # CRC remainder
    crc = "".join(
        data[-(len(generator) - 1):]
    )

    return crc


# =========================================================
# TEXT TO BINARY
# =========================================================

def text_to_binary(text):
    return "".join(
        format(byte, "08b")
        for byte in text.encode("utf-8")
    )


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hospital Report Validator",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ CRC Configuration")


# =========================================================
# CRC ALGORITHM SELECTION
# =========================================================

algorithm = st.sidebar.selectbox(
    "Select Algorithm",
    [
        "CRC-4",
        "CRC-8",
        "CRC-16",
        "CRC-32"
    ]
)


# =========================================================
# DEFAULT GENERATOR POLYNOMIALS
# =========================================================

generators = {

    # x^4 + x + 1
    "CRC-4": "10011",

    # x^8 + x^2 + x + 1
    "CRC-8": "100000111",

    # CRC-16-IBM / ARC polynomial
    # x^16 + x^15 + x^2 + 1
    "CRC-16": "11000000000000101",

    # CRC-32 IEEE 802.3 polynomial
    # x^32 + x^26 + x^23 + x^22 + x^16
    # + x^12 + x^11 + x^10 + x^8 + x^7
    # + x^5 + x^4 + x^2 + x + 1
    "CRC-32": "100000100110000010001110110110111"
}


default_generator = generators[algorithm]


# =========================================================
# EDITABLE GENERATOR POLYNOMIAL
# =========================================================

generator = st.sidebar.text_input(
    "Generator Polynomial",
    value=default_generator
)


# =========================================================
# GENERATOR VALIDATION
# =========================================================

valid_generator = True


if generator == "":

    st.sidebar.warning(
        "Enter a generator polynomial."
    )

    valid_generator = False


elif any(bit not in "01" for bit in generator):

    st.sidebar.error(
        "Generator must contain only 0 and 1."
    )

    valid_generator = False


elif generator[0] != "1":

    st.sidebar.warning(
        "Generator should start with 1."
    )

    valid_generator = False


elif len(generator) < 2:

    st.sidebar.warning(
        "Generator must contain at least 2 bits."
    )

    valid_generator = False


else:

    st.sidebar.success(
        f"Using generator: {generator}"
    )


# =========================================================
# POLYNOMIAL INFORMATION
# =========================================================

if valid_generator:

    crc_length = len(generator) - 1

    st.sidebar.write(
        f"CRC length: **{crc_length} bits**"
    )


st.sidebar.info(
    "The generator polynomial is editable. "
    "You can enter your own polynomial to verify "
    "answers from CRC questions."
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "🏥 Hospital Report Transfer Validator"
)

st.write(
    "CRC-based integrity checking for hospital "
    "laboratory reports."
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📄 Hospital Report",
        "🔢 Binary CRC",
        "📝 Text CRC"
    ]
)


# =========================================================
# TAB 1 - HOSPITAL REPORT
# =========================================================

with tab1:

    st.header("📄 Upload Hospital Report")

    uploaded_file = st.file_uploader(
        "Choose a hospital report",
        type=[
            "xlsx",
            "csv",
            "txt",
            "pdf",
            "docx"
        ]
    )


    if uploaded_file is not None:

        file_data = uploaded_file.getvalue()


        # -------------------------------------------------
        # UPLOAD SUCCESS
        # -------------------------------------------------

        st.success(
            "✅ Report uploaded successfully!"
        )


        # -------------------------------------------------
        # FILE INFORMATION
        # -------------------------------------------------

        col1, col2 = st.columns(2)


        with col1:

            st.write("**File Name**")

            st.write(
                uploaded_file.name
            )


        with col2:

            st.write("**File Size**")

            st.write(
                f"{len(file_data)} bytes"
            )


        st.divider()


        # -------------------------------------------------
        # VALIDATE GENERATOR
        # -------------------------------------------------

        if valid_generator:


            # -------------------------------------------------
            # ERROR SIMULATION
            # -------------------------------------------------

            simulate_error = st.checkbox(
                "⚠️ Simulate error during transfer"
            )


            # -------------------------------------------------
            # VERIFY BUTTON
            # -------------------------------------------------

            if st.button(
                "🔍 Verify Hospital Report",
                type="primary"
            ):


                # =================================================
                # SENDER SIDE
                # =================================================

                file_binary = "".join(
                    format(byte, "08b")
                    for byte in file_data
                )


                sender_crc = calculate_crc(
                    file_binary,
                    generator
                )


                # =================================================
                # SIMULATED TRANSFER
                # =================================================

                if simulate_error:

                    corrupted_data = bytearray(
                        file_data
                    )


                    # Flip one bit

                    if len(corrupted_data) > 100:

                        corrupted_data[100] ^= 1

                    else:

                        corrupted_data[0] ^= 1


                    received_data = bytes(
                        corrupted_data
                    )


                else:

                    received_data = file_data


                # =================================================
                # RECEIVER SIDE
                # =================================================

                received_binary = "".join(
                    format(byte, "08b")
                    for byte in received_data
                )


                receiver_crc = calculate_crc(
                    received_binary,
                    generator
                )


                # =================================================
                # RESULT
                # =================================================

                st.subheader(
                    "🔐 CRC Verification Result"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.write("Sender CRC")

                    st.code(
                        sender_crc,
                        language=None
                    )


                with col2:

                    st.write("Receiver CRC")

                    st.code(
                        receiver_crc,
                        language=None
                    )


                st.divider()


                # =================================================
                # VALIDATION
                # =================================================

                if sender_crc == receiver_crc:

                    st.success(
                        "✅ VALID - No error detected"
                    )

                    st.write(
                        "The sender and receiver CRC values "
                        "match. The report can be accepted."
                    )


                else:

                    st.error(
                        "❌ CORRUPTED - Error detected"
                    )

                    st.write(
                        "The sender and receiver CRC values "
                        "do not match. The report should be rejected."
                    )


        else:

            st.warning(
                "Please enter a valid generator polynomial "
                "before verifying the report."
            )


# =========================================================
# TAB 2 - BINARY CRC
# =========================================================

with tab2:

    st.header("🔢 Binary CRC Calculator")

    st.write(
        f"Calculate {algorithm} for binary data."
    )


    # -------------------------------------------------
    # BINARY INPUT
    # -------------------------------------------------

    binary_data = st.text_input(
        "Enter binary data",
        value="1101011011"
    )


    # -------------------------------------------------
    # CALCULATE BUTTON
    # -------------------------------------------------

    if st.button(
        "Calculate Binary CRC"
    ):


        # -------------------------------------------------
        # VALIDATE BINARY
        # -------------------------------------------------

        valid_binary = (
            binary_data != ""
            and all(
                bit in "01"
                for bit in binary_data
            )
        )


        if not valid_binary:

            st.error(
                "❌ Binary data must contain only 0 and 1."
            )


        elif not valid_generator:

            st.error(
                "❌ Please enter a valid generator polynomial."
            )


        else:

            # -------------------------------------------------
            # CALCULATE CRC
            # -------------------------------------------------

            crc = calculate_crc(
                binary_data,
                generator
            )


            # -------------------------------------------------
            # CODEWORD
            # -------------------------------------------------

            codeword = (
                binary_data + crc
            )


            st.success(
                "✅ CRC calculated successfully!"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Data:** {binary_data}"
                )

                st.write(
                    f"**Generator:** {generator}"
                )


            with col2:

                st.write(
                    f"**{algorithm}:** {crc}"
                )

                st.write(
                    f"**Codeword:** {codeword}"
                )


# =========================================================
# TAB 3 - TEXT CRC
# =========================================================

with tab3:

    st.header("📝 Text CRC Calculator")

    st.write(
        f"Convert text into binary and calculate {algorithm}."
    )


    # -------------------------------------------------
    # TEXT INPUT
    # -------------------------------------------------

    text = st.text_input(
        "Enter text",
        value="HELLO"
    )


    # -------------------------------------------------
    # CALCULATE BUTTON
    # -------------------------------------------------

    if st.button(
        "Calculate Text CRC"
    ):


        if not valid_generator:

            st.error(
                "❌ Please enter a valid generator polynomial."
            )


        elif text == "":

            st.warning(
                "Please enter some text."
            )


        else:

            # -------------------------------------------------
            # TEXT TO BINARY
            # -------------------------------------------------

            binary_text = text_to_binary(
                text
            )


            # -------------------------------------------------
            # CRC
            # -------------------------------------------------

            crc = calculate_crc(
                binary_text,
                generator
            )


            st.success(
                "✅ CRC calculated successfully!"
            )


            st.write(
                f"**Text:** {text}"
            )

            st.write(
                f"**Binary:** {binary_text}"
            )

            st.write(
                f"**Generator:** {generator}"
            )

            st.write(
                f"**{algorithm}:** {crc}"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Hospital Report Transfer Validator | "
    "CRC-4 | CRC-8 | CRC-16 | CRC-32 | "
    "OS&CN Product Project"
)