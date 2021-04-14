#!/usr/bin/python

import requests
import os


def main():
    page_size = 500
    basic_auth_credentials = (str(os.environ["SONAR_USER"]), str(os.environ["SONAR_PASS"]))
    sonarqube_url = str(os.environ["SONAR_URL"])
    total_item = int(os.environ["TOTAL_ITEM"])
    blacklist = str(os.environ["BLACKLIST"])
    lines_of_code = 0
    last_page_size = total_item % page_size
    page_count = (total_item - last_page_size) / page_size
    data = []
    for i in range(1, int(page_count + 1)):
        paging_parameters = "&pageSize={page_size}&pageIndex={page_number}".format(page_size=page_size, page_number=i)
        api_url = "{url}/api/components/search?qualifiers=TRK{params}".format(url=sonarqube_url,
                                                                              params=paging_parameters)
        api_response = requests.post(api_url, auth=basic_auth_credentials).json()
        data.append(api_response)
    paging_parameters = "&pageSize={page_size}&pageIndex={page_number}".format(page_size=page_size,
                                                                               page_number=int(page_count) + 1)
    api_url = "{url}/api/components/search?qualifiers=TRK{params}".format(url=sonarqube_url, params=paging_parameters)
    api_response = requests.post(api_url, auth=basic_auth_credentials).json()
    data.append(api_response)
    for item in data:
        for component in item.get("components"):
            # TODO: Use blacklist in here
            if not any(x in component.get("key") for x in ["sample-app", "sample-app-2"]):
                api_url = "{url}/api/measures/component?component={key}&metricKeys=ncloc"\
                    .format(url=sonarqube_url, key=component.get("key"))
                api_response = requests.post(api_url, auth=basic_auth_credentials).json()
                lines_of_code += int(api_response.get("component").get("measures")[0].get("value"))
    print("Total lines of code = ", lines_of_code)


if __name__ == "__main__":
    main()
