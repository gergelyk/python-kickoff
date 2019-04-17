python3 -m venv --clear venv --system-site-packages # use system-site-packages to mport python-qt5 from the system
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
pip install git+https://github.com/szsdk/quick # not available in PyPI
python3 -m pip install -e .

echo "setting KICKOFF_DEBUG=1"
echo "export KICKOFF_DEBUG=1" >> venv/bin/activate

ln -sf examples/kickoffcustomize.py .

echo "Setup done. Invoke:"
echo "source venv/bin/activate"
