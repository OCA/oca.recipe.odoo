import unittest
import os
import shutil
from tempfile import mkdtemp
from ..utils import working_directory_keeper

COMMIT_USER_NAME = 'Test'
COMMIT_USER_EMAIL = 'test@example.org'
COMMIT_USER_FULL = '%s %s' % (COMMIT_USER_NAME, COMMIT_USER_EMAIL)


class VcsTestCase(unittest.TestCase):
    """Common fixture"""

    def setUp(self):
        sandbox = self.sandbox = mkdtemp('test_oerp_recipe_vcs')
        src = self.src_dir = os.path.join(sandbox, 'src')
        dst = self.dst_dir = os.path.join(sandbox, 'dest')
        os.mkdir(src)
        os.mkdir(dst)
        with working_directory_keeper:
            self.create_src()

    def create_src(self):
        """Create a source repository to run most tests.

        To be implemented in subclasses."""
        raise NotImplementedError

    def tearDown(self):
        shutil.rmtree(self.sandbox)

    def assertShaEqual(self, this, other, msg=None):
        """Compare a SHA or a list of SHAs passed as str or bytes array"""

        def normalize(arg):
            if isinstance(arg, (list, tuple)):
                arg = list(arg)
                for idx, item in enumerate(arg):
                    arg[idx] = normalize(item)
            elif isinstance(arg, bytes):
                arg = arg.decode()
            return arg

        self.assertEqual(normalize(this), normalize(other), msg=msg)
