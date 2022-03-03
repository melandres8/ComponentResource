import uuid
from pulumi_gcp import storage as stg
import pulumi_google_native.iam.v1 as iam
import pulumi_google_native.storage.v1 as storage
import pulumi_google_native.storagetransfer.v1 as storagetransfer
from pulumi import Config, ComponentResource, FileAsset, ResourceOptions

config = Config()
project = config.require('project')


class MyBuckets(ComponentResource):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MyBuckets, cls).__new__(cls)
        return cls._instance

    def __init__(self, bucket_name, opts=None):
        super().__init__("pkg:index:MyBuckets", bucket_name, None, opts)
        self.bucket_name = bucket_name
        self.project = project
        sv_account = stg.get_transfer_project_servie_account(project=project)
        bucket = storage.Bucket(f'{self.bucket_name}',
                                project=self.project,
                                location='US',
                                storage_class='STANDARD',
                                opts=ResourceOptions(parent=self, delete_before_replace=True)
                                )

        iam_member = stg.BucketIAMMember("backup-bucket-IAMMember",
                                         bucket=bucket.name,
                                         role="roles/storage.admin",
                                         member=f"serviceAccount:{sv_account.email}",
                                         opts=ResourceOptions(depends_on=[bucket])
                                         )

        file = storage.BucketObject('idx',
                                    bucket=bucket.name,
                                    content_type='text/plain',
                                    source='./files/index.html'
                                    )

        image = storage.BucketObject('tt',
                                     bucket=bucket.name,
                                     source=FileAsset('./files/IMG_1512.jpg')
                                     )

        # self.register_outputs({
        #     #'bucket_name': bucket.name,
        #     'bucket_obj': file.name,
        #     'bucket_obj1': image.name
        # })

    @staticmethod
    def get_bucket(resource_name: str):
        bkt = storage.get_bucket(resource_name)
        return bkt

    @staticmethod
    def clone_bucket(src_bucket_name, dest_bucket_name):
        src_bucket = MyBuckets.get_bucket(src_bucket_name)
        gcs_account = stg.get_transfer_project_servie_account(project=project)
        bucket_backup = storage.Bucket(
            resource_name=dest_bucket_name,
            storage_class="COLDLINE",
            project=project,
            location="US",
            opts=ResourceOptions(delete_before_replace=True)
        )
        bucket_iam_member = stg.BucketIAMMember(
            resource_name="backup-bucket-IAMMember",
            bucket=bucket_backup.name,
            role="roles/storage.admin",
            member=f"serviceAccount:{gcs_account.email}",
            opts=ResourceOptions(depends_on=[bucket_backup])
        )
        bucket_transfer = storagetransfer.TransferJob(
            resource_name="bucket-clone",
            description="Transfer service for buckets",
            project=project,
            status=storagetransfer.TransferJobStatus.ENABLED,
            transfer_spec=storagetransfer.TransferSpecArgs(
                gcs_data_source=stg.TransferJobTransferSpecGcsDataSourceArgs(
                    bucket_name=src_bucket.name,
                ),
                gcs_data_sink=stg.TransferJobTransferSpecGcsDataSinkArgs(
                    bucket_name=bucket_backup.name,
                ),
                transfer_options=stg.TransferJobTransferSpecTransferOptionsArgs(
                    delete_objects_from_source_after_transfer=True,
                )
            ),
            opts=ResourceOptions(depends_on=[bucket_iam_member]),
        )
        print(gcs_account.email)
