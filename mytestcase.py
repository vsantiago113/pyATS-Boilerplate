from pyats.topology import Testbed, Device
from pyats import aetest
import re
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
        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/passwords.html#password-handling
        testbed.credentials['default'] = dict(username=self.parameters['username'],
                                              password=self.parameters['password'])

        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/concept.html#device-objects
        # https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#manual-creation
        my_devices = {'SW1': {'os': 'ios', 'ip': '192.168.1.201', 'serial_number': '1234567890'},
                      'SW2': {'os': 'ios', 'ip': '192.168.1.202', 'serial_number': '0987654321'}}
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

        self.parameters['device'] = testbed.devices[switch]

        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html#connection-basics
        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html#customizing-your-connection
        # https://pubhub.devnetcloud.com/media/pyats/docs/getting_started/index.html#connect-and-issue-commands
        self.parameters['device'].connect(learn_hostname=True, connection_timeout=10, log_stdout=False,
                                          init_exec_commands=['term length 0', 'term width 0'], logfile='mypyats.log')

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#test-sections
    @aetest.test
    def check_management_vlan(self, section, steps):
        section.name = 'Check if Management VLAN Exists'

        # https://pubhub.devnetcloud.com/media/unicon/docs/api/unicon.eal.html?highlight=dialog#module-unicon.eal.dialogs
        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/services/service_dialogs.html?highlight=dialog
        """Example of using Dialogs
        dialog = dialogs.Dialog([dialogs.Statement(pattern=r'.*Are you sure you want to continue\?.*',
                                                   action="sendline({'key': 'y'})",
                                                   args=None,
                                                   loop_continue=True,
                                                   continue_timer=False
                                                   )
                                 ])
        output = self.parameters['device'].execute('show ip int b', reply=dialog)
        """

        # https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/services/generic_services.html#configure
        """To configure a device and send configurations check this URL above."""

        output = self.parameters['device'].execute('show ip int b')

        # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/steps.html?highlight=steps#section-steps
        with steps.start('Checking Vlan99 and IP Address', continue_=True) as step:

            # https://docs.python.org/3/howto/regex.html
            match = re.search(r'(?P<vlan>vlan99)\s+(?P<ip>(?:\d{1,3}[.]?){4})', output, flags=re.IGNORECASE)
            if match:
                with step.start('Management Vlan', description='Checking if Vlan99 exists and is configured correctly.',
                                continue_=True) as sub_step:
                    if match.group('ip').startswith('192.168.1.20'):
                        sub_step.passed(f'Vlan: "Vlan99" has the following IP Address set: "{match.group("ip")}"')
                    else:
                        sub_step.failed(f'Vlan99 is not set correctly, found IP Address: "{match.group("ip")}"')
            else:
                step.failed('Vlan99 does not exists or does not have an IP Address set!')

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#cleanup-section
    @aetest.cleanup
    def disconnect_from_device(self, section):
        section.name = 'Disconnect from Device'

        # https://pubhub.devnetcloud.com/media/pyats/docs/connections/class.html#baseconnection
        if self.parameters['device'].connected:
            self.parameters['device'].disconnect()
        self.parameters.pop('device', None)


# https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#common-cleanup
class ScriptCommonCleanup(aetest.CommonCleanup):
    uid = 'CommonCleanup'

    # https://pubhub.devnetcloud.com/media/pyats/docs/aetest/structure.html#subsections
    @aetest.subsection
    def cleanup_section(self):
        pass


if __name__ == '__main__':
    aetest.main()
