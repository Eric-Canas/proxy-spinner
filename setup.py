from setuptools import setup, find_packages

setup(
    name='proxy-spinnerr',
    version='0.1',
    author='Eric-Canas',
    author_email='eric@ericcanas.com',
    url='https://github.com/Eric-Canas/proxy-rotator',
    description='ProxySpinner is an straightforward, non-reliable, non-secure, but easy-to-use library for '
                'avoiding IP blocking by rotating free proxies on demand. It relies in services like '
                'proxyscrape.com to get the proxies and rotates them on demand, and is subject to the '
                'availability of that service and the proxies it lists.',

    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)