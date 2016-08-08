openCommittee
=============
Live on - http://www.vaadat-sarim.org.il/

* install python 2.7.11
* run 'pip install virtualenv'
    * Mac + Linux:
        * run 'pip install virtualenvwrapper'
        * run 'export WORKON_HOME=/Users/<<YOUR_USERNAME>>/Envs'
        * run 'source /usr/local/bin/virtualenvwrapper.sh,
    * Windows:
        * run 'pip install virtualenvwrapper-win'

* run 'mkvirtualenv openCommittee'
* run 'workon openCommittee'
* run 'pip install -r requirements.txt'
    * (if you encounter problems check this out - http://stackoverflow.com/questions/38243633/falied-to-install-flask-under-virutalenv-on-windows-error-2-the-system-cann)
* install postgres
* install pgadmin
* create a new db called ‘openCommittee’
* create a role called ‘openCommittee’ with the same password
* make this role the owner of the new db
* run 'python manage.py syncdb --migrate'
* download *.json files to directory
* run 'python manage.py loaddata ministers.json'
* run 'python manage.py loaddata voteType.json'
* run 'python manage.py import_bills_gss'
* run 'python manage.py import_votes_gss'
* run ‘python manage.py run server’

browse to the website!
