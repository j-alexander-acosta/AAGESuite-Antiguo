include .env
export

#BACKUP_DATE ?= $(shell dialog --stdout --date-format %Y%m%d --calendar "Elija la fecha del respaldo a restaurar" 4 40)
BACKUP_DATE ?= `dialog --stdout --date-format %Y%m%d --calendar "Elija la fecha del respaldo a restaurar" 4 40`
BACKUP_DATE := ${BACKUP_DATE}
DUMP_FILENAME ?= "carga-${BACKUP_DATE}.dump"
DUMP_FILENAME := ${DUMP_FILENAME}

serve: .make.nix-exists
	nix-shell --run 'python3 manage.py runserver 0.0.0.0:8080'
.PHONY: serve

shell: .make.nix-exists
	nix-shell
.PHONY: shell

test: .make.nix-exists
	nix-shell --run 'python3 manage.py test --parallel --settings=carga.settings.testing'
.PHONY: test

migrate: .make.nix-exists
	nix-shell --run 'python3 manage.py migrate'
.PHONY: migrate

manage.py: .make.nix-exists
	nix-shell --run 'django-admin startproject $(PROJECT_NAME) .'

dropdb: .make.nix-exists
	rm .make.postgres-started; \
	rm .make.postgres-init; \
	rm -rf $(PGHOST)
.PHONY: dropdb


restore: .make.nix-exists
	scp -P 22222 ch.unach.cl:/home/carga/backups/${DUMP_FILENAME} /tmp; \
	nix-shell --run 'dropdb $(DBNAME); createdb -O $(DBUSER) $(DBNAME)'; \
	nix-shell --run "pg_restore -Fc -d carga /tmp/${DUMP_FILENAME} --no-privileges --no-owner"; \
	rm /tmp/${DUMP_FILENAME}
.PHONY: restore

.make.postgres-init:
	if [ ! -d $(PGDATA) ]; then mkdir -p $(PGDATA) && initdb --auth-local=trust; fi
	touch $@

db_init: .make.postgres-init
.PHONY: db_init

.make.postgres-started: .make.postgres-init
	echo -n "PostgreSQL "; \
	setsid pg_ctl -l $(PGLOG) -o '-k $(PGHOST) -h ""' -w start; \
	if [ ! "`psql -d template1 -c '\du' | grep $(DBUSER) | awk '{print $$1}'`" = "$(DBUSER)" ]; \
		then \
			createuser -s $(DBUSER); \
			createdb -O $(DBUSER) $(DBNAME); \
	fi
	touch $@

.SILENT: .make.postgres-started

db_start: .make.postgres-started
.PHONY: db_start

db_stop:
	if [ `find .make.nix-shell* | wc -l` -eq 1 ]; then pg_ctl stop && rm .make.postgres-started; fi
.PHONY: db_stop

.make.nix-exists:
	if command -v nix 2>/dev/null; \
		then \
			echo 'Selecting $(TRACKED_NIX_CHANNEL) channel as $(PROJECT_NAME)-nixpkgs.'; \
			if [ `nix-channel --list | grep $(PROJECT_NAME)-nixpkgs | wc -l` -ne 1 ]; then nix-channel --add https://nixos.org/channels/$(TRACKED_NIX_CHANNEL) $(PROJECT_NAME)-nixpkgs && nix-channel --update $(PROJECT_NAME)-nixpkgs; fi; \
			touch --date=@0 $@; \
		else \
			if [ ! -d ~/.nix-profile ]; then curl -L https://nixos.org/nix/install | sh; fi; \
			echo "$$(tput setaf 3)It seems Nix is already installed. Make sure all necessary\nenvironment variables are set, either log in again, or type\n\n$$(tput setaf 2)  . ~/.nix-profile/etc/profile.d/nix.sh\n$$(tput setaf 9)"; \
			exit 1; \
	fi
.SILENT: .make.nix-exists


ctags:
	ctags -e -R --languages=python3 --exclude=.git --exclude=log .
.PHONY: ctags

clear_session:
	rm -rf .make.postgres-started
	rm -rf .make.nix-shell*
.PHONY: clear_session

clean:
	rm -rf .make*
	rm -rf $(CONFIG_DIR)
.PHONY: clean
