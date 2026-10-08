import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Pincode Information Finder",
    page_icon="📍",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("📍 Pincode Information Finder")

st.write(
    "Enter an Indian 6-digit pincode to get location "
    "and post office details."
)

# -----------------------------
# Pincode Input
# -----------------------------
pincode = st.text_input(
    "Enter Pincode",
    max_chars=6,
    placeholder="Example: 110001"
)

# -----------------------------
# Search Button
# -----------------------------
if st.button("🔍 Search"):

    # Validate pincode
    if not pincode.isdigit() or len(pincode) != 6:
        st.error("❌ Please enter a valid 6-digit pincode.")

    else:

        url = f"https://api.postalpincode.in/pincode/{pincode}"

        try:
            # -----------------------------
            # Create HTTP Session
            # -----------------------------
            session = requests.Session()

            # Retry connection if temporarily failed
            retry = Retry(
                total=3,
                connect=3,
                read=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"]
            )

            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

            # Browser-like headers
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/155.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json"
            }

            # -----------------------------
            # API Request
            # -----------------------------
            with st.spinner("🔎 Searching pincode..."):

                response = session.get(
                    url,
                    headers=headers,
                    timeout=20
                )

            # Check HTTP status
            response.raise_for_status()

            # Convert response to JSON
            data = response.json()

            # -----------------------------
            # Check API Response
            # -----------------------------
            if not data:
                st.error("❌ Empty response received from the API.")

            elif data[0].get("Status") == "Success":

                offices = data[0].get("PostOffice", [])

                if not offices:
                    st.warning("⚠️ No post office information found.")
                    st.stop()

                # -----------------------------
                # Success Message
                # -----------------------------
                st.success("✅ Pincode found successfully!")

                # First post office
                first_office = offices[0]

                # -----------------------------
                # Location Details
                # -----------------------------
                st.subheader("📍 Location Details")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        "**Pincode:**",
                        first_office.get("Pincode", "N/A")
                    )

                    st.write(
                        "**State:**",
                        first_office.get("State", "N/A")
                    )

                    st.write(
                        "**District:**",
                        first_office.get("District", "N/A")
                    )

                    st.write(
                        "**Region:**",
                        first_office.get("Region", "N/A")
                    )

                with col2:
                    st.write(
                        "**Division:**",
                        first_office.get("Division", "N/A")
                    )

                    st.write(
                        "**Circle:**",
                        first_office.get("Circle", "N/A")
                    )

                    st.write(
                        "**Country:**",
                        first_office.get("Country", "N/A")
                    )

                # -----------------------------
                # Post Offices
                # -----------------------------
                st.subheader("📮 Post Offices")

                for office in offices:

                    office_name = office.get(
                        "Name",
                        "Unknown Post Office"
                    )

                    with st.expander(f"📮 {office_name}"):

                        st.write(
                            "**Name:**",
                            office.get("Name", "N/A")
                        )

                        st.write(
                            "**Branch Type:**",
                            office.get("BranchType", "N/A")
                        )

                        st.write(
                            "**Delivery Status:**",
                            office.get("DeliveryStatus", "N/A")
                        )

                        st.write(
                            "**District:**",
                            office.get("District", "N/A")
                        )

                        st.write(
                            "**Division:**",
                            office.get("Division", "N/A")
                        )

                        st.write(
                            "**Region:**",
                            office.get("Region", "N/A")
                        )

                        st.write(
                            "**Circle:**",
                            office.get("Circle", "N/A")
                        )

            else:
                st.error(
                    f"❌ No information found for pincode {pincode}."
                )

        # -----------------------------
        # Connection Error
        # -----------------------------
        except requests.exceptions.ConnectionError as e:
            st.error(
                "❌ Unable to connect to the Pincode API."
            )
            st.info(
                "Please check your internet connection "
                "or try again later."
            )

        # -----------------------------
        # Timeout Error
        # -----------------------------
        except requests.exceptions.Timeout:
            st.error(
                "⏱️ The API took too long to respond. "
                "Please try again."
            )

        # -----------------------------
        # HTTP Error
        # -----------------------------
        except requests.exceptions.HTTPError as e:
            st.error(
                f"❌ API returned an HTTP error: {e}"
            )

        # -----------------------------
        # JSON Error
        # -----------------------------
        except ValueError:
            st.error(
                "❌ The API returned an invalid response."
            )

        # -----------------------------
        # Other Errors
        # -----------------------------
        except requests.exceptions.RequestException as e:
            st.error(
                f"❌ Something went wrong: {e}"
            )

        except Exception as e:
            st.error(
                f"❌ Unexpected error: {e}"
            )