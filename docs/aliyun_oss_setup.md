aliyun oss setup
============

### Create an oss bucket

Create a new oss bucket that will be used to store the backups, and do not enable public access.


### Configure Medusa

Generate access keys for that user and save them in a file called `.ossutilconfig` in the following format:

```
[Credentials]
language=CH
endpoint=oss-cn-beijing.aliyuncs.com
accessKeyID=<your-ak>
accessKeySecret=<your-sk>
```

Place this file on all Cassandra nodes running medusa under `/etc/medusa` and set the rights appropriately so that only users running Medusa can read/modify it.
Set the `key_file` value in the `[storage]` section of `/etc/medusa/medusa.ini` to the credentials file:  

```
storage_provider = aliyun_oss
bucket_name = my_oss_bucket
key_file = /etc/medusa/.ossutilconfig
api_profile=Credentials

```

Medusa should now be able to access the bucket and perform all required operations.
