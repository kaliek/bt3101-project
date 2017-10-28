from pymongo import MongoClient, errors
class DatabaseHandler:
    DB_IP = '115.66.242.122'
    DB_PORT = 9212
    PROJECT_DATABASE = 'bt3101'
    CRAWL_REQUEST_COLLECTION = 'crawlrequests'
    PROFESSOR_COLLECTION = 'professors'
    UNIVERSITY_COLLECTION = 'universities'

    def __init__(self):
        self.client = MongoClient(self.DB_IP, self.DB_PORT)
        self.db = self.client[self.PROJECT_DATABASE]

    def get_crawl_requests(self):
        return self.db[self.CRAWL_REQUEST_COLLECTION].find(
            {"status": [1, 0, 0, 0]}
        )

    def update_status(self, status, request_id, original_status):
        if status == 'success':
            original_status[1] = 1
            self.db[self.CRAWL_REQUEST_COLLECTION].update(
                {"_id": request_id},
                {
                    '$set': {"status": original_status}
                }
            )
        elif status == 'failure':
            original_status[1] = 2
            self.db[self.CRAWL_REQUEST_COLLECTION].update(
                {"_id": request_id},
                {
                    '$set': {"status": original_status}
                }
            )
        else:
            raise UnknownStatusException

    def get_input(self, request_id, original_status, university_id, professor_ids):
        university_name = self.db[self.UNIVERSITY_COLLECTION].find(
            {"_id": university_id})[0]['name']
        crawler_inputs = []
        for professor_id in professor_ids:
            professor_name = self.db[self.PROFESSOR_COLLECTION].find({"_id": professor_id})[
                0]['name']
            crawler_inputs.append(
                [professor_name, university_name, professor_id, request_id, original_status])
        return crawler_inputs

    def update_professor(self, professor_id, name, promotion_institution, rank, phd_institution, phd_year):
        self.db[self.PROFESSOR_COLLECTION].update(
            {
                "_id": professor_id,
                "name": name
            },
            {
                "$setOnInsert": {
                    "promotionInstitution": promotion_institution,
                    "pdhInstitution": phd_institution,
                    "phdYear": phd_year
                }
            },
            upsert=True
        )
        self.db[self.PROFESSOR_COLLECTION].update(
            {
                "_id": professor_id,
                "name": name,
                "rank": None
            },
            {
                "$set": {
                    "rank": rank
                }
            }
        )


