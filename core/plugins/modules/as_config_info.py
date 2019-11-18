#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: as_config_info
short_description: Get AutoScaling configs
extends_documentation_fragment: openstack
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Get AS config info from the OTC.
options:
  name:
    description:
      - Name of the AS config.
  image_id:
    description:
      - ID of the image to filter results.
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_configs:
    description: List of dictionaries describing RDS datastore version.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the datastore.
            type: str
            sample: "10.0"
'''

EXAMPLES = '''
# Get configs versions.
- as_config_info:
  register: as
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.opentelekomcloud.core.plugins.module_utils.otc \
    import openstack_full_argument_spec, \
    openstack_module_kwargs, openstack_cloud_from_module


def main():
    argument_spec = openstack_full_argument_spec(
        name=dict(required=False),
        image_id=dict(required=False)
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(
        argument_spec=argument_spec,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    name_filter = module.params['name']
    image_id_filter = module.params['image_id']

    try:
        data = []
        # TODO: Pass filters into SDK
        for raw in cloud.auto_scaling.configs():
            if name_filter and raw.name != name_filter:
                continue
            if (image_id_filter
                    and raw.instance_config['image_id'] != image_id_filter):
                continue
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        module.exit_json(
            changed=False,
            as_configs=data
        )

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
