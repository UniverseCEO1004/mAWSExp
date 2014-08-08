# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
"""Abstractions for CLI arguments.

This module contains abstractions for representing CLI arguments.
This includes how the CLI argument parser is created, how arguments
are serialized, and how arguments are bound (if at all) to operation
arguments.

The BaseCLIArgument is the interface for all arguments.  This is the interface
expected by objects that work with arguments.  If you want to implement your
own argument subclass, make sure it implements everything in BaseCLIArgument.

Arguments generally fall into one of several categories:

* global argument.  These arguments may influence what the CLI does,
  but aren't part of the input parameters needed to make an API call.  For
  example, the ``--region`` argument specifies which region to send the request
  to.  The ``--output`` argument specifies how to display the response to the
  user.  The ``--query`` argument specifies how to select specific elements
  from a response.
* operation argument.  These are arguments that influence the parameters we
  send to a service when making an API call.  Some of these arguments are
  automatically created directly from introspecting the JSON service model.
  Sometimes customizations may provide a pseudo-argument that takes the
  user input and maps the input value to several API parameters.

"""
import logging

from botocore import xform_name
from botocore.parameters import ListParameter, StructParameter

from awscli.argprocess import unpack_cli_arg
from awscli.schema import SchemaTransformer


LOG = logging.getLogger('awscli.arguments')


class UnknownArgumentError(Exception):
    pass


class BaseCLIArgument(object):
    """Interface for CLI argument.

    This class represents the interface used for representing CLI
    arguments.

    """

    def __init__(self, name):
        self._name = name

    def add_to_arg_table(self, argument_table):
        """Add this object to the argument_table.

        The ``argument_table`` represents the argument for the operation.
        This is called by the ``ServiceOperation`` object to create the
        arguments associated with the operation.

        :type argument_table: dict
        :param argument_table: The argument table.  The key is the argument
            name, and the value is an object implementing this interface.
        """
        argument_table[self.name] = self

    def add_to_parser(self, parser):
        """Add this object to the parser instance.

        This method is called by the associated ``ArgumentParser``
        instance.  This method should make the relevant calls
        to ``add_argument`` to add itself to the argparser.

        :type parser: ``argparse.ArgumentParser``.
        :param parser: The argument parser associated with the operation.

        """
        pass

    def add_to_params(self, parameters, value):
        """Add this object to the parameters dict.

        This method is responsible for taking the value specified
        on the command line, and deciding how that corresponds to
        parameters used by the service/operation.

        :type parameters: dict
        :param parameters: The parameters dictionary that will be
            given to ``botocore``.  This should match up to the
            parameters associated with the particular operation.

        :param value: The value associated with the CLI option.

        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def cli_name(self):
        return '--' + self._name

    @property
    def cli_type_name(self):
        raise NotImplementedError("cli_type_name")

    @property
    def required(self):
        raise NotImplementedError("required")

    @property
    def documentation(self):
        raise NotImplementedError("documentation")

    @property
    def cli_type(self):
        raise NotImplementedError("cli_type")

    @property
    def py_name(self):
        return self._name.replace('-', '_')

    @property
    def choices(self):
        """List valid choices for argument value.

        If this value is not None then this should return a list of valid
        values for the argument.

        """
        return None

    @property
    def synopsis(self):
        return None

    @property
    def positional_arg(self):
        return None

    @property
    def nargs(self):
        return None

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group_name(self):
        """Get the group name associated with the argument.

        An argument can be part of a group.  This property will
        return the name of that group.

        This base class has no default behavior for groups, code
        that consumes argument objects can use them for whatever
        purposes they like (documentation, mutually exclusive group
        validation, etc.).

        """
        return None


class CustomArgument(BaseCLIArgument):
    """
    Represents a CLI argument that is configured from a dictionary.

    For example, the "top level" arguments used for the CLI
    (--region, --output) can use a CustomArgument argument,
    as these are described in the cli.json file as dictionaries.

    This class is also useful for plugins/customizations that want to
    add additional args.

    """

    def __init__(self, name, help_text='', dest=None, default=None,
                 action=None, required=None, choices=None, nargs=None,
                 cli_type_name=None, group_name=None, positional_arg=False,
                 no_paramfile=False, schema=None, synopsis=None):
        self._name = name
        self._help = help_text
        self._dest = dest
        self._default = default
        self._action = action
        self._required = required
        self._nargs = nargs
        self._cli_type_name = cli_type_name
        self._group_name = group_name
        self._positional_arg = positional_arg
        if choices is None:
            choices = []
        self._choices = choices
        self.no_paramfile = no_paramfile
        self._schema = schema
        self._synopsis = synopsis

        # If the top level element is a list then set nargs to
        # accept multiple values seperated by a space.
        if self._schema and self._schema.get('type', None) == 'array':
            self._nargs = '+'

        # TODO: We should eliminate this altogether.
        # You should not have to depend on an argument_object
        # as part of the interface.  Currently the argprocess
        # and docs code relies on this object.
        self.argument_object = None

    @property
    def cli_name(self):
        if self._positional_arg:
            return self._name
        else:
            return '--' + self._name

    def add_to_parser(self, parser):
        """

        See the ``BaseCLIArgument.add_to_parser`` docs for more information.

        """
        cli_name = self.cli_name
        kwargs = {}
        if self._dest is not None:
            kwargs['dest'] = self._dest
        if self._action is not None:
            kwargs['action'] = self._action
        if self._default is not None:
            kwargs['default'] = self._default
        if self._choices:
            kwargs['choices'] = self._choices
        if self._required is not None:
            kwargs['required'] = self._required
        if self._nargs is not None:
            kwargs['nargs'] = self._nargs
        parser.add_argument(cli_name, **kwargs)

    def create_argument_object(self):
        """
        Create an argument object based on the JSON schema if one is set.
        After calling this method, ``parameter.argument_object`` is available
        e.g. for generating docs.
        """
        transformer = SchemaTransformer(self._schema)
        transformed = transformer.transform()

        # Set the parameter name from the parsed arg key name
        transformed.update({'name': self.name})

        LOG.debug('Custom parameter schema for {0}: {1}'.format(
            self.name, transformed))

        # Select the correct top level type
        if transformed['type'] == 'structure':
            self.argument_object = StructParameter(None, **transformed)
        elif transformed['type'] == 'list':
            self.argument_object = ListParameter(None, **transformed)
        else:
            raise ValueError('Invalid top level type {0}!'.format(
                transformed['type']))

    @property
    def required(self):
        if self._required is None:
            return False
        return self._required

    @required.setter
    def required(self, value):
        self._required = value

    @property
    def documentation(self):
        return self._help

    @property
    def cli_type_name(self):
        if self._cli_type_name is not None:
            return self._cli_type_name
        elif self._action in ['store_true', 'store_false']:
            return 'boolean'
        elif self.argument_object is not None:
            return self.argument_object.type
        else:
            # Default to 'string' type if we don't have any
            # other info.
            return 'string'

    @property
    def cli_type(self):
        cli_type = str
        if self._action in ['store_true', 'store_false']:
            cli_type = bool
        return cli_type

    @property
    def choices(self):
        return self._choices

    @property
    def group_name(self):
        return self._group_name

    @property
    def synopsis(self):
        return self._synopsis

    @property
    def positional_arg(self):
        return self._positional_arg

    @property
    def nargs(self):
        return self._nargs


class CLIArgument(BaseCLIArgument):
    """Represents a CLI argument that maps to a service parameter.

    """

    TYPE_MAP = {
        'structure': str,
        'map': str,
        'timestamp': str,
        'list': str,
        'string': str,
        'float': float,
        'integer': str,
        'long': int,
        'boolean': bool,
        'double': float,
        'blob': str
    }

    def __init__(self, name, argument_object, operation_object):
        """

        :type name: str
        :param name: The name of the argument in "cli" form
            (e.g.  ``min-instances``).

        :type argument_object: ``botocore.parameter.Parameter``
        :param argument_object: The parameter object to associate with
            this object.

        :type operation_object: ``botocore.operation.Operation``
        :param operation_object: The operation object associated with
            this object.

        """
        self._name = name
        self.argument_object = argument_object
        self.operation_object = operation_object

    @property
    def py_name(self):
        return self._name.replace('-', '_')

    @property
    def required(self):
        return self.argument_object.required

    @required.setter
    def required(self, value):
        self.argument_object.required = value

    @property
    def documentation(self):
        return self.argument_object.documentation

    @property
    def cli_type_name(self):
        return self.argument_object.type

    @property
    def cli_type(self):
        return self.TYPE_MAP.get(self.argument_object.type, str)

    def add_to_parser(self, parser):
        """

        See the ``BaseCLIArgument.add_to_parser`` docs for more information.

        """
        cli_name = self.cli_name
        parser.add_argument(
            cli_name,
            help=self.documentation,
            type=self.cli_type,
            required=self.required)

    def add_to_params(self, parameters, value):
        if value is None:
            return
        else:
            # This is a two step process.  First is the process of converting
            # the command line value into a python value.  Normally this is
            # handled by argparse directly, but there are cases where extra
            # processing is needed.  For example, "--foo name=value" the value
            # can be converted from "name=value" to {"name": "value"}.  This is
            # referred to as the "unpacking" process.  Once we've unpacked the
            # argument value, we have to decide how this is converted into
            # something that can be consumed by botocore.  Many times this is
            # just associating the key and value in the params dict as down
            # below.  Sometimes this can be more complicated, and subclasses
            # can customize as they need.
            unpacked = self._unpack_argument(value)
            LOG.debug('Unpacked value of "%s" for parameter "%s": %s', value,
                      self.argument_object.py_name, unpacked)
            parameters[self.argument_object.py_name] = unpacked

    def _unpack_argument(self, value):
        service_name = self.operation_object.service.endpoint_prefix
        operation_name = xform_name(self.operation_object.name, '-')
        override = self._emit_first_response('process-cli-arg.%s.%s' % (
            service_name, operation_name), param=self.argument_object,
            value=value,
            operation=self.operation_object)
        if override is not None:
            # A plugin supplied an alternate conversion,
            # use it instead.
            return override
        else:
            # Fall back to the default arg processing.
            return unpack_cli_arg(self.argument_object, value)

    def _emit(self, name, **kwargs):
        session = self.operation_object.service.session
        return session.emit(name, **kwargs)

    def _emit_first_response(self, name, **kwargs):
        session = self.operation_object.service.session
        return session.emit_first_non_none_response(name, **kwargs)


class ListArgument(CLIArgument):

    def add_to_parser(self, parser):
        cli_name = self.cli_name
        parser.add_argument(cli_name,
                            nargs='*',
                            type=self.cli_type,
                            required=self.required)


class BooleanArgument(CLIArgument):
    """Represent a boolean CLI argument.

    A boolean parameter is specified without a value::

        aws foo bar --enabled

    For cases wher the boolean parameter is required we need to add
    two parameters::

        aws foo bar --enabled
        aws foo bar --no-enabled

    We use the capabilities of the CLIArgument to help achieve this.

    """

    def __init__(self, name, argument_object, operation_object,
                 action='store_true', dest=None, group_name=None,
                 default=None):
        super(BooleanArgument, self).__init__(name, argument_object,
                                              operation_object)
        self._mutex_group = None
        self._action = action
        if dest is None:
            self._destination = self.py_name
        else:
            self._destination = dest
        if group_name is None:
            self._group_name = self.name
        else:
            self._group_name = group_name
        self._default = default

    def add_to_params(self, parameters, value):
        # If a value was explicitly specified (so value is True/False
        # but *not* None) then we add it to the params dict.
        # If the value was not explicitly set (value is None)
        # we don't add it to the params dict.
        if value is not None:
            parameters[self.py_name] = value

    def add_to_arg_table(self, argument_table):
        # Boolean parameters are a bit tricky.  For a single boolean parameter
        # we actually want two CLI params, a --foo, and a --no-foo.  To do this
        # we need to add two entries to the argument table.  So we can add
        # ourself as the positive option (--no), and then create a clone of
        # ourselves for the negative service.  We then insert both into the
        # arg table.
        argument_table[self.name] = self
        negative_name = 'no-%s' % self.name
        negative_version = self.__class__(negative_name, self.argument_object,
                                          self.operation_object,
                                          action='store_false',
                                          dest=self._destination,
                                          group_name=self.group_name)
        argument_table[negative_name] = negative_version

    def add_to_parser(self, parser):
        parser.add_argument(self.cli_name,
                            help=self.documentation,
                            action=self._action,
                            default=self._default,
                            dest=self._destination)

    @property
    def group_name(self):
        return self._group_name
