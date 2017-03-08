#!/usr/bin/env python
import os, sys
import math
import boto
from global_credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME

class VideoUpload:

    def __init__(self, filepath):
        self.filepath = filepath
        self.bucketname = S3_BUCKET_NAME
        self.s3 = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    def upload_file(self):

        b = self.s3.get_bucket(self.bucketname)

        filename = os.path.basename(self.filepath)
        k = b.new_key(filename)

        mp = b.initiate_multipart_upload(str(k.key))
        print mp,"!!!!"

        source_size = os.stat(self.filepath).st_size

        #Minimum 5Mb chunk is required to successfully upload a file in multiparts
        bytes_per_chunk = 6*1024*1024

        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

        for i in range(chunks_count):
                offset = i * bytes_per_chunk
                remaining_bytes = source_size - offset
                bytes = min([bytes_per_chunk, remaining_bytes])
                part_num = i + 1

                print "uploading part " + str(part_num) + " of " + str(chunks_count)

                with open(self.filepath, 'r') as fp:
                        fp.seek(offset)
                        mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)

        if len(mp.get_all_parts()) == chunks_count:
                mp.complete_upload()
                k.set_canned_acl('public-read')
                video_url = k.generate_url(0, query_auth=False, force_http=True)
                return video_url
                print "upload_file done"
        else:
                mp.cancel_upload()
                print "upload_file failed"

if __name__ == "__main__":

        if len(sys.argv) != 3:
                print "usage: python s3upload.py bucketname filepath"
                exit(0)

        bucketname = BUCKET_NAME

        filepath = sys.argv[1]

        s3 = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

        upload_file(s3, bucketname, filepath)


