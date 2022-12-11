from setuptools import setup

setup(
    name='Region from Number',
    version='1.0',
    packages=[''],
    url='https://github.com/kingco6ra/region_from_number',
    license='',
    author='kingco6ra',
    author_email='king.co6ra@yandex.ru',
    description='Получение региона в котором был зарегистрирован номер.',
    entry_points={
        'console_scripts':
            ['region = region:run']
    },
    install_requires=[
        'certifi==2022.12.7',
        'charset-normalizer==2.1.1',
        'colorama==0.4.6',
        'idna==3.4',
        'requests==2.28.1',
        'soupsieve==2.3.2.post1',
        'urllib3==1.26.13',
        'aiohttp~=3.8.3',
    ]
)
