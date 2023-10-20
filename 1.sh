
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


# 20231020 测试效果

生成的文件，可以在我的机器上运行，coredump 问题已经解决。
但是运行 python 模块需要设置 MOJO_PYTHON_LIBRARY 变量 export MOJO_PYTHON_LIBRARY=/usr/lib64/libpython3.so
并且 mojo 代码中引用的 py 文件还是要存在的，并没有被编译进可执行文件中

继续等待 mojo 生成静态链接文件。
