import os.path
import setuptools

root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='pydouz',
    version='0.1.2',
    url='https://github.com/mohanson/pydouz',
    license='WTFPL',
    author='mohanson',
    author_email='mohanson@outlook.com',
    description='Douz is an experimental language for embedded and math.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'llvmlite',
    ],
    packages=['pydouz'],
    entry_points={
        'console_scripts': [
            'pydouz=pydouz.cmdline:parse',
        ],
    }
)
