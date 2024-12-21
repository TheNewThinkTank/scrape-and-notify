
import getpass
# from pprint import pprint as pp
import requests
from bs4 import BeautifulSoup


def scrape_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    event_list = soup.find(class_="tribe-events-loop")
    event_list_items = event_list.find_all("a")
    # find a list of all span elements
    spans = soup.find_all("span", {"class": "tribe-event-date-start"})
    # create a list of lines corresponding to element dates
    startdates = [span.get_text() for span in spans]
    event_names = [
        event.contents[0].strip("\n\t\t").strip("\t") for event in event_list_items
    ]
    event_links = [event.get("href") for event in event_list_items]
    name_date_links = [
        name_date_link
        for name_date_link in zip(event_names, startdates, event_links)
        if name_date_link[0] != "Læs mere »"
    ]
    return name_date_links


# TODO: use https://github.com/TheNewThinkTank/open-courier/blob/main/src/send_email.py
# def send_email(msg, sender_email, password, receiver_email):
#     port = 587  # For starttls
#     smtp_server = "smtp.gmail.com"
#     message = """\
#     Subject: See your coming events

#     {}""".format(
#         msg
#     ).encode(
#         "utf-8"
#     )
#     context = ssl.create_default_context()
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.ehlo()  # Can be omitted
#         server.starttls(context=context)
#         server.ehlo()  # Can be omitted
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)


def main():
    url = "https://dsko.org/kalenderen/"
    msg = scrape_url(url)

    sender_email = input("Type the sender-email and press enter:")
    password = getpass.getpass(prompt="Type your password and press enter:")
    receiver_email = input("Type the receiver-email and press enter:")
    # send_email(msg, sender_email, password, receiver_email)


if __name__ == "__main__":
    main()
