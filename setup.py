from setuptools import setup
import specs

if __name__ == "__main__":
    setup(
        name='specs',
        description='easy, readable python test specifications inspired by rspec',
        long_description=open("README.md").read(),
        version=specs.__version__,
        license='MIT',
        author='Catalin Costache',
        author_email='catacgc@gmail.com',
        url='http://github.com/catacgc/specs/',
        py_modules=['specs', 'pytest_specs'],
        entry_points={'pytest11': ['pep8 = pytest_specs']},
        install_requires=['pytest>=2.4.2'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Environment :: Console',
            'Programming Language :: Python',
            'Topic :: Software Development :: Documentation',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing',
            'Topic :: Utilities',
            ]
        )