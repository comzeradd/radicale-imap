from setuptools import find_packages, setup


def readme_md():
    """Return contents of README.md"""
    return open("README.md").read()


def changelog_md():
    """Return contents of Changelog.md"""
    return open("Changelog.md").read()


setup(
    name='radicale-imap',
    version='0.2.0',
    author='Nikos Roussos',
    author_email='nikos@roussos.cc',
    url='https://gitlab.com/comzeradd/radicale-imap/',
    description='Radicale IMAP authentication plugin',
    long_description_content_type="text/markdown",
    long_description=readme_md() + "\n\n" + changelog_md(),
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['radicale'],
    license='LICENSE',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
