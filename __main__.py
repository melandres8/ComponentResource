#!/usr/bin/env python3
"""A Google Cloud Python Pulumi program"""
from buckets_component import MyBuckets
from pulumi import ResourceOptions, ResourceTransformationArgs

if __name__ == '__main__':
    newBucket = MyBuckets('file-test', opts=ResourceOptions(delete_before_replace=True,
                                                            replace_on_changes=['spec.input'],
                                                            protect=False))

    bucket = MyBuckets.get_bucket('file-test-050c225')
    clone = MyBuckets.clone_bucket('file-test-050c225', 'backup-bucket')
    print(bucket.name)
