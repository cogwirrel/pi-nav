import sys
import arrow
import boto3
import uuid
from alexi.db.credentials import AWS_SECRET_KEY, AWS_ACCESS_KEY_ID, AWS_REGION

DOMAIN = 'AlexiData'

def _db():
    return boto3.client('sdb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def _attributes_to_dict(attributes):
    return {x['Name']: x['Value'] for x in attributes}


def _dict_to_attributes(attrs):
    return [{'Name': k, 'Value': str(v), 'Replace': True} for k, v in attrs.iteritems()]


def set_current_gps_data(data):
    data['timestamp'] = arrow.utcnow().isoformat()

    _db().put_attributes(
        DomainName=DOMAIN,
        ItemName=str(uuid.uuid4()),
        Attributes=_dict_to_attributes(data)
    )
