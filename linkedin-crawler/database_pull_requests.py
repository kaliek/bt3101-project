import csv
from database_handler import *

db_handler = DatabaseHandler()
user_requests = db_handler.get_crawl_requests()
crawler_inputs = []
for user_request in user_requests:
    request_id = user_request['_id']
    university_id = user_request['universityId']
    professor_ids = user_request['professorIds']
    original_status = user_request['status']
    crawler_inputs = db_handler.get_input(
        request_id, original_status, university_id, professor_ids)

if len(crawler_inputs) != 0:
    # write a csv file for linkedin-crawler.js to crawl
    with open("crawler_inputs.csv", "w") as f:
        writer = csv.writer(f)
        # writer.writerow(["professor_name", "university_name", "professor_id", "request_id", "original_status"])
        writer.writerows(crawler_inputs)
