#!/usr/bin/env python3
"""A Google Cloud Python Pulumi program"""
from buckets_component import MyBuckets
from pulumi import ResourceOptions


if __name__ == '__main__':
    newBucket = MyBuckets('file-test', opts=ResourceOptions(delete_before_replace=True,
                                                            replace_on_changes=['spec.input'],
                                                            protect=True))
    MyBuckets.add_bucket(newBucket)
    bucket = MyBuckets.get_bucket('file-test-d9d63a0')
    print(bucket)
