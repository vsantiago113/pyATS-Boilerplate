from pyats.topology import Testbed, Device
from pyats import aetest
from unicon.eal import dialogs

# https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#manual-creation
testbed = Testbed(name='dynamic_testbed')


# https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html
# https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#common-setup
class ScriptCommonSetup(aetest.CommonSetup):
    uid = 'CommonSetup'

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#subsections
    @aetest.subsection
    def default_setup(self, section):
        section.name = 'Default Script Setup'

        # https://pubhub.devnetcloud.com/media/pyats/docs/getting_started/index.html#describe-your-testbed
        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#testbed-file
        """If you want to use a YAML file instead check the two urls above. 
        The two links above shows you how to create the YAML file and how to load it."""

        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/concept.html#testbed-object
        testbed.credentials['default'] = dict(username=self.parameters.get('username'),
                                              password=self.parameters.get('password'))

        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/concept.html#device-objects
        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#manual-creation
        my_devices = {'SW1': {'os': 'iosxe', 'ip': '192.168.1.201', 'serial_number': '1234567890'},
                      'SW2': {'os': 'iosxe', 'ip': '192.168.1.202', 'serial_number': '0987654321'}}
        for k, v in my_devices.items():
            device = Device(k,
                            os=v['os'],
                            connections={
                                'ssh': {
                                    'protocol': 'ssh',
                                    'ip': v['ip']
                                }
                            },
                            custom={
                                'data': {
                                    'serial_number': v['serial_number']
                                }
                            })
            testbed.add_device(device)

        # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/examples.html?highlight=aetest%20loop%20mark#mega-looping
        aetest.loop.mark(MyTestcase, switch=[sw for sw in testbed.devices],
                         uids=[sw.replace(' ', '_') for sw in testbed.devices])


# https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#testcases
class MyTestcase(aetest.Testcase):
    uid = 'ScriptTestCase'

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#setup-section
    @aetest.setup
    def establish_connection(self, section, switch):
        section.name = 'Establish Connection'

        device = testbed.devices[switch]

        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html#connection-basics
        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html#customizing-your-connection
        # https://pubhub.devnetcloud.com/media/pyats/docs/getting_started/index.html#connect-and-issue-commands
        device.connect(learn_hostname=True, connection_timeout=10, log_stdout=False,
                       init_exec_commands=['term length 0', 'term width 0'])

        device.execute('show ip int b')

        device.disconnect()

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#test-sections
    @aetest.test
    def testcase_part1(self, section, switch):
        section.name = 'Testcase Part 1'

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#cleanup-section
    @aetest.cleanup
    def testcase_cleanup(self, section, switch):
        section.name = 'Cleanup'


# https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#common-cleanup
class ScriptCommonCleanup(aetest.CommonCleanup):
    uid = 'CommonCleanup'

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#subsections
    @aetest.subsection
    def disconnect_from_device(self):
        pass


if __name__ == '__main__':
    aetest.main()
