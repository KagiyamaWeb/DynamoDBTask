import boto3
import datetime
import numpy as np
import time
from typing import List, Dict


#dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:5555')
#table = dynamodb.Table('your-table-name')


def convert_to_dynamodb_documents(user_id: int, 
                                  day: datetime.date, 
                                  activity_scores: List[int]
) -> List[Dict]:

    activity_scores_as_strings = np.array(activity_scores, dtype=str)
    start_of_day = int(datetime.datetime(day.year, day.month, day.day).timestamp())

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