from setuptools import setup

if __name__ == "__main__":
    setup(
        name='specs',
        description='easy test specifications inspired by rspec',
        long_description=open("README.md").read(),
        version='0.1.0',
        author='Catalin Costache',
        author_email='catacgc@gmail.com',
        url='http://github.com/catacgc/specs/',
        py_modules=['specs', 'pytest_specs'],
        entry_points={'pytest11': ['pep8 = pytest_specs']},
        install_requires=['pytest>=2.4.2'],
        )