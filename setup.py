# coding: utf-8
import setuptools

setuptools.setup(
    name='UTG',
    version='0.2.0',
    description=u'Генератор связанного русского текста',
    long_description = open('README.rst').read(),
    url='https://github.com/Tiendil/utg',
    author='Aleksey Yeletsky <Tiendil>',
    author_email='a.eletsky@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

        'Natural Language :: Russian'],
    keywords=['text generation', 'генерация текста'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    test_suite = 'tests',
    )
