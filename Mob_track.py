import time
import smtplib
from email.mime.text import MIMEText
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def send_email_notification(sender_email, receiver_email, password, smtp_server, smtp_port, imei):
    msg = MIMEText(f"IMEI {imei} has been detected.")
    msg['Subject'] = 'IMEI Tracking Alert'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def check_imei_in_log(log_file, target_imei, email_config):
    with open(log_file, 'r') as file:
        for line in file:
            if target_imei in line:
                send_email_notification(**email_config, imei=target_imei)
                print(f"{Fore.RED}Alert: IMEI {target_imei} detected.")
                break


def monitor_imei(log_file, target_imei, check_interval, email_config):
    while True:
        check_imei_in_log(log_file, target_imei, email_config)
        time.sleep(check_interval)


def get_user_input():
    print(f"{Fore.GREEN}{Style.BRIGHT}Mobile Tracking System")
    print(f"{Fore.YELLOW}Please provide the following details:")

    log_file_path = input(f"{Fore.CYAN}Enter the path to the log file: ")
    target_imei = input(f"{Fore.CYAN}Enter the target IMEI number: ")
    check_interval = int(input(f"{Fore.CYAN}Enter the check interval in seconds: "))

    sender_email = input(f"{Fore.CYAN}Enter the sender email address: ")
    receiver_email = input(f"{Fore.CYAN}Enter the receiver email address: ")
    password = input(f"{Fore.CYAN}Enter the sender email password: ")
    smtp_server = input(f"{Fore.CYAN}Enter the SMTP server address: ")
    smtp_port = int(input(f"{Fore.CYAN}Enter the SMTP server port: "))

    email_config = {
        'sender_email': sender_email,
        'receiver_email': receiver_email,
        'password': password,
        'smtp_server': smtp_server,
        'smtp_port': smtp_port
    }

    return log_file_path, target_imei, check_interval, email_config


if __name__ == "__main__":
    log_file_path, target_imei, check_interval, email_config = get_user_input()
    monitor_imei(log_file_path, target_imei, check_interval, email_config)
