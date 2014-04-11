# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


from awscli.customizations.commands import BasicCommand
from awscli.clidriver import CLIOperationCaller

import constants
import emrutils
import steputils
import hbaseutils
import argumentschema
import helptext
import exceptions
import applicationutils
import instancegroupsutils


class CreateCluster(BasicCommand):
    NAME = 'create-cluster'
    DESCRIPTION = ('Creates and starts running an EMR cluster.')
    ARG_TABLE = [
        {'name': 'name',
         'default': 'Development Cluster',
         'help_text': helptext.CLUSTER_NAME},
        {'name': 'log-uri',
         'help_text': helptext.LOG_URI},
        {'name': 'ami-version',
         'default': 'latest',
         'help_text': helptext.AMI_VERSION},
        {'name': 'instance-groups',
         'required': True,
         'schema': argumentschema.INSTANCE_GROUPS_SCHEMA,
         'help_text': helptext.INSTANCE_GROUPS},
        {'name': 'additional-info'},
        {'name': 'ec2-attributes',
         'help_text': helptext.EC2_ATTRIBUTES,
         'schema': argumentschema.EC2_ATTRIBUTES_SCHEMA},
        {'name': 'auto-terminate', 'action': 'store_true',
         'group_name': 'auto_terminate',
         'help_text': helptext.AUTO_TERMINATE},
        {'name': 'no-auto-terminate', 'action': 'store_true',
         'group_name': 'auto_terminate'},
        {'name': 'termination-protected', 'action': 'store_true',
         'group_name': 'termination_protected',
         'help_text': helptext.TERMINATION_PROTECTED},
        {'name': 'no-termination-protected', 'action': 'store_true',
         'group_name': 'termination_protected'},
        {'name': 'visible-to-all-users', 'action': 'store_true',
         'group_name': 'visibility',
         'help_text': helptext.VISIBILITY},
        {'name': 'no-visible-to-all-users', 'action': 'store_true',
         'group_name': 'visibility'},
        {'name': 'enable-debugging', 'action': 'store_true',
         'group_name': 'debug',
         'help_text': helptext.DEBUGGING},
        {'name': 'no-enable-debugging', 'action': 'store_true',
         'group_name': 'debug'},
        {'name': 'tags', 'nargs': '+',
         'help_text': helptext.TAGS},
        {'name': 'bootstrap-actions',
         'help_text': helptext.BOOTSTRAP_ACTIONS,
         'schema': argumentschema.BOOTSTRAP_ACTIONS_SCHEMA},
        {'name': 'applications',
         'help_text': helptext.APPLICATIONS,
         'schema': argumentschema.APPLICATIONS_SCHEMA},
        {'name': 'steps',
         'schema': argumentschema.STEPS_SCHEMA,
         'help_text': helptext.STEPS},
        {'name': 'restore-from-hbase-backup',
         'schema': argumentschema.HBASE_RESTORE_FROM_BACKUP_SCHEMA,
         'help_text': helptext.RESTORE_FROM_HBASE}
    ]

    def _run_main(self, parsed_args, parsed_globals):
        emr = self._session.get_service('emr')
        params = {}
        bootstrap_actions = []
        params['Name'] = parsed_args.name
        params['AmiVersion'] = parsed_args.ami_version

        emrutils.apply_dict(
            params, 'AdditionalInfo', parsed_args.additional_info)
        emrutils.apply_dict(params, 'LogUri', parsed_args.log_uri)
        instances_config = {}
        instances_config['InstanceGroups'] = \
            instancegroupsutils.build_instance_groups(
                parsed_args.instance_groups)

        if (
                parsed_args.no_auto_terminate is False and
                parsed_args.auto_terminate is False):
            raise exceptions.\
                MissingBooleanOptionsError(
                    true_option='--auto-terminate',
                    false_option='--no-auto-terminate')

        instances_config['KeepJobFlowAliveWhenNoSteps'] = \
            emrutils.apply_boolean_options(
                parsed_args.no_auto_terminate,
                '--no-auto-terminate',
                parsed_args.auto_terminate,
                '--auto-terminate')

        instances_config['TerminationProtected'] = \
            emrutils.apply_boolean_options(
                parsed_args.termination_protected,
                '--termination-protected',
                parsed_args.no_termination_protected,
                '--no-termination-protected')

        params['VisibleToAllUsers'] = \
            emrutils.apply_boolean_options(
                parsed_args.visible_to_all_users,
                '--visible-to-all-users',
                parsed_args.no_visible_to_all_users,
                '--no-visible-to-all-users')

        params['Tags'] = emrutils.parse_tags(parsed_args.tags)
        params['Instances'] = instances_config

        if parsed_args.ec2_attributes is not None:
            self._build_ec2_attributes(
                cluster=params, parsed_attrs=parsed_args.ec2_attributes)

        debugging_enabled = emrutils.apply_boolean_options(
            parsed_args.enable_debugging,
            '--enable-debugging',
            parsed_args.no_enable_debugging,
            '--no-enable-debugging')

        if parsed_args.log_uri is None and debugging_enabled is True:
            raise exceptions.LogUriError

        if debugging_enabled is True:
            self._update_cluster_dict(
                cluster=params,
                key='Steps',
                value=[self._build_enable_debugging(parsed_globals)])

        if parsed_args.applications is not None:
            app_list, ba_list, step_list = applicationutils.build_applications(
                parsed_applications=parsed_args.applications,
                parsed_globals=parsed_globals,
                ami_version=params['AmiVersion'])
            self._update_cluster_dict(
                params, 'NewSupportedProducts', app_list)
            self._update_cluster_dict(
                params, 'BootstrapActions', ba_list)
            self._update_cluster_dict(
                params, 'Steps', step_list)

        hbase_restore_config = parsed_args.restore_from_hbase_backup
        if hbase_restore_config is not None:
            args = hbaseutils.build_hbase_restore_from_backup_args(
                dir=hbase_restore_config.get('Dir'),
                backup_version=hbase_restore_config.get('BackupVersion'))
            step_config = emrutils.build_step(
                jar=constants.HBASE_JAR_PATH,
                name=constants.HBASE_RESTORE_STEP_NAME,
                action_on_failure=constants.CANCEL_AND_WAIT,
                args=args)
            self._update_cluster_dict(
                params, 'Steps', [step_config])

        if parsed_args.bootstrap_actions is not None:
            self._build_bootstrap_actions(
                cluster=params,
                parsed_boostrap_actions=parsed_args.bootstrap_actions)

        if parsed_args.steps is not None:
            steps_list = steputils.build_step_config_list(
                parsed_step_list=parsed_args.steps,
                region=parsed_globals.region)
            self._update_cluster_dict(
                cluster=params, key='Steps', value=steps_list)
        cli_operation_caller = CLIOperationCaller(self._session)
        cli_operation_caller.invoke(
            emr.get_operation('RunJobFlow'), params, parsed_globals)

        return 0

    def _build_instance_groups(self, parsed_instance_groups):
        instance_groups = []
        for instance_group in parsed_instance_groups:

            emrutils.check_required_field(
                structure='InstanceGroupConfig',
                name='InstanceGroupType',
                value=instance_group.get('InstanceGroupType'))
            emrutils.check_required_field(
                structure='InstanceGroupConfig',
                name='InstanceType',
                value=instance_group.get('InstanceType'))
            emrutils.check_required_field(
                structure='InstanceGroupConfig',
                name='InstanceCount',
                value=instance_group.get('InstanceCount'))
            ig_config = {}
            keys = instance_group.keys()
            if 'Name' in keys:
                ig_config['Name'] = instance_group['Name']
            else:
                ig_config['Name'] = instance_group['InstanceGroupType']
            ig_config['InstanceType'] = instance_group['InstanceType']
            ig_config['InstanceCount'] = instance_group['InstanceCount']
            ig_config['InstanceRole'] = instance_group['InstanceGroupType']
            if 'BidPrice' in keys:
                ig_config['BidPrice'] = instance_group['BidPrice']
                ig_config['Market'] = constants.SPOT
            else:
                ig_config['Market'] = constants.ON_DEMAND
            instance_groups.append(ig_config)

        return instance_groups

    def _build_ec2_attributes(self, cluster, parsed_attrs):
        keys = parsed_attrs.keys()
        instances = cluster['Instances']
        if 'AvailabilityZone' in keys and 'SubnetId' in keys:
            raise exceptions.SubnetAndAzValidationError

        emrutils.apply_params(
            src_params=parsed_attrs, src_key='KeyName',
            dest_params=instances, dest_key='Ec2KeyName')
        emrutils.apply_params(
            src_params=parsed_attrs, src_key='SubnetId',
            dest_params=instances, dest_key='Ec2SubnetId')

        if 'AvailabilityZone' in keys:
            instances['Placement'] = dict()
            emrutils.apply_params(
                src_params=parsed_attrs, src_key='AvailabilityZone',
                dest_params=instances['Placement'],
                dest_key='AvailabilityZone')

        emrutils.apply_params(
            src_params=parsed_attrs, src_key='InstanceProfile',
            dest_params=cluster, dest_key='JobFlowRole')

        emrutils.apply(params=cluster, key='Instances', value=instances)

        return cluster

    def _build_bootstrap_actions(
            self, cluster, parsed_boostrap_actions):
        cluster_ba_list = cluster.get('BootstrapActions')
        if cluster_ba_list is None:
            cluster_ba_list = []

        bootstrap_actions = []
        if len(cluster_ba_list) + len(parsed_boostrap_actions) \
                > constants.MAX_BOOTSTRAP_ACTION_NUMBER:
            raise ValueError('aws: error: maximum number of '
                             'bootstrap actions for a cluster exceeded.')

        for ba in parsed_boostrap_actions:
            ba_config = {}
            if ba.get('Name') is not None:
                ba_config['Name'] = ba.get('Name')
            else:
                ba_config['Name'] = constants.BOOTSTRAP_ACTION_NAME
            script_arg_config = {}
            emrutils.apply_params(
                src_params=ba, src_key='Path',
                dest_params=script_arg_config, dest_key='Path')
            emrutils.apply_params(
                src_params=ba, src_key='Args',
                dest_params=script_arg_config, dest_key='Args')
            emrutils.apply(
                params=ba_config,
                key='ScriptBootstrapAction',
                value=script_arg_config)
            bootstrap_actions.append(ba_config)

        result = cluster_ba_list + bootstrap_actions
        if len(result) > 0:
            cluster['BootstrapActions'] = result

        return cluster

    def _build_enable_debugging(self, parsed_globals):
        return emrutils.build_step(
            name=constants.DEBUGGING_NAME,
            action_on_failure=constants.TERMINATE_CLUSTER,
            jar=emrutils.get_script_runner(),
            args=[emrutils.build_s3_link(
                relative_path=constants.DEBUGGING_PATH,
                region=parsed_globals.region)])

    def _update_cluster_dict(self, cluster, key, value):
        if key in cluster.keys():
            cluster[key] += value
        elif value is not None and len(value) > 0:
            cluster[key] = value
        return cluster
