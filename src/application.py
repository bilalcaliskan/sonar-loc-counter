#!/usr/bin/python

import math
import requests
import os


def main():
    basic_auth_credentials = (str(os.environ["SONAR_USER"]), str(os.environ["SONAR_PASS"]))
    sonarqube_url = str(os.environ["SONAR_URL"])
    # TODO: Use blacklist while counting lines
    blacklist = str(os.environ["BLACKLIST"])

    api_url = "{url}/api/components/search?qualifiers=TRK".format(url=sonarqube_url)
    api_response = requests.get(api_url, auth=basic_auth_credentials).json()

    total_item = int(api_response.get("paging").get("total"))
    page_size = int(api_response.get("paging").get("pageSize"))

    lines_of_code = 0
    page_count = math.ceil(total_item / page_size)
    data = []
    for i in range(1, page_count + 1):
        if i == page_count:
            page_size = total_item % page_size

        paging_parameters = "&ps={page_size}&p={page_number}".format(page_size=page_size, page_number=i)
        api_url = "{url}/api/components/search?qualifiers=TRK{params}".format(url=sonarqube_url,
                                                                              params=paging_parameters)
        api_response = requests.post(api_url, auth=basic_auth_credentials).json()
        data.append(api_response)

    counter = 0
    for item in data:
        for component in item.get("components"):
            api_url = "{url}/api/measures/component?component={key}&metricKeys=ncloc".format(url=sonarqube_url,
                                                                                             key=component.get("key"))
            api_response = requests.post(api_url, auth=basic_auth_credentials).json()
            print(api_response)
            lines_of_code += int(api_response.get("component").get("measures")[0].get("value"))
            counter = counter + 1

    print("\nTotal number of repos fetched = ", counter)
    print("Total lines of code = ", lines_of_code)


if __name__ == "__main__":
    main()
