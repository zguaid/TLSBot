# TLSBot

## Description

This bot is designed to help none tech people get a TLS Visa appointment (bots like this one are used by agencies to sell appointments at ridiculous prices (sounds unfair to me).

## Prerequisites

- [Python 3.9](https://www.python.org/downloads/) or higher installed on your system.
- Required packages listed in [requirements.txt](./requirements.txt).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AnwarMEQOR/TLSBot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd TLSBot
    ```

3. Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Create a `.env` file in the root directory of the project.
2. Add the following content to the `.env` file:

    ```plaintext
    center=<center_code>
    email=<your_email>
    password=<your_password>
    useTwilio=True
    account_sid=<your_account_sid>
    auth_token=<your_auth_token>
    phone_number=<your_phone_number>
    twilio_phone_number=<your_twilio_phone_number>
    ```

    - Replace `<center_code>` with the center code (*CAS* for Casablanca, *AGA* for Agadir, *FEZ* for Fez, *RAK* for Marrakech, *OUD* for Oujda, *RBA* for Rabat & *TNG* for Tanger).
    - Replace `<your_email>` with the email associated to your TLS account.
    - Replace `<your_password>` with your password.
    - Replace useTwilio=True with useTwilio=False if you are not planning to use twilio.
    - In case you want to use twilio, replace `<your_account_sid>`, `<your_auth_token>`, `<your_phone_number>`, and `<your_twilio_phone_number>` with your Twilio account information.

3. Run the bot:

    ```bash
    python main.py
    ```

## Contributing

Contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

Use this software at your own risk. The authors and contributors are not responsible for any misuse, damage, or other liabilities arising from the use of this software.

## License

[License](./LICENSE)
