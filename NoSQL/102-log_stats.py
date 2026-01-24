#!/usr/bin/env python3
"""Improved log stats: adds top 10 IPs."""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def main():
    """
    Prints statistics about Nginx logs stored in MongoDB.

    - Displays total number of logs
    - Shows HTTP methods count
    - Shows number of GET /status checks
    - Displays top 10 most frequent IPs
    """
    client = MongoClient("mongodb://127.0.0.1:27017")
    col = client.logs.nginx

    total = col.count_documents({})
    print(f"{total} logs")

    print("Methods:")
    for m in METHODS:
        count = col.count_documents({"method": m})
        print(f"\tmethod {m}: {count}")

    status = col.count_documents({"method": "GET", "path": "/status"})
    print(f"{status} status check")

    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1, "_id": 1}},
        {"$limit": 10}
    ]
    for doc in col.aggregate(pipeline):
        print(f"\t{doc['_id']}: {doc['count']}")


if __name__ == "__main__":
    main()
