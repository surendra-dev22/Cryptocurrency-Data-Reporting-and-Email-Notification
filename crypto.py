import os
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders
import requests
from datetime import datetime
import pandas as pd
import schedule
import time
from dotenv import load_dotenv

def send_mail(subject, body, filename):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    load_dotenv()
    sender_mail = os.getenv('SENDER_EMAIL')
    receiver_mail = os.getenv('RECEIVER_EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] = receiver_mail
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'html'))  # Change content type to 'html'

    # Attach the file
    with open(filename, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        message.attach(part)

    try:
        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_mail, email_password)
            server.sendmail(sender_mail, receiver_mail, message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f'Unable to send mail: {e}')


def get_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    param = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1
    }

    # Sending requests
    response = requests.get(url, params=param)

    if response.status_code == 200:
        print('Connection Successful! \nGetting the data...')

        # Storing the response into data
        data = response.json()
        df = pd.DataFrame(data)

        df = df[[
            'id', 'current_price', 'market_cap', 'price_change_percentage_24h',
            'high_24h', 'low_24h', 'ath', 'atl', ]]

        today = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
        df['time_stamp'] = today

        top_negative_10 = df.nsmallest(10, 'price_change_percentage_24h')
        top_positive_10 = df.nlargest(10, 'price_change_percentage_24h')

        # Convert the DataFrames to HTML tables
        top_positive_10_html = top_positive_10.to_html(index=False)
        top_negative_10_html = top_negative_10.to_html(index=False)

        file_name = f'crypto_data_{today}.csv'
        df.to_csv(file_name, index=False)
        print(f"Data saved successfully as {file_name}")

        subject = f"Top 10 crypto currency data to invest for {today}"

        body = f"""
                <html>
                <body>
                    <p>Good Morning!</p>
                    <p>Your crypto reports are here!</p>

                    <h3>Top 10 crypto with the highest price increase in the last 24 hours:</h3>
                    {top_positive_10_html}  <!-- Insert the HTML table for top positive cryptos -->

                    <h3>Top 10 crypto with the highest price decrease in the last 24 hours:</h3>
                    {top_negative_10_html}  <!-- Insert the HTML table for top negative cryptos -->

                    <p>Attached is the 250+ crypto currency latest report.</p>

                    <p>Regards!</p>
                    <p>See you tomorrow!</p>
                    <p>Your Crypto Python Application</p>
                </body>
                </html>
                """

        # Sending the email
        send_mail(subject, body, file_name)
    else:
        print(f"Connection Failed! Error Code {response.status_code}")


if __name__ == '__main__':
    schedule.every().day.at('18:01').do(get_crypto_data)

    while True:
        schedule.run_pending()
        time.sleep(60)
