# Find the root of the project to add it to the python path for resolving imports
import pyrootutils
import yaml

path = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml", "requirements.txt"],
    pythonpath=True,
    dotenv=True,
)
import click
from siimhack_dataset_toolbox.dicom_tag_modifier import DICOMTagModifier
from siimhack_dataset_toolbox.config_default import siim_default_configuration

context_settings = dict(help_option_names=["-h", "--help"])


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group(context_settings=context_settings)
def cli():
    """
    SIIM Hackathon dataset CLI to add new data in the dataset.
    \b
    Action Commands:
        modify_dicom_tags     Modify existing dicom data to fit the SIIM hackathon data format.
    \b
    """
    pass


# 1. Dicom modifier CLI

MODIFY_DICOM_TAGS_OPTIONS = [
    click.option('--input-directory',
                 '-i',
                 required=True,
                 type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True),
                 help='Input directory.'),
    click.option('--tag_modifier_request',
                 '-req',
                 required=True,
                 type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
                 help='Dicom tag request (yaml).'),
    click.option('--output-directory',
                 '-o',
                 required=True,
                 type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, writable=True,
                                 resolve_path=True),
                 help='Output directory.'),
    click.option('--validated-dicom',
                 is_flag=True,
                 help='Validate that the dicom file is a valid dicom'),
]


@cli.command(name='modify_dicom_tags')
@add_options(MODIFY_DICOM_TAGS_OPTIONS)
def modify_dicom_tags_cli(**kwargs):
    input_directory = kwargs['input_directory']
    output_directory = kwargs['output_directory']
    tag_modifier_request = kwargs['tag_modifier_request']
    validated_dicom = kwargs.get('validated_dicom', False)

    request = siim_default_configuration
    if tag_modifier_request:
        with open(tag_modifier_request, 'r') as f:
            request = yaml.safe_load(f)
    dm = DICOMTagModifier(input_directoy=input_directory, output_directory=output_directory, )
    dm.modify_dicom_tags(request)


if __name__ == '__main__':
    cli()
