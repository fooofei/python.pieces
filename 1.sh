
docker pull swr.cn-north-4.myhuaweicloud.com/fooofei/mojo:1020

docker run -it -v$(pwd):/host --network=host --name=temp --rm swr.cn-north-4.myhuaweicloud.com/fooofei/mojo:1020 bash 
apt install python3.10-venv -y
apt-get update
apt-get install modular -y
apt-get install libedit-dev -y
# 每次运行 install 前都必须执行这个
modular clean
modular install mojo

echo 'export MOJO_PYTHON_LIBRARY="/usr/lib/x86_64-linux-gnu/libpython3.10.so"' >> ~/.bashrc


echo 'export MODULAR_HOME="/root/.modular"' >> ~/.bashrc
echo 'export PATH="/root/.modular/pkg/packages.modular.com_mojo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

If you are using ZSH, run the following commands:
echo 'export MODULAR_HOME="/root/.modular"' >> ~/.zshrc
echo 'export PATH="/root/.modular/pkg/packages.modular.com_mojo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
