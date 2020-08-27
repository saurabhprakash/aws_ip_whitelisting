from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

import boto3

import os

@login_required
def index(request):

    if request.method == 'POST':
        print('Adding port: ' + request.POST['port'] + ', for IP: ' + request.POST['ip'])
        ec2 = boto3.client('ec2')
        security_group_id = os.environ['SG']
        data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
                'FromPort': int(request.POST['port']),
                'ToPort': int(request.POST['port']),
                'IpRanges': [{
                    'CidrIp': request.POST['ip'].strip() + '/32',
                    'Description': request.user.username
                }]
            }
        ])
        print ('response from aws=' + str(data))
        return render(request, 'success.html', {
            
        })
    return render(request, 'input.html', {
            
        })
