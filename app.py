import streamlit as st
import pandas as pd

# Initialize session state for cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stTextInput, .stSelectbox, .stNumberInput, .stButton {
            border-radius: 10px;
            padding: 8px;
        }
        .product-card {
            border-radius: 10px;
            background-color: white;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        img {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Page Navigation
st.sidebar.title("🛍 Cosmetics Store")
page = st.sidebar.radio("Go to", ["Home", "Cart", "Order", "Contact"])

# Sample cosmetics data
cosmetics_data = [
    {"Name": "Lipstick", "Category": "Makeup", "Price": 500, "Stock": 50, "Image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6WYah9LEDunOcyySFRy2w7kYxtdIJdrXhug&s"},
    {"Name": "Foundation", "Category": "Makeup", "Price": 1200, "Stock": 40, "Image": "data:image/jpeg;base64,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"},
    {"Name": "Eyeliner", "Category": "Makeup", "Price": 300, "Stock": 60, "Image": "data:image/png;base64,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"},
    {"Name": "Moisturizer", "Category": "Skincare", "Price": 700, "Stock": 30, "Image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQICXh3orWK8LNqkFuuG0J2tg3_a4SxMo7jTQ&s"},
    {"Name": "Face Wash", "Category": "Skincare", "Price": 400, "Stock": 80, "Image": "data:image/jpeg;base64,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"},
    {"Name": "Perfume", "Category": "Fragrance", "Price": 1500, "Stock": 20, "Image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQltwuoOXw6ChiqPLjoqT7cEP0ffbKeClOvdw&s"},
]

# Convert data to DataFrame
cosmetics_df = pd.DataFrame(cosmetics_data)

if page == "Home":
    st.title("🛒 Beauty____Com")
    st.markdown("Welcome to the **Cosmetics Store**. Search, filter, and add products to your cart effortlessly.")

    # Search bar
    search_query = st.text_input("🔍 Search for a product:").lower()

    # Category selection
    categories = ["All"] + list(cosmetics_df["Category"].unique())
    selected_category = st.selectbox("📂 Select Category:", categories)

    # Filter data
    filtered_df = cosmetics_df[cosmetics_df["Name"].str.lower().str.contains(search_query)]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    # Display products as cards in rows of four
    st.subheader("📋 Available Products")
    cols = st.columns(4)  

    for index, row in filtered_df.iterrows():
        col = cols[index % 4]  
        with col:
            st.image(row["Image"])
            st.markdown(f"""
                <div class='product-card'>
                    <h5>{row['Name']}</h5>
                    <p>Category: {row['Category']}</p>
                    <p>Price: Rs. {row['Price']}</p>
                    <p>Stock: {row['Stock']} available</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Add to Cart", key=f"{row['Name']}_{index}"):
                if row['Name'] in st.session_state.cart:
                    st.session_state.cart[row['Name']] += 1
                else:
                    st.session_state.cart[row['Name']] = {"quantity": 1, "price": row['Price']}
                st.success(f"✅ {row['Name']} added to cart!")

 

# Cart Page
elif page == "Cart":
    st.title("🛒 Your Cart")

    if not st.session_state.cart:
        st.write("Your cart is empty!")
    else:
        total_price = 0
        for item, details in st.session_state.cart.items():
            st.write(f"🛍 {item} - {details['quantity']} pcs x Rs.{details['price']} = Rs.{details['quantity'] * details['price']}")
            total_price += details["quantity"] * details["price"]

        st.subheader(f"💵 Total Price: Rs.{total_price}")

elif page == "Order":
    st.title("📝 Order Page")
    st.markdown("Review and confirm your order.")

    if st.session_state.cart:
        # Convert cart dictionary to DataFrame with price details
        order_df = pd.DataFrame(
            [(name, details["quantity"], details["price"], details["quantity"] * details["price"]) 
             for name, details in st.session_state.cart.items()],
            columns=["Product", "Quantity", "Price per unit", "Total Price"]
        )

        # Display the order summary
        st.dataframe(order_df)

        # Calculate Grand Total
        grand_total = order_df["Total Price"].sum()
        st.subheader(f"💰 Grand Total: Rs.{grand_total}")

        if st.button("Confirm Order"):
            st.success("🎉 Your order has been placed successfully!")
            st.session_state.cart.clear()
    else:
        st.info("No items in the cart to place an order.")


elif page == "Contact":
    st.title("📞 Contact Us")
    st.markdown("For any inquiries, reach out to us!")
    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Your Message")
    if st.button("Submit"):
        st.success("✅ Your message has been sent!")

    