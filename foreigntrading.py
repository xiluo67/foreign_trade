from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

def send_email(subject, body, to_email):
    smtp_server = 'smtp.163.com'
    smtp_port = 465
    smtp_username = '18813080703@163.com'
    smtp_password = 'CTXUUXYIFOUHIYIJ'  # Ensure this is your correct password

    from_email = smtp_username

    # Create the email
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'html'))

    try:
        # Connect to the server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
            print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the SMTP server. Check your email and password.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Set up the Selenium WebDriver for Firefox
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# URL of the ICBC foreign currency exchange rates page
url = "https://www.icbc.com.cn/ICBC/EN/FinancialInformation/ForeignExchangeRates/RMBExchangeSpotRates/"
driver.get(url)

# Wait for the table to be fully loaded
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'el-table__body'))
)

# Wait for a bit more to ensure all dynamic content is loaded
time.sleep(5)  # Increase if necessary

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
# Locate the correct table
table = soup.find('table', class_='el-table__body')
if table: 
    # Extract the rows and columns if you find the data in the HTML
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 4:  # Ensure there are enough columns
            currency = cells[0].text.strip()
            buy_rate = cells[1].text.strip()
            sell_rate = cells[3].text.strip()  # Adjust index if necessary
            local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Currency: {currency}, Sell Rate: {buy_rate}, Buy Rate: {sell_rate}, Time: {local_time}")
            if currency == 'CAD' and float(buy_rate.replace(',', '')) > 522.5:
                print(float(buy_rate.replace(',', '')))
                send_email(
                subject="Time to Sell CAD!!",
                body = (
                        f"""
                        <html>
                        <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                color: #333;
                                line-height: 1.6;
                                margin: 20px;
                            }}
                            h1 {{
                                color: #0044cc;
                            }}
                            .container {{
                                border: 1px solid #ddd;
                                padding: 20px;
                                border-radius: 5px;
                                background-color: #f9f9f9;
                            }}
                            .footer {{
                                margin-top: 20px;
                                font-size: 0.9em;
                                color: #777;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>CAD Sell Rate Information</h1>
                            <p>Dear Rosie,</p>
                            <p>I hope this message finds you well.</p>
                            <p>I would like to inform you that the current CAD sell rate is: <strong>{buy_rate}</strong>.</p>
                            <p>The local time is: <strong>{local_time}</strong>.</p>
                            <p class="footer">Data collected from ICBC<br>All the best luck,<br><br>Minibot X</p>
                        </div>
                    </body>
                    </html>
                    """
                ),to_email="xiluorosie67@gmail.com")
else:
    print("Table not found.")