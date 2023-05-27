import setuptools

# Read configuration from setup.cfg
config = setuptools.config.read_configuration('setup.cfg')

# Call setuptools.setup with the configuration
setuptools.setup(install_requires=[
    'click==8.1.3',
    'Faker==18.7.0',
    'numpy==1.24.2',
    'pydicom==2.3.1',
    'pyrootutils==1.0.4',
    'PyYAML==6.0',
    'tqdm==4.65.0']
    , **config)
