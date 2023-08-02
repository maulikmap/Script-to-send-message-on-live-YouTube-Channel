from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

g_username = []
g_password = []
min_msgs = int(input("Enter minimum messages to be sent: "))
max_msgs = int(input("Enter maximum messages to be sent: "))
auth_link = r'' # add link to authenticate the code before sending the messages. This link should return true for successful authentication.
gmail_link = r'https://accounts.google.com/v3/signin/identifier?dsh=S-233973616%3A1682542862716442&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AQMjQ7TdV4atQZmHKjRZSUOrUsthgUNchqMru4CvhVstLZS9SnrYDq222ul5vlloX61wUAmdMhMd3A&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
gmail_logout = r'https://accounts.google.com/Logout?hl=en&continue=https://mail.google.com&service=mail&timeStmp=1683881438&secTok=.AG5fkS9VHMkjpHEsxUbVw91FRKUNxZeXHA&ec=GAdAFw&hl=en'
y_link = r'' # Add link of Live Youtube channel here.
msg = ["📉📉💰💰📈📈📉📉💰💰📈📈", "📉💰📈📉💰📈📉💰📈📉💰📈", "📉📉📉💰💰📈📈📉📉💰💰📈📈📈",
       "📉💰💰📈📉💰💰📈📉💰💰📈", "📉📉💰📈📉💰💰💰📉📉💰📈", "📉💰📈📈📉💰💰💰📈📈📉💰📈📈"] # List of various emojis combinations

# set options for headless
options = Options()
options.add_argument('headless')
options.add_argument('window-size=1366x768')
# options.add_argument("download.default_directory=/home/tops/python-scrapping/selenium_chrome/download") # remove comment if you want to run headless browser

# Create the chrome webdriver object
service = Service(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service)  # , options=options)

def g_user_generate():
    with open("email.txt", 'r') as f: # email.txt stores the gmail Username and Password.
        lines = f.readlines()

        i = 1
        for line in lines:
            if i % 2 != 0:
                g_username.append(line.strip())
            else:
                g_password.append(line.strip())
            i = i + 1

    g_user = list(zip(g_username, g_password))
    return g_user

def paste_content(driver, el, content): #It is used to paste emojis into live chatbox of channel
    driver.execute_script(
        f'''
        const text = `{content}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text', text);
        const event = new ClipboardEvent('paste', {{ clipboardData: dataTransfer, bubbles: true}});
        arguments[0].dispatchEvent(event)''',
        el)


def login(e_p): # Automate the gmail Login 

    try:
        # breakpoint()
        print("Trying to login into: " + e_p[0])
        # login page url
        driver.get(gmail_link)

        delay = random.randint(3, 6)
        time.sleep(delay)
        element_username = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id ="identifierId"]')))
        element_username.send_keys(e_p[0])

        delay = random.randint(5, 10)
        element_nextbtn = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierNext"]/div/button')))
        element_nextbtn.send_keys(Keys.ENTER)

        delay = random.randint(3, 6)
        time.sleep(delay)
        element_pass = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        element_pass.send_keys(e_p[1])

        delay = random.randint(5, 10)
        element_login = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="passwordNext"]/div/button')))
        element_login.send_keys(Keys.ENTER)

        # wait the ready state to be complete
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script(
                "return document.readyState === 'complete'")
        )

        print("Login Successful")
        redirect_to_live_channel()

    except Exception as e:
        print('failed to login {}'.format(str(e)))
        return False


def redirect_to_live_channel(): #After login link is redirect to live channel

    time.sleep(random.randint(3, 5))

    try:
        driver.get(y_link)
        time.sleep(random.randint(15, 30))

        i = random.randint(min_msgs, max_msgs)

        while True:
            try:
                delay = random.randint(2, 6)
                time.sleep(delay)
                # element_input_chat = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                #    (By.XPATH, '//div[@id="input" and @class="style-scope yt-live-chat-text-input-field-renderer"]')))\\
                # element_input_chat.send_keys(msg)

                elm = driver.find_element(
                    By.XPATH, '//div[@id="input" and @class="style-scope yt-live-chat-text-input-field-renderer"]')

                msg_i = random.randint(0, 5)
                paste_content(driver, elm, msg[msg_i])

                delay = random.randint(3, 7)
                time.sleep(delay)
                send_btn = driver.find_element(
                    By.XPATH, '//yt-icon-button[@id="button" and @class="style-scope yt-button-renderer style-default size-default"]')
                send_btn.click()

                print("Message number " + str(i) +
                      " (" + msg[msg_i] + " )" + " sent")

                if i == 0:
                    break
                i -= 1
                time.sleep(random.randint(10, 20))

            except Exception as e:
                print('Failed to send message in loop {}'.format(str(e)))
                continue

    except Exception as e:
        print('failed to redirect on live channel page {}'.format(str(e)))
        return False


def main():
    g_users = g_user_generate()
    print("Script is running with below email and password: " +" \n" + '\n'.join(str(i[0]) for i in g_users))
        
    for e_p in g_users:
        driver.get(gmail_logout)
        # call login with email_password(e_p)
        login(e_p)


if __name__ == "__main__":
    while True:
        main()