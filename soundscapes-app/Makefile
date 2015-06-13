restart:
	rm -f soundscapes.sqlite3
	rm -rf ../media/
	~/.venvs/soundscapes/bin/python manage.py migrate
	~/.venvs/soundscapes/bin/python manage.py loaddata shows.yaml
	~/.venvs/soundscapes/bin/python manage.py update
