from pyats.topology import Testbed, Device
from pyats import aetest
from unicon.eal import dialogs
import sys

testbed = Testbed('dynamic_testbed')


class CommonSetup(aetest.CommonSetup):
    uid = 'CommonSetup'

    @aetest.subsection
    def default_setup(self, section):
        section.name = 'Default Setup'

        print(self.parameters['username'])
        print(self.parameters['password'])
        print(self.parameters.__dict__)


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def default_cleanup(self, section):
        section.name = 'Cleanup'


if __name__ == '__main__':
    aetest.main()
