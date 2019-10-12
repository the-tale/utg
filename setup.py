# coding: utf-8
import setuptools

setuptools.setup(
    name='UTG',
    version='0.3.2',
    description='Генератор связанного русского текста',
    long_description=open('README.rst').read(),
    url='https://github.com/Tiendil/utg',
    author='Aleksey Yeletsky <Tiendil>',
    author_email='a.eletsky@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Natural Language :: Russian'],
    keywords=['text generation', 'генерация текста'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Rels>=0.3.0',
    ],
    test_suite='tests')
