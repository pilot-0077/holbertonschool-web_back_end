#!/usr/bin/env python3
"""Module for using PyMongo"""


def top_students(mongo_collection):
    """Return all students sorted by average score (descending)."""
    pipeline = [
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))
