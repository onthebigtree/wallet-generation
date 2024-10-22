#!/bin/bash

# 更新包列表
echo "Updating package lists..."
sudo apt-get update

# 安装 Python3 和 pip（如果尚未安装）
echo "Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

# 升级 pip
echo "Upgrading pip..."
pip3 install --upgrade pip

# 安装必要的 Python 包
echo "Installing required Python packages..."
pip install eth_account web3 secrets pysui

