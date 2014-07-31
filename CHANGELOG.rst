=========
CHANGELOG
=========


1.3.25
======

* bugfix:``aws ec2 describe-network-interface-attribute``: Fix issue where
  the model for the ``aws ec2 describe-network-interface-attribute`` was
  incorrect
  (`issue 558 <https://github.com/aws/aws-cli/issues/558>`__)
* bugfix:``aws s3``: Add option to not follow symlinks via
  ``--[no]-follow-symlinks``.  Note that the default behavior of following
  symlinks is left unchanged.
  (`issue 854 <https://github.com/aws/aws-cli/pull/854>`__,
   `issue 453 <https://github.com/aws/aws-cli/issues/453>`__,
   `issue 781 <https://github.com/aws/aws-cli/issues/781>`__)
* bugfix:``aws route53 change-tags-for-resource``: Fix serialization issue
  for ``aws route53 change-tags-for-resource``
  (`botocore issue 328 <https://github.com/boto/botocore/pull/328>`__)
* bugfix:``aws ec2 describe-network-interface-attribute``: Update parameters
  to add the ``--attribute`` argument
  (`botocore issue 327 <https://github.com/boto/botocore/pull/327>`__)
* feature:``aws autoscaling``: Update command to the latest version
* feature:``aws elasticache``: Update command to the latest version
* feature:``aws route53``: Update command to the latest version
* feature:``aws route53domains``: Add support for Amazon Route53 Domains


1.3.24
======

* feature:``aws elasticloadbalancing``: Update to the latest service model.
* bugfix:``aws swf poll-for-decision-task``: Fix issue where
  the default paginated response is missing output response keys
  (`issue botocore 324 <https://github.com/boto/botocore/pull/324>`__)
* bugfix:Connections: Fix issue where connections were hanging
  when network issues occurred
  `issue botocore 325 <https://github.com/boto/botocore/pull/325>`__)
* bugfix:``aws s3/s3api``: Fix issue where Deprecations were being
  written to stderr in Python 3.4.1
  `issue botocore 319 <https://github.com/boto/botocore/issues/319>`__)


1.3.23
======

* feature:``aws support``: Update ``aws support`` command to
  the latest version
* feature:``aws iam``: Update ``aws iam`` command to the latest
  version
* feature:``aws emr``: Add ``--hive-site`` option to
  ``aws emr create-cluster`` and ``aws emr install-application`` commands
* feature:``aws s3 sync``: Add an ``--exact-timestamps`` option
  to the ``aws s3 sync`` command
  (`issue 824 <https://github.com/aws/aws-cli/pull/824>`__)
* bugfix:``aws ec2 copy-snapshot``: Fix bug when spaces in
  the description caused the copy request to fail
  (`issue botocore 321 <https://github.com/boto/botocore/pull/321>`__)


1.3.22
======

* feature:``aws cwlogs``: Add support for Amazon CloudWatch Logs
* feature:``aws cognito-sync``: Add support for
  Amazon Cognito Service
* feature:``aws cognito-identity``: Add support for
  Amazon Cognito Identity Service
* feature:``aws route53``: Update ``aws route53`` command to the
  latest version
* feature:``aws ec2``: Update ``aws ec2`` command to the
  latest version
* bugfix:``aws s3/s3api``: Fix issue where ``--endpoint-url``
  wasn't being used for ``aws s3/s3api`` commands
  (`issue 549 <https://github.com/aws/aws-cli/issues/549>`__)
* bugfix:``aws s3 mv``: Fix bug where using the ``aws s3 mv``
  command to move a large file onto itself results in the
  file being deleted
  (`issue 831 <https://github.com/aws/aws-cli/issues/831>`__)
* bugfix:``aws s3``: Fix issue where parts in a multipart
  upload are stil being uploaded when a part has failed
  (`issue 834 <https://github.com/aws/aws-cli/issues/834>`__)
* bugfix:Windows: Fix issue where ``python.exe`` is on a path
  that contains spaces
  (`issue 825 <https://github.com/aws/aws-cli/pull/825>`__)


1.3.21
======

* feature:``aws opsworks``: Update the ``aws opsworks`` command
  to the latest version
* bugfix:Shorthand JSON: Fix bug where shorthand lists with
  a single item (e.g. ``--arg Param=[item]``) were not parsed
  correctly.
  (`issue 830 <https://github.com/aws/aws-cli/pull/830>`__)
* bugfix:Text output: Fix bug when rendering only
  scalars that are numbers in text output
  (`issue 829 <https://github.com/aws/aws-cli/pull/829>`__)
* bugfix:``aws cloudsearchdomain``: Fix bug where
  ``--endpoint-url`` is required even for ``help`` subcommands
  (`issue 828 <https://github.com/aws/aws-cli/pull/828>`__)


1.3.20
======

* feature:``aws cloudsearchdomain``: Add support for the
  Amazon CloudSearch Domain command.
* feature:``aws cloudfront``: Update the Amazon CloudFront
  command to the latest version


1.3.19
======

* feature:``aws ses``: Add support for delivery notifications
* bugfix:Region Config: Fix issue for ``cn-north-1`` region
  (`issue botocore 314 <https://github.com/boto/botocore/pull/314>`__)
* bugfix:Amazon EC2 Credential File: Fix regression for parsing
  EC2 credential file
  (`issue botocore 315 <https://github.com/boto/botocore/pull/315>`__)
* bugfix:Signature Version 2: Fix timestamp format when calculating
  signature version 2 signatures
  (`issue botocore 308 <https://github.com/boto/botocore/pull/308>`__)


1.3.18
======

* feature:``aws configure``: Add support for setting nested attributes
  (`issue 817 <https://github.com/aws/aws-cli/pull/817>`__)
* bugfix:``aws s3``: Fix issue when uploading large files to newly
  created buckets in a non-standard region
  (`issue 634 <https://github.com/aws/aws-cli/issues/634>`__)
* feature:``aws dynamodb``: Add support for a ``local`` region for
  dynamodb (``aws dynamodb --region local ...``)
  (`issue 608 <https://github.com/aws/aws-cli/issues/608>`__)
* feature:``aws elasticbeanstalk``: Update ``aws elasticbeanstalk``
  model to the latest version
* feature:Documentation Examples: Add more documentatoin examples for many
  AWS CLI commands
* feature:``aws emr``: Update model to the latest version
* feature:``aws elastictranscoder:`` Update model to the latest version


1.3.17
======

* feature:``aws s3api``: Add support for server-side encryption with
  a customer-supplied encryption key.
* feature:``aws sns``: Support for message attributes.
* feature:``aws redshift``: Support for renaming clusters.


1.3.16
======

* bugfix:``aws s3``: Fix bug related to retrying requests
  when 500 status codes are received
  (`issue botocore 302 <https://github.com/boto/botocore/pull/302>`__)
* bugfix:``aws s3``: Fix when when using S3 in the ``cn-north-1`` region
  (`issue botocore 301 <https://github.com/boto/botocore/pull/301>`__)
* bugfix:``aws kinesis``: Fix pagination bug when using the ``get-records``
  operation
  (`issue botocore 304 <https://github.com/boto/botocore/pull/304>`__)


1.3.15
======

* bugfix:Python 3.4.1:  Add support for python 3.4.1
  (`issue 800 <https://github.com/aws/aws-cli/issues/800>`__)
* feature:``aws emr``: Update preview commands for Amazon
  Elastic MapReduce


1.3.14
======

* bugfix:``aws s3``: Add filename to error message when we're unable
  to stat local filename
  (`issue 795 <https://github.com/aws/aws-cli/pull/795>`__)
* bugfix:``aws s3api get-bucket-policy``: Fix response parsing
  for the ``aws s3api get-bucket-policy`` command
  (`issue 678 <https://github.com/aws/aws-cli/issues/678>`__)
* bugfix:Shared Credentials: Fix bug when specifying profiles
  that don't exist in the CLI config file
  (`issue botocore 294 <https://github.com/boto/botocore/pull/294>`__)
* bugfix:``aws s3``: Handle Amazon S3 error responses that have
  a 200 OK status code
  (`issue botocore 298 <https://github.com/boto/botocore/pull/298>`__)
* feature:``aws sts``:  Update the ``aws sts`` command to the latest
  version
* feature:``aws cloudsearch``:  Update the ``aws cloudsearch`` command to the
  latest version


1.3.13
======

* feature:Shorthand: Add support for surrounding list parameters
  with ``[]`` chars in shorthand syntax
  (`issue 788 <https://github.com/aws/aws-cli/pull/788>`__)
* feature:Shared credential file: Add support for the
  ``~/.aws/credentials`` file
* feature:``aws ec2``: Add support for Amazon EBS encryption


1.3.12
======

* bugfix:``aws s3``: Fix issue when ``--delete`` and ``--exclude``
  filters are used together
  (`issue 778 <https://github.com/aws/aws-cli/issues/778>`__)
* feature:``aws route53``: Update ``aws route53`` to the latest
  model
* bugfix:``aws emr``: Fix issue with ``aws emr`` retry logic not
  being applied correctly
  (`botocore issue 285 <https://github.com/boto/botocore/pull/285>`__)


1.3.11
======

* feature:``aws cloudtrail``: Add support for eu-west-1, ap-southeast-2,
  and eu-west-1 regions
* bugfix:``aws ec2``:  Fix issue when specifying user data from a file
  containing non-ascii characters
  (`issue 765 <https://github.com/aws/aws-cli/issues/765>`__)
* bugfix:``aws cloudtrail``: Fix a bug with python3 when creating a
  subscription
  (`issue 773 <https://github.com/aws/aws-cli/pull/773>`__)
* bugfix:Shorthand: Fix issue where certain shorthand parameters were
  not parsing to the correct types
  (`issue 776 <https://github.com/aws/aws-cli/pull/776>`__)
* bugfix:``aws cloudformation``: Fix issue with parameter casing for
  the ``NotificationARNs`` parameter
  (`botocore issue 283 <https://github.com/boto/botocore/pull/283>`__)


1.3.10
======

* feature:``aws cloudformation``: Add support for updated API

1.3.9
=====

* feature:``aws sqs``: Add support for message attributes
* bugfix:``aws s3api``: Fix issue when setting metadata on an S3 object
  (`issue 356 <https://github.com/aws/aws-cli/issues/356>`__)

1.3.8
=====

* feature:``aws autoscaling``: Add support for launching Dedicated Instances
  in Amazon Virtual Private Cloud
* feature:``aws elasticache``: Add support to backup and restore for Redis
  clusters
* feature:``aws dynamodb``: Update ``aws dynamodb`` command to the latest API

1.3.7
=====

* bugfix:Output Format: Fix issue with encoding errors when
  using text and table output and redirecting to a pipe or file
  (`issue 742 <https://github.com/aws/aws-cli/issues/742>`__)
* bugfix:``aws s3``: Fix issue with sync re-uploading certain
  files
  (`issue 749 <https://github.com/aws/aws-cli/issues/749>`__)
* bugfix:Text Output: Fix issue with inconsistent text output
  based on order
  (`issue 751 <https://github.com/aws/aws-cli/issues/751>`__)
* bugfix:``aws datapipeline``: Fix issue for aggregating keys into
  a list when calling ``aws datapipeline get-pipeline-definition``
  (`issue 750 <https://github.com/aws/aws-cli/pull/750>`__)
* bugfix:``aws s3``: Fix issue when running out of disk
  space during ``aws s3`` transfers
  (`issue 739 <https://github.com/aws/aws-cli/issues/739>`__)
* feature:``aws s3 sync``: Add ``--size-only`` param to the
  ``aws s3 sync`` command
  (`issue 472 <https://github.com/aws/aws-cli/issues/473>`__,
   `issue 719 <https://github.com/aws/aws-cli/pull/719>`__)


1.3.6
=====

* bugfix:``aws cloudtrail``: Fix issue when using ``create-subscription``
  command
  (`issue botocore 268 <https://github.com/boto/botocore/pull/268>`__)
* feature:``aws cloudsearch``: Amazon CloudSearch has moved out of preview
  (`issue 730 <https://github.com/aws/aws-cli/pull/730>`__)
* bugfix:``aws s3 website``: Fix issue where ``--error-document`` was being
  ignored in certain cases
  (`issue 714 <https://github.com/aws/aws-cli/pull/714>`__)


1.3.5
=====

* feature:``aws opsworks``: Update ``aws opsworks`` model to the
  latest version
* bugfix:Pagination: Fix issue with ``--max-items`` with ``aws route53``,
  ``aws iam``, and ``aws ses``
  (`issue 729 <https://github.com/aws/aws-cli/pull/729>`__)
* bugfix:``aws s3``: Fix issue with fips-us-gov-west-1 endpoint
  (`issue botocore 265 <https://github.com/boto/botocore/pull/265>`__)
* bugfix:Table Output: Fix issue when displaying unicode
  characters in table output
  (`issue 721 <https://github.com/aws/aws-cli/pull/721>`__)
* bugfix:``aws s3``: Fix regression when syncing files with
  whitespace
  (`issue 706 <https://github.com/aws/aws-cli/issues/706>`__,
   `issue 718 <https://github.com/aws/aws-cli/issues/718>`__)


1.3.4
=====

* bugfix:``aws ec2``: Fix issue with EC2 model resulting in
  responses not being parsed.


1.3.3
=====

* feature:``aws ec2``: Add support for Amazon VPC peering
* feature:``aws redshift``: Add support for the latest Amazon Redshift API
* feature:``aws cloudsearch``: Add support for the latest Amazon CloudSearch
  API
* bugfix:``aws cloudformation``: Documentation updates
* bugfix:Argument Parsing: Fix issue when list arguments were
  not being decoded to unicode properly
  (`issue 711 <https://github.com/aws/aws-cli/issues/711>`__)
* bugfix:Output: Fix issue when invalid output type was provided
  in a config file or environment variable
  (`issue 600 <https://github.com/aws/aws-cli/issues/600>`__)


1.3.2
=====

* bugfix:``aws datapipeline``: Fix issue when serializing
  pipeline definitions containing list elements
  (`issue 705 <https://github.com/aws/aws-cli/issues/705>`__)
* bugfix:``aws s3``: Fix issue when recursively removing keys
  containing control characters
  (`issue 675 <https://github.com/aws/aws-cli/issues/675>`__)
* bugfix:``aws s3``: Honor ``--no-verify-ssl`` in high level
  ``aws s3`` commands
  (`issue 696 <https://github.com/aws/aws-cli/issues/696>`__)


1.3.1
=====

* bugfix:Parameters: Fix issue parsing with CLI
  parameters of type ``long``
  (`issue 693 <https://github.com/aws/aws-cli/pull/693/files>`__)
* bugfix:Pagination: Fix issue where ``--max-items``
  in pagination was always assumed to be an integer
  (`issue 689 <https://github.com/aws/aws-cli/pull/689>`__)
* feature:``aws elb``: Add support for AccessLog
* bugfix:Bundled Installer: Allow creation of bundled
  installer with ``pip 1.5``
  (`issue 691 <https://github.com/aws/aws-cli/issues/691>`__)
* bugfix:``aws s3``: Fix issue when copying objects using
  ``aws s3 cp`` with key names containing ``+`` characters
  (`issue #614 <https://github.com/aws/aws-cli/issues/614>`__)
* bugfix:``ec2 create-snapshot``: Remove ``Tags`` key from
  output response
  (`issue 247 <https://github.com/boto/botocore/pull/247>`__)
* bugfix:``aws s3``: ``aws s3`` commands should not be requiring regions
  (`issue 681 <https://github.com/aws/aws-cli/issues/681>`__)
* bugfix:``CLI Arguments``: Fix issue where unicode command line
  arguments were not being handled correctly
  (`issue 679 <https://github.com/aws/aws-cli/pull/679>`__)


1.3.0
=====

* bugfix:``aws s3``: Fix issue where S3 downloads would hang
  in certain cases and could not be interrupted
  (`issue 650 <https://github.com/aws/aws-cli/issues/650>`__,
   `issue 657 <https://github.com/aws/aws-cli/issues/657>`__)
* bugfix:``aws s3``: Support missing canned ACLs when using
  the ``--acl`` parameter
  (`issue 663 <https://github.com/aws/aws-cli/issues/663>`__)
* bugfix:``aws rds describe-engine-default-parameters``: Fix
  pagination issue when calling
  ``aws rds describe-engine-default-parameters``
  (`issue 607 <https://github.com/aws/aws-cli/issues/607>`__)
* bugfix:``aws cloudtrail``: Merge existing SNS topic policy
  with the existing AWS CloudTrail policy instead of overwriting
  the default topic policy
* bugfix:``aws s3``: Fix issue where streams were not being
  rewound when encountering 307 redirects with multipart uploads
  (`issue 544 <https://github.com/aws/aws-cli/issues/544>`__)
* bugfix:``aws elb``: Fix issue with documentation errors
  in ``aws elb help``
  (`issue 622 <https://github.com/aws/aws-cli/issues/622>`__)
* bugfix:JSON Parameters: Add a more clear error message
  when parsing invalid JSON parameters
  (`issue 639 <https://github.com/aws/aws-cli/pull/639>`__)
* bugfix:``aws s3api``: Properly handle null inputs
  (`issue 637 <https://github.com/aws/aws-cli/issues/637>`__)
* bugfix:Argument Parsing: Handle files containing JSON with
  leading and trailing spaces
  (`issue 640 <https://github.com/aws/aws-cli/pull/640>`__)


1.2.13
======

* feature:``aws route53``: Update ``aws route53`` command to
  support string-match health checks and the UPSERT action for the
  ``aws route53 change-resource-record-sets`` command
* bugfix:Command Completion: Don't show tracebacks on SIGINT
  (`issue 628 <https://github.com/aws/aws-cli/issues/628>`__)
* bugfix:Docs: Don't duplicate enum values in reference docs
  (`issue 632 <https://github.com/aws/aws-cli/pull/632>`__)
* bugfix:``aws s3``: Don't require ``s3://`` prefix
  (`issue 626 <https://github.com/aws/aws-cli/pull/626>`__)


1.2.12
======

* feature:``aws configure``: Add support for ``configure get`` and ``configure
  set`` command which allow you to set and get configuration values from the
  AWS config file (`issue 602 <https://github.com/aws/aws-cli/issues/602`__)
* bugfix:``aws s3``: Fix issue with Amazon S3 downloads on certain OSes
  (`issue 619 <https://github.com/aws/aws-cli/issues/619`__)


1.2.11
======

* Add support for the ``--recursive`` option in the ``aws s3 ls`` command
  (`issue 465 <https://github.com/aws/aws-cli/issues/465`)
* Add support for the ``AWS_CA_BUNDLE`` environment variable so that users
  can specify an alternate path to a cert bundle
  (`issue 586 <https://github.com/aws/aws-cli/pull/586>`__)
* Add ``metadata_service_timeout`` and ``metadata_service_num_attempts``
  config parameters to control behavior when retrieving credentials using
  an IAM role (`issue 597 <https://github.com/aws/aws-cli/pull/597>`__)
* Retry intermittent ``aws s3`` download failures including socket timeouts
  and content length mismatches (`issue 594 <https://github.com/aws/aws-cli/pull/594>`__)
* Fix response parsing of ``aws s3api get-bucket-location``
  (`issue 345 <https://github.com/aws/aws-cli/issues/345>`__)
* Fix response parsing of the ``aws elastictranscoder`` command
  (`issue 207 <https://github.com/boto/botocore/pull/207>`__)
* Update ``aws elasticache`` command to not require certain parameters


1.2.10
======

* Add support for creating launch configuration or Auto Scaling groups
  using an Amazon EC2 instance, for attaching Amazon EC2 isntances to an
  existing Auto Scaling group, and for describing the limits on the Auto
  Scaling resources in the ``aws autoscaling`` command
* Update documentation in the ``aws support`` command
* Allow the ``--protocol`` customization for ``CreateNetworkAclEntry`` to
  also work for ``ReplaceNetworkAclEntry`` (`issue 559 <https://github.com/aws/aws-cli/issues/559>`__)
* Remove one second delay when tasks are finished running for several
  ``aws s3`` subcommands (`issue 551 <https://github.com/aws/aws-cli/pull/551>`__)
* Fix bug in shorthand documentation generation that prevented certain
  nested structure parameters from being fully documented (`issue 579 <https://github.com/aws/aws-cli/pull/579>`__)
* Update default timeout from .1 second to 1 second (`botocore issue 202 <https://github.com/boto/botocore/pull/202>`__)
* Removed filter parameter in RDS operations (`issue 515 <https://github.com/aws/aws-cli/issues/515>`__)
* Fixed region endpoint for the ``aws kinesis`` command (`botocore issue 194 <https://github.com/boto/botocore/pull/194>`__)


1.2.9
=====

* Fix issue 548 where ``--include/--exclude`` arguments for various
  ``aws s3`` commands were prepending the CWD instead of the source
  directory for filter patterns
* Fix issue 552 where a remote location without a trailing slash would
  show a malformed XML error when using various  ``aws s3`` commands
* Add support for tagging in ``aws emr`` command
* Add support for georestrictions in ``aws cloudfront`` command
* Add support for new audio compression codecs in the
  ``aws elastictranscoder`` command
* Update the ``aws cloudtrail`` command to the latest API
* Add support for the new China (Beijing) Region. Note: Although the AWS CLI
  now includes support for the newly announced China (Beijing)
  Region, the service endpoints will not be accessible until the Region’s
  limited preview is launched in early 2014. To find out more about the new
  Region and request a limited preview account, please visit
  http://www.amazonaws.cn/.


1.2.8
=====

* Add support for parallel multipart uploads when copying objects
  between Amazon S3 locations when using the ``aws s3`` command (issue 538)
* Fix issue 542 where the ``---stack-policy-url`` will parameter will not
  interpret its value as a URL when using the
  ``aws cloudformation create-stack`` command
* Add support for global secondary indexes in the ``aws dynamodb`` command
* Add support for the ``aws kinesis`` command
* Add support for worker roles in the ``aws elasticbeanstalk`` command
* Add support for resource tagging and other new operations in the
  ``aws emr`` command
* Add support for resource-based permissions in the
  ``aws opsworks`` command
* Update the ``aws elasticache`` command to signature version 4


1.2.7
=====

* Allow tcp, udp, icmp, all for ``--protocol`` param of
  the ``ec2 create-network-acl-entry`` command
  (`issue 508 <https://github.com/aws/aws-cli/issues/508>`__)
* Fix bug when filtering ``s3://`` locations with the
  ``--include/--exclude`` params
  (`issue 531 <https://github.com/aws/aws-cli/pull/531>`__)
* Fix an issue with map type parameters raising uncaught
  exceptions in commands such as `sns create-platform-application`
  (`issue 407 <https://github.com/aws/aws-cli/issues/407>`__)
* Fix an issue when both ``--private-ip-address`` and
  ``--associate-public-ip-address`` are specified in the
  ``ec2 run-instances`` command
  (`issue 520 <https://github.com/aws/aws-cli/issues/520>`__)
* Fix an issue where ``--output text`` was not providing
  a starting identifier for certain rows
  (`issue 516 <https://github.com/aws/aws-cli/pull/516>`__)
* Update the ``support`` command to the latest version
* Update the ``--query`` syntax to support flattening sublists
  (`boto/jmespath#20 <https://github.com/boto/jmespath/pull/20>`__)


1.2.6
=====

* Allow ``--endpoint-url`` to work with the ``aws s3`` command
  (`issue 469 <https://github.com/aws/aws-cli/pull/469>`__)
* Fix issue with ``aws cloudtrail [create|update]-subscription`` not
  honoring the ``--profile`` argument
  (`issue 494 <https://github.com/aws/aws-cli/issues/494>`__)
* Fix issue with ``--associate-public-ip-address`` when a ``--subnet-id``
  is provided (`issue 501 <https://github.com/aws/aws-cli/issues/501>`__)
* Don't require key names for structures of single scalar values
  (`issue 484 <https://github.com/aws/aws-cli/issues/484>`__)
* Fix issue with symlinks silently failing during ``s3 sync/cp``
  (`issue 425 <https://github.com/aws/aws-cli/issues/425>`__
   and `issue 487 <https://github.com/aws/aws-cli/issues/487>`__)
* Add a ``aws configure list`` command to show where the configuration
  values are sourced from
  (`issue 513 <https://github.com/aws/aws-cli/pull/513>`__)
* Update ``cloudwatch`` command to use Signature Version 4
* Update ``ec2`` command to support enhanced network capabilities and
  pagination controls for ``describe-instances`` and ``describe-tags``
* Add support in ``rds`` command for copying DB snapshots from
  one AWS region to another


1.2.5
=====

* Add support for AWS Cloudtrail
* Add support for identity federation using SAML 2.0 in the ``aws iam`` command
* Update the ``aws redshift`` command to include several new features related to
  event notifications, encryption, audit logging, data load from external hosts,
  WLM configuration, and database distribution styles and functions
* Add a ``--associate-public-ip-address`` option to the ``ec2 run-instances``
  command (`issue 479 <https://github.com/aws/aws-cli/issues/479>`__)
* Add an ``s3 website`` command for configuring website configuration for an S3
  bucket (`issue 482 <https://github.com/aws/aws-cli/pull/482>`__)


1.2.4
=====

* Fix an issue with the ``s3`` command when using GovCloud regions
  (boto/botocore#170)
* Fix an issue with the ``s3 ls`` command making an extra query at the
  root level (issue 439)
* Add detailed error message when unable to decode local filenames during
  an ``s3 sync`` (issue 378)
* Support ``-1`` and ``all`` as valid values to the ``--protocol`` argument
  to ``ec2 authorize-security-group-ingress`` and
  ``ec2 authorize-security-group-egress`` (issue 460)
* Log the reason why a file is synced when using the ``s3 sync`` command
* Fix an issue when uploading large files on low bandwidth networks
  (issue 454)
* Fix an issue with parsing shorthand boolean argument values (issue 477)
* Fix an issue with the ``cloudsearch`` command missing a required attribute
  (boto/botocore#175)
* Fix an issue with parsing XML response for
  ``ec2 describe-instance-attribute`` (boto/botocore#174)
* Update ``cloudformation`` command to support new features for stacks and
  templates
* Update ``storagegateway`` command to support a new gateway configuration,
  Gateway-Virtual Tape Library (Gateway-VTL)
* Update ``elb`` command to support cross-zone load balancing, which
  changes the way that Elastic Load Balancing (ELB) routes incoming requests


1.2.3
=====

* Add a new ``configure`` command that allows users to interactively specify
  configuration values (pull request 455)
* Add support for new EMR APIs, termination of specific cluster instances, and
  unlimited EMR steps
* Update Amazon CloudFront command to the 2013-09-27 API version
* Fix issue where Expires timestamp in bundle-instance policy is incorrect
  (issue 456)
* The requests library is now vendored in botocore (at version 2.0.1)
* Fix an issue where timestamps used for Signature Version 4 weren't being
  refreshed (boto/botocore#162)


1.2.2
=====

* Fix an issue causing ``s3 sync`` with the ``--delete`` incorrectly deleting files (issue 440)
* Fix an issue with ``--output text`` combined with paginated results (boto/botocore#165)
* Fix a bug in text output when an empty list is encountered (issue 446)


1.2.1
=====

* Update the AWS Direct Connect command to support the latest features
* Fix text output with single scalar value (issue 428)
* Fix shell quoting for ``PAGER``/``MANPAGER`` environment variable (issue 429)
* --endpoint-url is explicitly used for URL of remote service (boto/botocore#163)
* Fix an validation error when using ``--ip-permissions`` and ``--group-id`` together (issue 435)


1.2.0
=====

* Update Amazon Elastic Transcoder command with audio transcoding features
* Improve text output (``--output text``) to have a consistent output structure
* Add ``--query`` argument that allows you to specify output data using a JMESPath expression
* Upgrade requests library to 2.0.0
* Update Amazon Redshift region configuration to include ``ap-southeast-1``  and ``ap-southeast-2``
* Update Amazon S3 region configuration to include ``fips-us-gov-west-1``
* Add a bundled installer for the CLI which bundles all necessary dependencies (does not require pip)
* Fix an issue with ZSH tab completion (issue 411)
* Fix an issue with S3 requests timing out (issue 401)
* Fix an issue with ``s3api delete-objects`` not providing the ``Content-MD5`` header (issue 400)


1.1.2
=====

* Update the Amazon EC2 command to support Reserved Instance instance type modifications
* Update the AWS OpsWorks command to support new resource management features
* Fix an issue when transferring files on different drives on Windows
* Fix an issue that caused interactive help to emit control characters on certain Linux distributions


1.1.1
=====

* Update the Amazon CloudFront command to support the latest API version 2013-08-26
* Update the Auto Scaling client to support public IP address association of instances
* Update Amazon SWF to support signature version 4
* Update Amazon RDS with a new subcommand, ``add-source-identifier-to-subscription``


1.1.0
=====

* Update the ``s3`` commands to support the setting for how objects are stored in Amazon S3
* Update the Amazon EC2 command to support the latest API version (2013-08-15)
* Fix an issue causing excessive CPU utilization in some scenarios where many files were being uploaded
* Fix a memory growth issue with ``s3`` copying and syncing of files
* Fix an issue caused by a conflict with a dependency and Python 3.x that caused installation to fail
