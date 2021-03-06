import os

import click

ROOT_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)
PLUGIN_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'detectem/plugins')
PLUGIN_DIRECTORIES = [
    d for d in os.listdir(PLUGIN_DIRECTORY) if not d.startswith('_')
]


@click.command()
@click.option(
    '--matcher',
    type=click.Choice(['url', 'body', 'header']),
    required=True,
    help='Set the matcher type.',
)
@click.option(
    '--category',
    type=click.Choice(PLUGIN_DIRECTORIES),
    required=True,
    help='Set plugin category.',
)
@click.argument('name')
def main(name, category, matcher):
    create_plugin_file(name, category, matcher)
    create_test_file(name, matcher)


def create_plugin_file(name, category, matcher):
    plugin_template = '''
from detectem.plugin import Plugin


class {title}Plugin(Plugin):
    name = '{name}'
    homepage = ''
    matchers = [
        {{'{matcher}': 'Plugin signature v(?P<version>[0-9\.]+)'}},
    ]
    """
    js_matchers = [
        {{'check': '', 'version': ''}},
    ]
    """
'''.format(name=name, title=name.title(), matcher=matcher).lstrip()

    plugin_filename = name + '.py'
    plugin_filepath = os.path.join(
        PLUGIN_DIRECTORY, category, plugin_filename
    )

    if os.path.exists(plugin_filepath):
        raise FileExistsError('Plugin file already exists.')

    with open(plugin_filepath, mode='w') as f:
        f.write(plugin_template)
        print('Created plugin file at {}'.format(plugin_filepath))


def create_test_file(name, matcher):
    test_template = '''
- plugin: {name}
  matches:
    - {matcher}:
      version:
'''.format(name=name, matcher=matcher).lstrip()

    test_filename = name + '.yml'
    test_filepath = os.path.join(
        ROOT_DIRECTORY, 'tests', 'plugins', 'fixtures', test_filename
    )

    if os.path.exists(test_filepath):
        raise FileExistsError('Test file already exists.')

    with open(test_filepath, mode='w') as f:
        f.write(test_template)
        print('Created test file at {}'.format(test_filepath))


if __name__ == "__main__":
    main()
