from requests_html import HTMLSession
import chompjs
import pandas as pd

# s = HTMLSession()


def find_last_page():
    r = s.get('http://www.nepalstock.com/main/floorsheet/index/1/?contract-no=&stock-symbol=&buyer=&seller=&_limit=500')
    last_page_no = r.html.find(
        '#home-contents > table > tr:nth-child(503) > td > div > a:nth-child(1)',
        first=True).text
    return int(last_page_no.split('/')[-1])


def get_results_from_a_page(page_no):
    url = f'http://www.nepalstock.com/main/floorsheet/index/{page_no}/?contract-no=&stock-symbol=&buyer=&seller=&_limit=500'
    r = s.get(url)
    results = r.html.find('.table.my-table > tr')
    length = len(results)-3
    return_list = []
    for counter, rows in enumerate(results):
        if counter >= 2 and counter < length:
            this_dict = {}
            this_dict['contract_no'] = rows.find('td:nth-child(2)')[0].text
            this_dict['company_name'] = rows.find('td:nth-child(3)')[0].text
            this_dict['buyer'] = rows.find('td:nth-child(4)')[0].text
            this_dict['seller'] = rows.find('td:nth-child(5)')[0].text
            this_dict['quantity'] = rows.find('td:nth-child(6)')[0].text
            this_dict['rate'] = rows.find('td:nth-child(7)')[0].text
            this_dict['total'] = rows.find('td:nth-child(8)')[0].text
            return_list.append(this_dict)
    print(len(return_list))
    return return_list


def main():
    last_page = find_last_page()

    final_output = []

    # final_output = get_results_from_a_page(1)
    # final_output2 = get_results_from_a_page(1)
    # final_output.extend(final_output2)
    # return final_output

    # final_results = [final_output.append(get_results_from_a_page(
    #     url_val)) for url_val in range(1, last_page+1)]

    [final_output.extend(get_results_from_a_page(
        url_val)) for url_val in range(1, 4)]
    print("final results", final_output[0:5])
    print("Total Length", len(final_output))
    print("this is it", final_output[0])
    return final_output


if __name__ == "__main__":
    s = HTMLSession()
    df = pd.DataFrame(main())
    print("Dataframe", df.head())
    df.to_csv('floorsheet.csv', index=False)
    print('finished')
