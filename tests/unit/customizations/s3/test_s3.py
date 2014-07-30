# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0e
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import argparse
import os
from six import StringIO
import sys
from awscli.testutils import unittest
import mock

import botocore.session
from mock import Mock, MagicMock, patch

from awscli.customizations.s3.s3 import AppendFilter, \
    awscli_initialize, add_s3, \
    S3, S3SubCommand, S3Parameter, CommandArchitecture, CommandParameters, \
    ListCommand
from tests.unit.customizations.s3 import make_loc_files, clean_loc_files, \
    make_s3_files, s3_cleanup, S3HandlerBaseTest
from tests.unit.customizations.s3.fake_session import FakeSession
from awscli.testutils import BaseAWSHelpOutputTest


class AppendFilterTest(unittest.TestCase):
    def test_call(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('--include', action=AppendFilter, nargs=1,
                            dest='path')
        parser.add_argument('--exclude', action=AppendFilter, nargs=1,
                            dest='path')
        parsed_args = parser.parse_args(['--include', 'a', '--exclude', 'b'])
        self.assertEqual(parsed_args.path, [['--include', 'a'],
                                            ['--exclude', 'b']])


class FakeArgs(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class AWSInitializeTest(unittest.TestCase):
    """
    This test ensures that all events are correctly registered such that
    all of the commands can be run.
    """
    def setUp(self):
        self.cli = Mock()

    def test_initialize(self):
        awscli_initialize(self.cli)
        reference = []
        reference.append("building-command-table.main")
        reference.append("building-operation-table.s3")
        reference.append("doc-examples.S3.*")
        # TODO: Change this test, it has to be updated everytime we
        # add a new command.
        cmds = ['mv', 'rm', 'ls', 'rb', 'mb', 'cp', 'sync', 'website']
        for cmd in cmds:
            reference.append("building-parameter-table.s3." + cmd)
        for arg in self.cli.register.call_args_list:
            self.assertIn(arg[0][0], reference)


class CreateTablesTest(unittest.TestCase):
    def test_s3(self):
        """
        Ensures that the table for the service was created properly.
        Also ensures the original s3 service is renamed to ``s3api``.
        """
        s3_service = Mock()
        s3_service.name = 's3'
        self.services = {'s3': s3_service}
        add_s3(self.services, True)
        orig_service = self.services.pop('s3api')
        self.assertEqual(orig_service, s3_service)
        for service in self.services.keys():
            self.assertIn(service, ['s3'])


class S3SubCommandTest(unittest.TestCase):
    """
    This checks top make sure that the S3SubCommand properly handles commands
    passed to it.
    """
    def setUp(self):
        self.session = FakeSession()
        module = 'awscli.customizations.s3.s3.CommandArchitecture'
        self.cmd_arc_patch = patch(module)
        self.cmd_arc_mock = self.cmd_arc_patch.start()
        self.cmd_arc_mock.run.return_value = "Passed"

    def tearDown(self):
        self.cmd_arc_patch.stop()

    def test_call_error(self):
        """
        This checks to make sure an improper command throws an
        exception.
        """
        s3_command = S3SubCommand('cp', self.session,  {'nargs': 2})
        with self.assertRaisesRegexp(ValueError, 'Unknown options'):
            s3_command(['foo', 's3://', '--sfdf'], [])


class S3ParameterTest(unittest.TestCase):
    """
    Tests the ability to put parameters along with options into
    a parser using the S3Parameter class
    """
    def test_add_to_parser(self):
        s3_param = S3Parameter('test',
                               {'action': 'store_true', 'dest': 'destination'})
        parser = argparse.ArgumentParser()
        s3_param.add_to_parser(parser)
        parsed_args = parser.parse_args(['--test'])
        self.assertTrue(parsed_args.destination)


class CommandArchitectureTest(S3HandlerBaseTest):
    def setUp(self):
        super(CommandArchitectureTest, self).setUp()
        self.session = FakeSession()
        self.bucket = make_s3_files(self.session)
        self.loc_files = make_loc_files()
        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout

        super(CommandArchitectureTest, self).setUp()
        clean_loc_files(self.loc_files)
        s3_cleanup(self.bucket, self.session)

    def test_create_instructions(self):
        """
        This tests to make sure the instructions for any command is generated
        properly.
        """
        cmds = ['cp', 'mv', 'rm', 'sync', 'mb', 'rb']

        instructions = {'cp': ['file_generator', 's3_handler'],
                        'mv': ['file_generator', 's3_handler'],
                        'rm': ['file_generator', 's3_handler'],
                        'sync': ['file_generator', 'comparator', 's3_handler'],
                        'mb': ['s3_handler'],
                        'rb': ['s3_handler']}

        params = {'filters': True, 'region': 'us-east-1', 'endpoint_url': None,
                  'verify_ssl': None}
        for cmd in cmds:
            cmd_arc = CommandArchitecture(self.session, cmd,
                                          {'region': 'us-east-1',
                                           'endpoint_url': None,
                                           'verify_ssl': None})
            cmd_arc.create_instructions()
            self.assertEqual(cmd_arc.instructions, instructions[cmd])

        # Test if there is a filter.
        cmd_arc = CommandArchitecture(self.session, 'cp', params)
        cmd_arc.create_instructions()
        self.assertEqual(cmd_arc.instructions, ['file_generator', 'filters',
                                                's3_handler'])

    def test_run_cp_put(self):
        # This ensures that the architecture sets up correctly for a ``cp`` put
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]
        rel_local_file = os.path.relpath(local_file)
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': True, 'quiet': False,
                  'src': local_file, 'dest': s3_file, 'filters': filters,
                  'paths_type': 'locals3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'cp', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) upload: %s to %s" % (rel_local_file, s3_file)
        self.assertIn(output_str, self.output.getvalue())

    def test_error_on_same_line_as_status(self):
        s3_file = 's3://' + 'bucket-does-not-exist' + '/' + 'text1.txt'
        local_file = self.loc_files[0]
        rel_local_file = os.path.relpath(local_file)
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': False, 'quiet': False,
                  'src': local_file, 'dest': s3_file, 'filters': filters,
                  'paths_type': 'locals3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'cp', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        # Also, we need to verify that the error message is on the *same* line
        # as the upload failed line, to make it easier to track.
        output_str = (
            "upload failed: %s to %s Error: Bucket does not exist\n" % (
                rel_local_file, s3_file))
        self.assertIn(output_str, self.output.getvalue())

    def test_run_cp_get(self):
        # This ensures that the architecture sets up correctly for a ``cp`` get
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]
        rel_local_file = os.path.relpath(local_file)
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': True, 'quiet': False,
                  'src': s3_file, 'dest': local_file, 'filters': filters,
                  'paths_type': 's3local', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'cp', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) download: %s to %s" % (s3_file, rel_local_file)
        self.assertIn(output_str, self.output.getvalue())

    def test_run_cp_copy(self):
        # This ensures that the architecture sets up correctly for a ``cp`` copy
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': True, 'quiet': False,
                  'src': s3_file, 'dest': s3_file, 'filters': filters,
                  'paths_type': 's3s3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'cp', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) copy: %s to %s" % (s3_file, s3_file)
        self.assertIn(output_str, self.output.getvalue())

    def test_run_mv(self):
        # This ensures that the architecture sets up correctly for a ``mv``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': True, 'quiet': False,
                  'src': s3_file, 'dest': s3_file, 'filters': filters,
                  'paths_type': 's3s3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'mv', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) move: %s to %s" % (s3_file, s3_file)
        self.assertIn(output_str, self.output.getvalue())

    def test_run_remove(self):
        # This ensures that the architecture sets up correctly for a ``rm``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        filters = [['--include', '*']]
        params = {'dir_op': False, 'dryrun': True, 'quiet': False,
                  'src': s3_file, 'dest': s3_file, 'filters': filters,
                  'paths_type': 's3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'rm', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) delete: %s" % s3_file
        self.assertIn(output_str, self.output.getvalue())

    def test_run_sync(self):
        # This ensures that the architecture sets up correctly for a ``sync``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]
        s3_prefix = 's3://' + self.bucket + '/'
        local_dir = self.loc_files[3]
        rel_local_file = os.path.relpath(local_file)
        filters = [['--include', '*']]
        params = {'dir_op': True, 'dryrun': True, 'quiet': False,
                  'src': local_dir, 'dest': s3_prefix, 'filters': filters,
                  'paths_type': 'locals3', 'region': 'us-east-1',
                  'endpoint_url': None, 'verify_ssl': None,
                  'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'sync', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) upload: %s to %s" % (rel_local_file, s3_file)
        self.assertIn(output_str, self.output.getvalue())

    def test_run_mb(self):
        # This ensures that the architecture sets up correctly for a ``rb``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_prefix = 's3://' + self.bucket + '/'
        params = {'dir_op': True, 'dryrun': True, 'quiet': False,
                  'src': s3_prefix, 'dest': s3_prefix, 'paths_type': 's3',
                  'region': 'us-east-1', 'endpoint_url': None,
                  'verify_ssl': None, 'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'mb', params)
        cmd_arc.create_instructions()
        cmd_arc.run()
        output_str = "(dryrun) make_bucket: %s" % s3_prefix
        self.assertIn(output_str, self.output.getvalue())

    def test_run_rb(self):
        # This ensures that the architecture sets up correctly for a ``rb``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_prefix = 's3://' + self.bucket + '/'
        params = {'dir_op': True, 'dryrun': True, 'quiet': False,
                  'src': s3_prefix, 'dest': s3_prefix, 'paths_type': 's3',
                  'region': 'us-east-1', 'endpoint_url': None,
                  'verify_ssl': None, 'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'rb', params)
        cmd_arc.create_instructions()
        rc = cmd_arc.run()
        output_str = "(dryrun) remove_bucket: %s" % s3_prefix
        self.assertIn(output_str, self.output.getvalue())
        self.assertEqual(rc, 0)

    def test_run_rb_nonzero_rc(self):
        # This ensures that the architecture sets up correctly for a ``rb``
        # command.  It is just just a dry run, but all of the components need
        # to be wired correctly for it to work.
        s3_prefix = 's3://' + self.bucket + '/'
        params = {'dir_op': True, 'dryrun': False, 'quiet': False,
                  'src': s3_prefix, 'dest': s3_prefix, 'paths_type': 's3',
                  'region': 'us-east-1', 'endpoint_url': None,
                  'verify_ssl': None, 'follow_symlinks': True}
        cmd_arc = CommandArchitecture(self.session, 'rb', params)
        cmd_arc.create_instructions()
        rc = cmd_arc.run()
        output_str = "remove_bucket failed: %s" % s3_prefix
        self.assertIn(output_str, self.output.getvalue())
        self.assertEqual(rc, 1)


class CommandParametersTest(unittest.TestCase):
    def setUp(self):
        self.environ = {}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()
        self.session = FakeSession()
        self.mock = MagicMock()
        self.mock.get_config = MagicMock(return_value={'region': None})
        self.loc_files = make_loc_files()
        self.bucket = make_s3_files(self.session)

    def tearDown(self):
        self.environ_patch.stop()
        clean_loc_files(self.loc_files)
        s3_cleanup(self.bucket, self.session)

    def test_check_path_type_pass(self):
        # This tests the class's ability to determine whether the correct
        # path types have been passed for a particular command.  It test every
        # possible combination that is correct for every command.
        cmds = {'cp': ['locals3', 's3s3', 's3local'],
                'mv': ['locals3', 's3s3', 's3local'],
                'rm': ['s3'], 'mb': ['s3'], 'rb': ['s3'],
                'sync': ['locals3', 's3s3', 's3local']}
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]

        combos = {'s3s3': [s3_file, s3_file],
                  's3local': [s3_file, local_file],
                  'locals3': [local_file, s3_file],
                  's3': [s3_file],
                  'local': [local_file],
                  'locallocal': [local_file, local_file]}

        for cmd in cmds.keys():
            cmd_param = CommandParameters(self.session, cmd, {})
            cmd_param.add_region(mock.Mock())
            correct_paths = cmds[cmd]
            for path_args in correct_paths:
                cmd_param.check_path_type(combos[path_args])

    def test_check_path_type_fail(self):
        # This tests the class's ability to determine whether the correct
        # path types have been passed for a particular command. It test every
        # possible combination that is incorrect for every command.
        cmds = {'cp': ['local', 'locallocal', 's3'],
                'mv': ['local', 'locallocal', 's3'],
                'rm': ['local', 'locallocal', 's3s3', 'locals3', 's3local'],
                'ls': ['local', 'locallocal', 's3s3', 'locals3', 's3local'],
                'sync': ['local', 'locallocal', 's3'],
                'mb': ['local', 'locallocal', 's3s3', 'locals3', 's3local'],
                'rb': ['local', 'locallocal', 's3s3', 'locals3', 's3local']}
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]

        combos = {'s3s3': [s3_file, s3_file],
                  's3local': [s3_file, local_file],
                  'locals3': [local_file, s3_file],
                  's3': [s3_file],
                  'local': [local_file],
                  'locallocal': [local_file, local_file]}

        for cmd in cmds.keys():
            cmd_param = CommandParameters(self.session, cmd, {})
            cmd_param.add_region(mock.Mock())
            wrong_paths = cmds[cmd]
            for path_args in wrong_paths:
                with self.assertRaises(TypeError):
                    cmd_param.check_path_type(combos[path_args])

    def test_check_src_path_pass(self):
        # This tests to see if all of the checks on the source path works.  It
        # does so by testing if s3 objects and and prefixes exist as well as
        # local files and directories.  All of these should not throw an
        # exception.
        s3_file = 's3://' + self.bucket + '/' + 'text1.txt'
        local_file = self.loc_files[0]
        s3_prefix = 's3://' + self.bucket
        local_dir = self.loc_files[3]

        # :var files: a list of tuples where the first element is a single
        #     element list of file paths. The second element is a boolean
        #     representing if the operation is a directory operation.
        files = [([s3_file], False), ([local_file], False),
                 ([s3_prefix], True), ([local_dir], True)]

        parameters = {}
        for filename in files:
            parameters['dir_op'] = filename[1]
            cmd_parameter = CommandParameters(self.session, 'put', parameters)
            cmd_parameter.add_region(mock.Mock())
            cmd_parameter.check_src_path(filename[0])

    def test_check_force(self):
        # This checks to make sure that the force parameter is run. If
        # successful. The delete command will fail as the bucket is empty
        # and be caught by the exception.
        cmd_params = CommandParameters(self.session, 'rb', {'force': True})
        cmd_params.parameters['src'] = 's3://mybucket'
        cmd_params.check_force(None)


class HelpDocTest(BaseAWSHelpOutputTest):
    def setUp(self):
        super(HelpDocTest, self).setUp()
        self.session = botocore.session.get_session()

    def tearDown(self):
        super(HelpDocTest, self).tearDown()

    def test_s3_help(self):
        # This tests the help command for the s3 service. This
        # checks to make sure the appropriate descriptions are
        # added including the tutorial.
        s3 = S3('s3', self.session)
        parser = argparse.ArgumentParser()
        parser.add_argument('--paginate', action='store_true')
        parsed_global = parser.parse_args(['--paginate'])
        help_command = s3.create_help_command()
        help_command([], parsed_global)
        self.assert_contains("This provides higher level S3 commands")
        self.assert_contains("Every command takes one or two positional")
        self.assert_contains("* rb")

    def test_s3command_help(self):
        # This tests the help command for an s3 command. This
        # checks to make sure the command prints appropriate
        # parts.  Note the examples are not included because
        # the event was not registered.
        s3command = S3SubCommand('cp', self.session, {'nargs': 2})
        parser = argparse.ArgumentParser()
        parser.add_argument('--paginate', action='store_true')
        parsed_global = parser.parse_args(['--paginate'])
        help_command = s3command.create_help_command()
        help_command([], parsed_global)
        self.assert_contains("cp")
        self.assert_contains("[--acl <value>]")
        self.assert_contains("Displays the operations that would be")

    def test_help(self):
        # This ensures that the file appropriately redirects to help object
        # if help is the only argument left to be parsed.  There should not
        # have any contents in the docs.
        s3_command = S3SubCommand('sync', self.session, {'nargs': 2})
        s3_command(['help'], [])
        self.assert_contains('sync')
        self.assert_contains("Synopsis")


class TestLSCommand(unittest.TestCase):
    def setUp(self):
        self.session = mock.Mock()
        self.session.get_service.return_value.get_operation.return_value\
                .call.return_value = (None, {'Buckets': []})
        self.session.get_service.return_value.get_operation.return_value\
                .paginate.return_value = [
                    (None, {'Contents': [], 'CommonPrefixes': []})]

    def test_ls_command_with_no_args(self):
        options = {'default': 's3://', 'nargs': '?'}
        ls_command = ListCommand('ls', self.session, options)
        parsed_args = FakeArgs(region=None, endpoint_url=None, verify_ssl=None)
        ls_command([], parsed_args)
        # We should only be a single call.
        self.session.get_service.return_value.get_operation.assert_called_with(
            'ListBuckets')
        call = self.session.get_service.return_value.get_operation\
                .return_value.call
        self.assertEqual(call.call_count, 1)
        self.assertEqual(call.call_args[1], {})
        # Verify get_endpoint
        get_endpoint = self.session.get_service.return_value.get_endpoint
        args = get_endpoint.call_args
        self.assertEqual(args, mock.call(region_name=None, endpoint_url=None,
                                         verify=None))

    def test_ls_with_verify_argument(self):
        options = {'default': 's3://', 'nargs': '?'}
        ls_command = ListCommand('ls', self.session, options)
        parsed_args = FakeArgs(region='us-west-2', endpoint_url=None, verify_ssl=False)
        ls_command([], parsed_args)
        # Verify get_endpoint
        get_endpoint = self.session.get_service.return_value.get_endpoint
        args = get_endpoint.call_args
        self.assertEqual(args, mock.call(region_name='us-west-2', endpoint_url=None,
                                         verify=False))

    def test_ls_command_for_bucket(self):
        options = {'default': 's3://', 'nargs': '?'}
        ls_command = ListCommand('ls', self.session, options)
        ls_command(['s3://mybucket/'], mock.Mock())
        call = self.session.get_service.return_value.get_operation\
                .return_value.call
        paginate = self.session.get_service.return_value.get_operation\
                .return_value.paginate
        # We should make no operation calls.
        self.assertEqual(call.call_count, 0)
        # And only a single pagination call to ListObjects.
        self.session.get_service.return_value.get_operation.assert_called_with(
            'ListObjects')
        self.assertEqual(
            paginate.call_args[1], {'bucket': u'mybucket',
                                    'delimiter': '/', 'prefix': u''})


if __name__ == "__main__":
    unittest.main()
