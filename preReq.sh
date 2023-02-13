if [[ "$OSTYPE" =~ ^msys ]]; then
	PYEXE="py"
else
	PYEXE="python3"
fi

$PYEXE -m pip install --upgrade pip
$PYEXE -m pip uninstall selenium keyboard pyairtable beautifulsoup4
$PYEXE -m pip install selenium keyboard pyairtable beautifulsoup4

echo "Libraries have been installed"
