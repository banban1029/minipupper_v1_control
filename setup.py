from setuptools import find_packages, setup

package_name = 'minipupper_v1_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages('src',exclude=['test']),
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='banban',
    maintainer_email='banshiro1029@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'calibrate.banban = minipupper_v1_control.calibrate:main' 
        ],
    },
)
