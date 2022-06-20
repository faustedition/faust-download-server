#!/bin/sh

echo "This will use micromamba to bootstrap a Python environment to run the server."

MAMBA_ROOT_PREFIX=$PWD/venv
export MAMBA_ROOT_PREFIX

echo "The environment will be in $MAMBA_ROOT_PREFIX".

echo "Downloading micromamba ..."
mkdir "$MAMBA_ROOT_PREFIX" && wget -qO- https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -C "$MAMBA_ROOT_PREFIX" -xj bin/micromamba
micromamba="$MAMBA_ROOT_PREFIX/bin/micromamba"

echo "Using micromamba to install python ..."
$micromamba install -n base --no-rc --yes python=3.10 -c conda-forge

echo "Using pip to install the server ..."
$micromamba --no-rc -n base run pip install '.[production]'

cat > run-server.sh <<EOF 
#!/bin/sh
cd "$PWD"
test -r .env && . .env
exec $MAMBA_ROOT_PREFIX/bin/gunicorn
EOF
chmod 755 ./run-server.sh

echo "You may now want to create an .env file to configure stuff"
echo "and run $PWD/run-server.sh to start the server."
