from setuptools import find_packages, setup


setup(
    name='smoke_test',
    version='1.1.0',
    url='https://github.com/petarmaric/smoke_test',
    license='BSD',
    author='Petar Maric',
    author_email='petarmaric@uns.ac.rs',
    description='Console app and Python API for automated smoke testing',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'smoke_test=smoke_test.shell:main',
        ],
        'distutils.commands': [
            'bdist_pex = pex.commands.bdist_pex:bdist_pex',
        ],
    },
    install_requires=[
        'friendly_name_mixin~=1.0',
        'pycparser==2.19',
        'pycparser_fake_libc==2.19',
        'PyYAML~=3.11',
        'simple_plugins~=1.0',
    ],
    extras_require={
        'dev': [
            'pex~=1.6.0',
        ],
    },
)
