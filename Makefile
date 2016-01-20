export PYTHONWARNINGS?=ignore

reloadgunicorn:
	cat var/app.pid | xargs kill -HUP

stopgunicorn:
	cat var/app.pid | xargs kill -SIGTERM

clean_pyc:
	@find `pwd` \( -name '*.pyc' -o -name '*.ptlc' \) -type f -delete

