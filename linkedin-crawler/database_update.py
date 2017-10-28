import csv
from database_handler import DatabaseHandler
# read the output file produced by linkedin-crawler.js to database

db_handler = DatabaseHandler()
with open("crawler_outputs.csv", "r") as f:
    outputs = csv.reader(f, delimiter=',')
    next(outputs)
    for output in outputs:
        professor_id = output[8]
        name = output[0]
        promotion_institution = output[2]
        rank = output[1]
        phd_institution = output[4]
        phd_year = output[5]
        db_handler.update_professor(
            professor_id, name, promotion_institution,
            rank, phd_institution, phd_year)
        status = "failure"
        if output[7]:
            status = "success"
        request_id = output[9]
        original_status = output[10]
        db_handler.update_status(status, request_id, original_status)
