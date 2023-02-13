if [[ "$OSTYPE" =~ ^msys ]]; then
	PYVERSION="py"
else
	PYVERSION="python3"
fi

$PYVERSION -m pip install --upgrade pip
$PYVERSION -m pip uninstall selenium keyboard pyairtable beautifulsoup4
$PYVERSION -m pip install selenium keyboard pyairtable beautifulsoup4

echo "Libraries have been installed"
