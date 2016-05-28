# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tempest.lib import decorators

from senlin.tests.tempest.api import base
from senlin.tests.tempest.api import utils


class TestNodeAction(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestNodeAction, cls).resource_setup()
        cls.profile_id = utils.create_a_profile(cls)
        cls.node_id = cls.create_test_node(cls.profile_id)['id']

    @classmethod
    def resource_cleanup(cls):
        cls.delete_test_node(cls.node_id)
        utils.delete_a_profile(cls, cls.profile_id)
        super(TestNodeAction, cls).resource_cleanup()

    @decorators.idempotent_id('ae124bfe-9fcf-4e87-91b7-319102efbdcc')
    def test_node_action_trigger(self):
        params = {
            'check': {
            }
        }
        # Trigger node action
        res = self.client.trigger_action('nodes', self.node_id, params=params)

        # Verfiy resp code, body and location in headers
        self.assertEqual(202, res['status'])
        self.assertIn('actions', res['location'])

        action_id = res['location'].split('/actions/')[1]
        self.wait_for_status('actions', action_id, 'SUCCEEDED')
