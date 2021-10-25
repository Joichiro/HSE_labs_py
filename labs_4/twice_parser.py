from bs4 import BeautifulSoup
import requests, re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
}


def get_request():
    return requests.get("https://elibrary.ru/rubrics.asp", headers=headers).text


def regular_parser():
    html_doc = get_request()
    search_pattern = re.compile('<tr align=center valign=top bgcolor=#eeeeee>.*</tr>', flags=re.DOTALL)
    result = re.findall(search_pattern, html_doc)
    code, rubric, number = None, None, None
    data = []
    for el in result[0].split('\n'):
        code_match = re.match('\d{2}', el)
        if code_match is not None:
            code = str(code_match.group(0)) + ".00.00"
        rubric_match = re.match('[^<].*</b>', el)
        if rubric_match is not None:
            rubric = rubric_match.group(0).split("</b>")[0]
        number_match = re.match('[<].*>\d{2,5}', el)
        if number_match is not None:
            number = number_match.group(0).split('>')[-1]
            if code is None or rubric is None:
                continue
            else:
                data.append([code, rubric, number])
    return data


def bs_parser():
    soup = BeautifulSoup(get_request(), 'html.parser')
    main_table = soup.find("table", {"id": "restab"})
    all_rows = main_table.find_all("tr")
    DATA = []
    for row in all_rows:
        try:
            columns = row.find_all("td")
            code = columns[0].b.text.split('\n')[1]
            rubric = columns[1].a.b.text.split('\n')[1]
            number = columns[2].text
            DATA.append([code, rubric, number])
        except:
            pass
    return DATA
