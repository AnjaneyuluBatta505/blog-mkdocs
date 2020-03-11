from setuptools import setup

setup(
    name='mkdoc-blog',
    version='1.0.0',
    packages=['blog'],
    url='https://github.com/AnjaneyuluBatta505/blog-mkdocs',
    license='MIT',
    author='Anjaneyulu Batta',
    author_email='anjaneyulu.batta505@gmail.com',
    description='Blog plugin for mkdocs',
    install_requires=['mkdocs'],

    entry_points={
        'mkdocs.plugins': [
            'mkdoc_blog = blog:Blog',
        ]
    },
)
