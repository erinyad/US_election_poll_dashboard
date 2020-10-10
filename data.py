from bs4 import BeautifulSoup
import requests


def scrape_poll_data():
    url = 'https://projects.fivethirtyeight.com/polls/president-general/'

    html_data = requests.get(url)
    soup = BeautifulSoup(html_data.content, 'html.parser')

    pollster_data_array = []
    rows = soup.find_all(class_='visible-row')
    for r in rows:
        date = r.find(class_='date-wrapper').text
        pollster = r.find(class_='pollster-container')
        pollster_text = pollster.find_all("a")[-1].text
        sample = r.find(class_='sample').text
        leader = r.find(class_='leader').text
        net = r.find(class_='net').text

        answers = r.find_all(class_='answer')
        values = r.find_all(class_='value')

        if len(values) == 1:
            itr = 2
            while itr > 0:
                next_row = r.findNext("tr")
                value = next_row.find(class_="value")
                answer = next_row.find(class_="answer")

                answers.append(answer)
                values.append(value)
                itr -= 1

        first_person = answers[0].text
        second_person = answers[1].text
        # if len(answers) == 3:
        #     third_person = answers[2]
        first_value = values[0].find(class_="heat-map").text
        second_value = values[1].find(class_="heat-map").text
        # if len(answers) == 3:
        #     third_value = values[2].find(class_="heat-map").text
        pollster_data = {
            "date": date,
            "pollster_name": pollster_text,
            "sample_size": sample,
            "leader": leader,
            "net": net,
            "first_person": first_person,
            "first_value": first_value,
            "second_person": second_person,
            "second_value": second_value
        }
        pollster_data_array.append(pollster_data)
    return pollster_data_array
