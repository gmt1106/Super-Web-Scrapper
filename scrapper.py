import requests 
from bs4 import BeautifulSoup
from bs4 import NavigableString



def extract_pages(url):

  html = requests.get(url)

  soup = BeautifulSoup(html.text, "html.parser") 

  pagination = soup.find("div", {"class":"s-pagination"})

  if not pagination:
    return 1

  pages = pagination.find_all("a")  

  #get the second last element in the list
  last_page = pages[-2].get_text(strip = True)
  
  return int(last_page)



def extract_job_data(soup):

  job_title = soup.find("a", {"class" : "s-link"})["title"]
  
  company, location = soup.find("h3", {"class" : "fc-black-700"}).find_all("span", recursive = False)
  company = company.get_text(strip=True).replace("via", " ")
  location = location.get_text(strip=True)

  job_id = soup["data-jobid"]

  return {"title" : job_title, "company" : company, "location" : location, "link" : f"https://stackoverflow.com/jobs/{job_id}"}



def extract_so_jobs(word):

  url = f"https://stackoverflow.com/jobs?q={word}&sort=i"

  last_page = extract_pages(url)

  job_dicts = []

  for page in range(last_page):
    page_html = requests.get(f"{url}&pg={page + 1}")
    page_soup = BeautifulSoup(page_html.text, "html.parser")
    jobs = page_soup.find_all("div", {"class":"-job"})
    print(f"scrapping page:{page}")

    for job in jobs:
      job_dicts.append(extract_job_data(job))

  return job_dicts

    


  




    





                        
