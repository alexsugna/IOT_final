"""
Configuration variables
"""

"""
S3
"""
s3_access_key = 'AKIAIAT3LZPV7FKA7L7Q'
s3_secret_key = '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'
bucket_name = 'final-alexsugna'
s3_endpoint = 'https://final-alexsugna.s3.us-east-2.amazonaws.com/'

"""
Face
"""
face_subscription_key = 'efca38a358b3453287058f2443e1a7b3'
face_endpoint = 'https://alexsugna.cognitiveservices.azure.com'
face_headers = {'Ocp-Apim-Subscription-Key': face_subscription_key}

"""
EC2
"""
ec2_private_ip = '172.31.40.131'
ec2_public_ip = '18.222.187.211'
ec2_upload_port = 0 # update this

"""
ESP
"""
esp8266_port = 80 # update this
esp_endpoint = '' # update this

"""
Android
"""
android_endpoint = '' # update this

"""
Miscelaneous
"""
idlen = 60
