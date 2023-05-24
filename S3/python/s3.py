#
# IPWorks 2022 Python Edition - Demo Application
#
# Copyright (c) 2023 /n software inc. - All rights reserved. - www.nsoftware.com
#

import sys
import string
from ipworks import *

input = sys.hexversion<0x03000000 and raw_input or input



def fire_error(e):
    print("Error %i: %s\n" % (e.code, e.message))


def print_menu():
    print("\n?   - Help")
    print("cd  - Change to bucket")
    print("ls  - List Objects")
    print("get - Get remoteFile")
    print("put - Put localFile")
    print("q   - Quit")


def fire_bucket_list(arg):
    print(arg.bucket_name)


def fire_object_list(arg):
    print(arg.object_name)


try:
    s3 = S3()
    buffer = ""

    s3.on_error = fire_error
    s3.on_bucket_list = fire_bucket_list
    s3.on_object_list = fire_object_list

    print("\n0     -   Amazon S3")
    print("1     -   Digital Ocean")
    print("2     -   Google Storage")
    print("3     -   Wasabi")
    print("4     -   Backblaze B2")
    print("5     -   Huawei")
    print("6     -   Alibaba")
    print("7     -   IBM")
    print("8     -   Oracle")
    print("9     -   Linode")
    print("255   -   Custom\n")

    s3.set_service_provider(int(input("Select Service Provider (enter number): ")))
    if s3.get_service_provider() == 255:  # Custom service Provider
        s3.config("URL=" + input("Custom URL: "))
    elif s3.get_service_provider() == 8:  # Custom service Provider
        s3.config("OracleNamespace" + input("Oracle Namespace: "))

    s3.set_access_key(input("Access Key: "))
    s3.set_secret_key(input("Secret Key: "))

    print("\nBucket List:\n")
    s3.list_buckets()

    print_menu()
    while buffer != "q":
        buffer = input("\nEnter Command: ")
        buffer = buffer.lower()
        if buffer == "cd":
            s3.set_bucket(input("Which Bucket?: "))
        elif buffer == "ls":
            s3.list_objects()
        elif buffer == "get":
            s3.set_local_file("")
            s3.get_object(input("Which file?: "))
            print("The content of the file:\n", (s3.get_object_data()))
        elif buffer == "put":
            s3.set_local_file(input("Local File to Upload: "))
            s3.create_object(input("Name of New Object: "))
            print("Object Created.")
        elif buffer == "?":
            print_menu()
        else:
            print("\nCommand Not Recognized.\n")
            print_menu()

except IPWorksError as e:
    fire_error(e)

except KeyboardInterrupt:
    print("Shutdown requested...exiting")

