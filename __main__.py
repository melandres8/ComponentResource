#!/usr/bin/env python3
"""A Google Cloud Python Pulumi program"""
from buckets_component import MyBuckets
from pulumi import ResourceOptions, ResourceTransformationArgs

if __name__ == '__main__':
    # newBucket = MyBuckets('file-test', opts=ResourceOptions(delete_before_replace=True,
    #                                                         replace_on_changes=['spec.input'],
    #                                                         protect=False))

    clone = MyBuckets.clone_bucket('bbucket11-db2ecce', 'bbucket99')
