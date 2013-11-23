from setuptools import setup

if __name__ == "__main__":
    setup(
        name='pspec',
        description='rspec inspired python test runner',
        long_description=open("README.md").read(),
        version='0.1.0',
        author='Catalin Costache',
        author_email='catacgc@gmail.com',
        url='http://github.com/catacgc/pspec/',
        py_modules=['pspec', 'pytest_pspec'],
        entry_points={'pytest11': ['pep8 = pytest_pspec']},
        install_requires=['pytest>=2.4.2'],
        )