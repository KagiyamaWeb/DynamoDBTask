import datetime
import multiprocessing
from typing import List, Dict
import time

def convert_to_dynamodb_documents(user_id: int, 
                                  day: datetime.date, 
                                  activity_scores: List[int]
) -> Dict:

    num_cores = multiprocessing.cpu_count()
    chunk_size = len(activity_scores) // num_cores # Split the activity_scores into chunks for parallel processing

    chunks = [activity_scores[i:i + chunk_size] for i in range(0, len(activity_scores), chunk_size)]

    # Create a multiprocessing pool for parallel processing
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.starmap(process_chunk, [(user_id, day, chunk) for chunk in chunks])

    # Combine the results into a single DynamoDB document
    combined_document = combine_results(results)

    return combined_document

def process_chunk(user_id: int, day: datetime.date, activity_scores: List[int]) -> Dict:
    # Convert activity scores to strings
    activity_scores_as_strings = [str(score) for score in activity_scores]

    # Calculate the timestamp for the start of the day
    start_of_day = int(datetime.datetime(day.year, day.month, day.day).timestamp())

    # Create DynamoDB document with a single list attribute 'v'
    f_third_document = {
            "u": user_id,
            "t": start_of_day,
            "v": activity_scores_as_strings[:960] # First 6 hours
        }

    s_third_document = {
            "u": user_id,
            "t": start_of_day,
            "v": activity_scores_as_strings[960:1920]  # Second 6 hours
        }

    t_third_document = {
            "u": user_id,
            "t": start_of_day,
            "v": activity_scores_as_strings[1920:]  # Third 6 hours
        }

    return [f_third_document, s_third_document, t_third_document]


def combine_results(results: List[Dict]) -> Dict:
    combined_document = {
        "u": results[0]["u"],
        "t": results[0]["t"],
        "v": []
    }

    for result in results:
        combined_document["v"].extend(result["v"])

    return combined_document

user_id = 123456
day = datetime.date(2023, 9, 6)
activity_scores = [60, 61, 78, 23, 25, 35, 23, 66, 78, 11]  

start_time = time.time()
print(convert_to_dynamodb_documents(user_id=user_id, day=day, activity_scores=activity_scores))
end_time = time.time()

elapsed_time = end_time - start_time
print(f'The function took {elapsed_time} seconds to complete')