import setuptools


setuptools.setup(
    name='carga',
    version='0.0.1',
    install_requires=['django', 'waitress', 'psycopg2'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=['scripts/carga',
             'scripts/carga-manage']
)
