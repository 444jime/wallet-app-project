# Multi-Currency Wallet 

A robust multi-layer financial system for real-time currency management. This application was developed as the final project for the **Programming III** course, focusing on a decoupled layered architecture, external API integration, and robust security standards.

## ✨ Key Features

* **Multi-currency Management**: Create and manage separate accounts for different currencies.
* **Real-time Conversion**: Seamless integration with the *CurrencyFreaks API* to fetch live exchange rates.
* **Security First**: Secure user authentication using `bcrypt` for password hashing.
* **Financial Operations**:
    * Deposit funds in ARS.
    * Buy and sell different currencies between your own accounts with instant balance updates.
    * Visual transaction confirmation with safety timeouts.

## 🏗️ Architecture

The project follows a **Multi-layer Architecture** to ensure high maintainability and scalability:

1.  **Presentation Layer (UI)**: Built with **PyQt6**, managing user interactions through a clean, professional interface.
2.  **Business Logic Layer**: Handles transaction verification, currency conversion calculations, and input validation.
3.  **Data Persistence Layer**: Utilizes the **SQLObject ORM** to manage the database schema (Users and Accounts) efficiently.

## 🛠️ Tech Stack

* **Language**: Python
* **GUI Framework**: PyQt6
* **Database / ORM**: SQLObject
* **Security**: Bcrypt & Dotenv
* **API**: CurrencyFreaks (v2.0)

## 🚀 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/444jime/multi-currency-wallet.git](https://github.com/444jime/multi-currency-wallet.git)
    cd multi-currency-wallet
    ```

2.  **Install dependencies**:
    ```bash
    pip install pyqt6 sqlobject bcrypt python-dotenv requests
    ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and define your connection string:
   ```env
   APY_KEY=your_currency_freaks_api_key
   # Example for MySQL:
   DATABASE_CONNECTION=mysql://user:password@localhost/database_name
   # Example for SQLite:
   DATABASE_CONNECTION=sqlite:///path/to/database.db
    ```
   
4.  **Run the application**:
    ```bash
    python main.py
    ```

---
*Developed by Tania as part of her Associate Degree in Systems Analysis.*
