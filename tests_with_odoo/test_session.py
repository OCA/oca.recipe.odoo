from oca.recipe.odoo.runtime.session import Session
from odoo.tests.common import get_db_name
from unittest import TestCase

TEST_MODULE = 'web_environment_ribbon'


class SessionTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.open_session()

    def tearDown(self):
        self.session.close()
        super().tearDown()

    def open_session(self):
        self.session = Session(None, None, parse_config=False)
        self.session.open(db=get_db_name())

    def uninstall_if_necessary(self):
        module = self.session.env['ir.module.module'].search(
            [('name', '=', TEST_MODULE)])
        if module.state == "installed":
            module.module_uninstall()

    def test_env_after_install_module(self):
        self.uninstall_if_necessary()
        self.assertAdminPresent()
        self.session.install_modules([TEST_MODULE])
        self.assertAdminPresent()

    def assertAdminPresent(self):
        self.assertIn(
            u"Admin",
            self.session.env['res.users'].search(
                [('login', '=', 'admin')]
            ).name
        )

    def test_env_context(self):
        self.uninstall_if_necessary()
        self.assertTrue(self.session.env.context.get('tz'))
        self.session.install_modules([TEST_MODULE])
        self.assertTrue(self.session.env.context.get('tz'))

    def test_registry(self):
        self.assertAdminPresent()

    def assertModuleState(self, module_name, expected_state):
        self.assertEqual(
            expected_state,
            self.session.env['ir.module.module'].search(
                [('name', '=', module_name)]
            ).state
        )

    def test_install_module(self):
        self.uninstall_if_necessary()
        self.assertModuleState(TEST_MODULE, 'uninstalled')
        self.session.install_modules([TEST_MODULE])
        self.assertModuleState(TEST_MODULE, 'installed')
