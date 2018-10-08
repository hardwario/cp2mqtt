from setuptools import setup

setup(
    name='cp2mqtt',
    packages=['cp2mqtt'],
    version='@@VERSION@@',
    description='COOPER to MQTT',
    url='https://github.com/hardwario/cp2mqtt',
    author='HARDWARIO s.r.o.',
    author_email='ask@hardwario.com',
    license='MIT',
    keywords = ['cooper', 'mqtt', 'zmq', 'iot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Environment :: Console',
        'Intended Audience :: Science/Research'
    ],
    install_requires=[
        'click>=6.7', 'PyYAML>=3.13','pyzmq>=17.1','schema>=0.6', 'paho-mqtt>=1.4', 'simplejson>=3.16'
    ],
    entry_points='''
        [console_scripts]
        cp2mqtt=cp2mqtt.app:main
    '''
)
