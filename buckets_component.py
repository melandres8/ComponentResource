import pulumi_google_native.storage.v1 as storage
from pulumi import Config, ComponentResource, FileArchive, FileAsset, ResourceOptions


config = Config()
project = config.require('project')


class MyBuckets(ComponentResource):
    global _buckets
    _buckets = []
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyBuckets, cls).__new__(cls)
        return cls._instance

    def __init__(self, bucket_name, opts = None):
        super().__init__("pkg:index:MyBuckets", bucket_name, None, opts)
        self.bucket_name = bucket_name
        self.project = project

        bucket = storage.Bucket(f'{self.bucket_name}',
            project=self.project,
            location='UK',
            storage_class='COLDLINE',
            opts=ResourceOptions(parent=self)
        )

        file = storage.BucketObject('index.html',
            bucket=bucket.name,
            content_type='text/plain',
            source='./files/index.html'
        )

        image = storage.BucketObject('tt',
            bucket=bucket.name,
            source=FileAsset('./files/IMG_1512.jpg')
        )

        self.register_outputs({
            'bucket_name': bucket.name,
            'bucket_obj': file.name,
            'bucket_obj': image.name
        })

    def add_bucket(resource_name):
        _buckets.append(resource_name)

    def get_bucket(resource_name: str):
        bkt = storage.get_bucket(resource_name)
        return bkt

    def get_buckets():
        return _buckets
