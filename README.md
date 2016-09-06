## pbcommand High Level Overview


co-owners:

[mpkocher](https://github.com/mpkocher)

[natechols](https://github.com/natechols)

PacBio Officially Supported Library. Note the APIs are still in flux and not yet 1.0.0.

[Full Docs](http://pbcommand.readthedocs.org/en/latest/)

[![Circle CI](https://circleci.com/gh/PacificBiosciences/pbcommand.svg?style=svg)](https://circleci.com/gh/PacificBiosciences/pbcommand)



### Components

PacBio library for common utils, models, and tools to interface with pbsmrtpipe workflow engine.

1. Common Models and Schemas
2. Service client layer to the SMRTLink services
3. Tool Contract and Resolved Tool Contract interface for integrating with pbsmrtpipe and SMRT Link


## PacBio Core Models and Schemas

- [ToolContract](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/pbreport.avsc) : Used in define task interfaces and used in pipeline definitions (i.e., Resolved Pipeline Templates)
- [ResolvedToolContract](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/resolved_tool_contract.avsc): Used in pipeline running
- [PacBio Report](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/pbreport.avsc) Core data model for plots, tables and metrics (i.e., attributes) displayed in SMRTLink or available as output from SMRT Link web services) [Examples](https://github.com/PacificBiosciences/pbcommand/tree/master/tests/data/example-reports)
- [PacBio DataStore](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/datastore.avsc): JSON file of datastore file(s) that are emitted from an analysis, import-dataset or other job type. 
- [DataStore View Rules](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/datastore_view_rules.avsc) Custom views of datastore files in SMRTLink)
- [TODO] Pipeline Template View Rules: Custom hiding and renaming of pipeline task options for SMRTLink UI) [Examples](https://github.com/PacificBiosciences/smrtflow/tree/master/smrt-server-analysis/src/main/resources/pipeline-template-view-rules)
- [TODO] Resolved Pipeline Template: Custom description of pipeline, bindings and task options for SMRTLink UI [Examples](https://github.com/PacificBiosciences/smrtflow/blob/master/smrt-server-analysis/src/main/resources/resolved-pipeline-templates/pbsmrtpipe.pipelines.dev_diagnostic_pipeline_template.json)
- [TODO] Report View Rules [Examples](https://github.com/PacificBiosciences/smrtflow/tree/master/smrt-server-analysis/src/main/resources/report-view-rules) 

An HTML view of these models can be generated by using [AvroDoc](https://github.com/ept/avrodoc)

The Avro schema format can be converted to JSON Schema using [Avro To Json Schema](https://json-schema-validator.herokuapp.com)


## Service Client Layer to SMRT Link

pbcommand provides a high level interface to the SMRT Link services. See `pbcommand.services` for more details.
 
Here's a terse example of getting a Job by id and fetching the report metrics from the results.
 
```
IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: from pbcommand.services import ServiceAccessLayer

In [2]: s = ServiceAccessLayer("smrtlink-beta", 8081)

In [3]: j = s.get_analysis_job_by_id(22270)

In [4]: j.id, j.name, j.path
Out[4]: 
(22270,
 'm54088_160819_000654_resequencing',
 '/pbi/dept/secondary/siv/smrtlink/smrtlink-beta/smrtsuite_166987/userdata/jobs_root/022/022270')

In [5]: j
Out[5]: ServiceJob(id=22270, uuid=u'4443d0b6-899c-40b9-98f2-2e2b4f889b53', name='m54088_160819_000654_resequencing', state='SUCCESSFUL', path='/pbi/dept/secondary/siv/smrtlink/smrtlink-beta/smrtsuite_166987/userdata/jobs_root/022/022270', job_type='pbsmrtpipe', created_at=datetime.datetime(2016, 8, 20, 1, 25, 50, 874000, tzinfo=<iso8601.Utc>), settings={u'workflowOptions': [], u'entryPoints': [{u'fileTypeId': u'PacBio.DataSet.ReferenceSet', u'entryId': u'eid_ref_dataset', u'datasetId': 9898}, {u'fileTypeId': u'PacBio.DataSet.SubreadSet', u'entryId': u'eid_subread', u'datasetId': 35547}], u'pipelineId': u'pbsmrtpipe.pipelines.sa3_ds_resequencing_fat', u'taskOptions': [], u'name': u'm54088_160819_000654_resequencing'})

In [6]: report_metrics = s.get_analysis_job_report_attrs(22270)

In [7]: report_metrics
Out[7]: 
{u'coverage.depth_coverage_mean': 11251.832147121406,
 u'coverage.missing_bases_pct': 0.004559547692868867,
 u'mapping_stats.mapped_readlength_max': 15478,
 u'mapping_stats.mapped_readlength_mean': 3899,
 u'mapping_stats.mapped_readlength_n50': 5844,
 u'mapping_stats.mapped_readlength_q95': 9560,
 u'mapping_stats.mapped_reads_n': 207986,
 u'mapping_stats.mapped_subread_bases_n': 810462596,
 u'mapping_stats.mapped_subread_concordance_mean': 0.8354,
 u'mapping_stats.mapped_subread_readlength_max': 12846.0,
 u'mapping_stats.mapped_subread_readlength_mean': 3823,
 u'mapping_stats.mapped_subreadlength_n50': 5799,
 u'mapping_stats.mapped_subreadlength_q95': 9530,
 u'mapping_stats.mapped_subreads_n': 212005,
 u'variants.longest_contig_name': u'11k_pbell_H1-6_ScaI_circular_3x_l65796',
 u'variants.mean_contig_length': 65796.0,
 u'variants.weighted_mean_bases_called': 0.9999544045230713,
 u'variants.weighted_mean_concordance': 0.9999696016293528,
 u'variants.weighted_mean_coverage': 11251.832147121406}

In [8]: 
 
``` 



## Tool Contract and Resolved Tool Contracts

To integrate with the pbsmrtpipe workflow engine you must to be able to generate a **Tool Contract** and to be able to run from a **Resolved Tool Contract**.

A **Tool Contract** contains the metadata of the exe, such as the file types of inputs, outputs and options.

Example [Tool Contract Json](https://github.com/PacificBiosciences/pbcommand/blob/master/tests/data/dev_example_dev_txt_app_tool_contract.json) (and [Avro Schema](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/tool_contract.avsc))

Example [Resolved Tool Contract Json](https://github.com/PacificBiosciences/pbcommand/blob/master/tests/data/resolved_tool_contract_dev_app.json) (and [Avro Schema](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/schemas/resolved_tool_contract.avsc))

There are two principle use cases, first wrapping/calling python functions that have been defined in external python packages, or scripts. Second, creating a CLI tool that supports emitting tool contracts, running resolved tool contracts and complete argparse style CLI.

Example from **pbcommand.cli.examples**

```python

import sys
import logging

from pbcommand.models import FileTypes
from pbcommand.cli import registry_builder, registry_runner

log = logging.getLogger(__name__)

registry = registry_builder("pbcommand", "python -m pbcommand.cli.examples.dev_quick_hello_world ")


def _example_main(input_files, output_files, **kwargs):
    # Simple Function that should imported from your library code
    # write mock output files for testing purposes, otherwise the End-to-End test will fail
    xs = output_files if isinstance(output_files, (list, tuple)) else [output_files]
    for x in xs:
        with open(x, 'w') as writer:
            writer.write("Mock data\n")
    return 0


@registry("dev_qhello_world", "0.2.1", FileTypes.FASTA, FileTypes.FASTA, nproc=1, options=dict(alpha=1234))
def run_rtc(rtc):
    return _example_main(rtc.task.input_files[0], rtc.task.output_files[0], nproc=rtc.task.nproc)


@registry("dev_fastq2fasta", "0.1.0", FileTypes.FASTQ, FileTypes.FASTA)
def run_rtc(rtc):
    return _example_main(rtc.task.input_files[0], rtc.task.output_files[0])


if __name__ == '__main__':
    sys.exit(registry_runner(registry, sys.argv[1:]))

```

A driver is the commandline interface that the workflow engine will call.

The driver will be called with "${exe} /path/to/resolved_tool_contract.json"

The tool contracts can be emitted to a directory and used in [pbsmrtpipe](https://github.com/PacificBiosciences/pbsmrtpipe).

```bash
$> python -m pbcommand.cli.examples.dev_quick_hello_world -o /path/to/my-tool-contracts
```


## Creating a Full Commandline Tool with TC/RTC and argparse support


Three Steps
- define Parser using `get_pbparser`
- add running from argparse and running from Resolved ToolContract funcs to call your main
- add call to driver

Import or define your main function from your library.

```python

def run_my_main(fasta_in, fasta_out, min_length):
    # do work. Main should return an int exit code and be completely independent of argparse
    return 0
```

Define a function that will add inputs, outputs and options to your parser.

```python
from pbcommand.models import FileTypes


def add_args_and_options(p):
    # FileType, label, name, description
    p.add_input_file_type(FileTypes.FASTA, "fasta_in", "Fasta File", "PacBio Spec'ed fasta file")
    # File Type, label, name, description, default file name
    p.add_output_file_type(FileTypes.FASTA, "fasta_out", "Filtered Fasta file", "Filtered Fasta file", "filter.fasta")
    # Option id, label, default value, name, description
    # for the argparse, the read-length will be translated to --read-length and (accessible via args.read_length)
    p.add_int("pbcommand.task_options.dev_read_length", "read-length", 25, "Length filter", "Min Sequence Length filter")
    return p
```

Define Parser

```python
from pbcommand.models import TaskTypes, SymbolTypes, get_pbparser


def get_contract_parser():
    tool_id = "example_namespace.tasks.my_id"
    version = "0.1.0"  # or reuse __version__
    display_name = "My Example Tool"
    # Number of processors to use, can also be SymbolTypes.MAX_NPROC
    nproc = 1
    # Log file, tmp dir, tmp file. See ResourceTypes in models, ResourceTypes.TMP_DIR
    resource_types = ()
    # Commandline exe to call "{exe}" /path/to/resolved-tool-contract.json
    driver_exe = "python -m pbcommand.cli.example.dev_app --resolved-tool-contract "
    desc = "Dev app for Testing that supports emitting tool contracts"
    is_distributed = False 
    # set to True if you want your task to be submitted to the cluster manager (e.g., SGE) if 
    # one is provided to the workflow engine.
    p = get_pbparser(tool_id, version, display_name, desc, driver_exe, is_distributed=is_distributed, nproc=nproc, resource_types=resource_types)
    add_args_and_options(p)
    return p
```
        

Define a Wrapping IO layer to call your main function from both the tool contract and raw argparse IO layer

```python
def _args_runner(args):
    # this is the args from parser.parse_args() using the python stdlib argparse model
    # the properties of args are defined as "labels" in the add_args_and_options func.
    return run_my_main(args.fasta_in, args.fasta_out, args.read_length)

    
def _resolved_tool_contract_runner(resolved_tool_contract):
    """
    :type resolved_tool_contract: pbcommand.models.ResolvedToolContract"""
    rtc = resolved_tool_contract
    # all options are referenced by globally namespaced id. This allows tools to use other tools options
    # e.g., pbalign to use blasr defined options.
    return run_my_main(rtc.task.input_files[0], rtc.task.outputs[0], rtc.task.options["pbcommand.task_options.dev_read_length"])
```
    
    
Add running layer

```python
import sys
import logging
from pbcommand.utils import setup_log
from pbcommand.cli import pbparser_runner

log = logging.getLogger(__name__)


def main(argv=sys.argv):
    # New interface that supports running resolved tool contracts
    log.info("Starting {f} version {v} pbcommand example dev app".format(f=__file__, v="0.1.0"))
    return pbparser_runner(argv[1:], 
                           get_contract_parser(), 
                           _args_runner, # argparse runner func
                           _resolved_tool_contract_runner, # tool contract runner func
                           log, # log instance
                           setup_log # setup log func
                           )
if __name__ == '__main__':
    sys.exit(main())
```

Now you can run your tool via the argparse standard interface as well as emitting a **Tool Contract** to stdout from the commandline interface.

```sh
> python -m 'pbcommand.cli.examples.dev_app' --emit-tool-contract
```

And you can run the tool from a **Resolved Tool Contract**

```sh
> python -m pbcommand.cli.examples.dev_app --resolved-tool-contract /path/to/resolved_contract.json
```

See the dev apps in ["pbcommand.cli.examples"](https://github.com/PacificBiosciences/pbcommand/blob/master/pbcommand/cli/examples/dev_app.py) for a complete application (They require pbcore to be installed).

In addition to TC/RTC support, there's a complete argparse support for the task options. An example of **help** is shown below.

```sh
$> python -m pbcommand.cli.examples.dev_app --help
usage: dev_app.py [-h] [-v] [--versions] [--emit-tool-contract]
                  [--resolved-tool-contract RESOLVED_TOOL_CONTRACT]
                  [--log-level LOG_LEVEL] [--debug]
                  [--read-length READ_LENGTH]
                  fasta_in fasta_out

Dev app for Testing that supports emitting tool contracts

positional arguments:
  fasta_in              PacBio Spec'ed fasta file
  fasta_out             Filtered Fasta file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --versions            Show versions of individual components (default: None)
  --emit-tool-contract  Emit Tool Contract to stdout (default: False)
  --resolved-tool-contract RESOLVED_TOOL_CONTRACT
                        Run Tool directly from a PacBio Resolved tool contract
                        (default: None)
  --log-level LOG_LEVEL
                        Set log level (default: 10)
  --debug               Debug to stdout (default: False)
  --read-length READ_LENGTH
                        Min Sequence Length filter (default: 25)
```

