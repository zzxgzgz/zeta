# SPDX-License-Identifier: MIT
# Copyright (c) 2020 The Authors.
#
# Authors: Bin Liang <@liangbin>
#
# Summary: Zeta Network node table for NBI API
#


import os
import uuid
import logging

from flask import (
    Blueprint, jsonify, request
)

from project.api.models import Node
from project import db
from .models import Zgc
from .....operator.obj.droplet import Droplet
from kubernetes import client, config

# from .....operator.operators.droplets_operator import DropletOperator
# from .....operator.operators.fwds_operator import FwdOperator
# from .....operator.operators.dfts_operator import DftOperator 

from .....operator.common.constants import KIND
from .vpcs import getGWsFromIpRange
logger = logging.getLogger()
config.load_incluster_config()
obj_api = client.CustomObjectsApi()
# existing_droplet_operator = DropletOperator()

# existing_fwd_operator = FwdOperator()

# existing_dft_operator = DftOperator()
nodes_blueprint = Blueprint('nodes', __name__)

def printlog(string):
    print(string)
    logger.info(string)

@nodes_blueprint.route('/nodes', methods=['GET', 'POST'])
def all_nodes():
    if request.method == 'POST':
        post_data = request.get_json()
        post_data['node_id'] = str(uuid.uuid4())

        response_object = post_data
        
        # query for Zgc
        zgc_id = post_data['zgc_id']
        zgc_for_id = Zgc.query.filter_by(zgc_id=zgc_id).first()
        
        printlog('zgc: {}'.format(zgc_for_id))

        # Try to get the existing fwds


        all_droplets_in_zgc = obj_api.list_cluster_custom_object(group="zeta.com",
            version="v1",
            namespace="default",
            plural="droplets"
        )

        printlog('Existing droplets: {}'.format(all_droplets_in_zgc))
        
        
        # # only execute if the Zgc with that zgc_id exists
        # if zgc_for_id:
        #     # Calculate how many IPs should this node get
        #     ips_macs_for_zgc_ip_range = getGWsFromIpRange(zgc_for_id.ip_start, zgc_for_id.ip_end)

        #     ips_macs_amount = len(ips_macs_for_zgc_ip_range['ip'])

        #     how_many_ip_should_this_node_get = ips_macs_amount // (len(zgc_for_id.nodes))

        #     ips = []
        #     macs = []

        #     modified_allocated_droplets = set()
        #     modified_allocated_fwds = set()

        #     # These are only keys, aka name of the object
        #     all_fwds_names = existing_fwd_operator.store.get_all_obj_type(KIND.fwd)

        #     all_fwds_in_zgc = [existing_droplet_operator.store[KIND.fwd][fwd_name] for fwd_name in all_fwds_names if zgc_id in fwd_name]
        #     # Get IPs and macs from other nodes(droplets), and remove those IPs and macs from those nodes(droplets) and ftns, then update those kube objects
        #     for i in range(how_many_ip_should_this_node_get):
        #         # this is a kube object
        #         fwd = all_fwds_in_zgc[i % how_many_ip_should_this_node_get]
                
        #         droplet_name_for_this_fwd = fwd.droplet
        #         # this is a kube object
        #         droplet = existing_droplet_operator.store[KIND.droplet][droplet_name_for_this_fwd]

        #         ip_list = droplet.ip.split(',')

        #         reassigned_ip = ip_list.pop()

        #         droplet.ip = ','.join(ip_list)

        #         mac_list = droplet.mac.split(',')

        #         reassigned_mac = mac_list.pop()

        #         droplet.mac = ','.join(mac_list)

        #         ips.append(reassigned_ip)

        #         macs.append(reassigned_mac)

        #         modified_allocated_droplets.add(droplet)

        #         modified_allocated_fwds.add(fwd)
                
        #     # Create Droplet objects for tenants, with the IPs and MACs
        #     new_droplet_tenant = Droplet(name=post_data['name'+'-'+post_data['inf_tenant']+'-'+zgc_id], obj_api=existing_droplet_operator.obj_api, network='tenant')
        #     new_droplet_tenant.ip = ','.join(ips)
        #     new_droplet_tenant.mac = ','.join(macs)
        #     new_droplet_tenant.phy_itf = post_data['inf_tenant']

        #     # Creat Droplet object for ZGC, with IP from 
        #     # Update the modified objects
        #     for modified_droplet in modified_allocated_droplets:
        #         modified_droplet.update_object()

        #     for modified_fwd in modified_allocated_fwds:
        #         modified_fwd.update_object()

        # commit change to data at last
        db.session.add(Node(**post_data))
        db.session.commit()
    
    else:
        response_object = [node.to_json() for node in Node.query.all()]
    return jsonify(response_object)


@nodes_blueprint.route('/nodes/ping', methods=['GET'])
def ping_nodes():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': os.uname()[1]
    })


@nodes_blueprint.route('/nodes/<node_id>', methods=['GET', 'PUT', 'DELETE'])
def single_node(node_id):
    node = Node.query.filter_by(node_id=node_id).first()
    if request.method == 'GET':
        response_object = node.to_json()
    elif request.method == 'PUT':
        post_data = request.get_json()
        node.zgc_id = post_data.get('zgc_id')
        node.description = post_data.get('description')
        node.ip_control = post_data.get('ip_control')
        node.inf_tenant = post_data.get('inf_tenant')
        node.inf_zgc = post_data.get('inf_zgc')
        db.session.commit()
        response_object = node.to_json()
    elif request.method == 'DELETE':
        db.session.delete(node)
        db.session.commit()
        response_object = {}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
