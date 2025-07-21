#!/usr/bin/env python3
"""
Setup script para o jogo Combate por Turnos com IA
"""

from setuptools import setup, find_packages
import os

# Lê o README para a descrição longa
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Lê os requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="combate-turnos-ia",
    version="2.0.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Jogo de combate por turnos com IA Minimax e Rede Neural",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/combate-turnos-ia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.910",
        ],
        "gui": [
            "Pillow>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "combate-turnos=game.window_manager:run_window_manager",
            "combate-console=main:main",
            "combate-demo=demo_neural_ai:menu_principal",
        ],
    },
    include_package_data=True,
    package_data={
        "game": ["assets/*.png"],
    },
    keywords=[
        "game", "ai", "minimax", "neural-network", "turn-based", 
        "strategy", "python", "tkinter", "machine-learning"
    ],
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/combate-turnos-ia/issues",
        "Source": "https://github.com/seu-usuario/combate-turnos-ia",
        "Documentation": "https://github.com/seu-usuario/combate-turnos-ia#readme",
    },
)