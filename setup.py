"""Setup script untuk BugBountyAI"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='bugbountyai',
    version='2.0.0',
    author='BugBountyAI Team',
    author_email='team@bugbountyai.com',
    description='AI-Powered Bug Bounty Security Vulnerability Scanner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/joaovitorpipps-max/BugBountyAI',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'bugbountyai=bugbountyai.cli.main:cli',
        ],
    },
    keywords='security bug-bounty vulnerability scanner ai machine-learning',
    project_urls={
        'Bug Reports': 'https://github.com/joaovitorpipps-max/BugBountyAI/issues',
        'Documentation': 'https://github.com/joaovitorpipps-max/BugBountyAI/docs',
        'Source Code': 'https://github.com/joaovitorpipps-max/BugBountyAI',
    },
)
