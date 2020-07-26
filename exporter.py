import csv 

def save_to_file(jobs):

  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Link"])

  for job in jobs:

    #values() return only values in the directionary in dict_values form 
    writer.writerow(list(job.values()))

  return 