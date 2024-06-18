# Parameters. You can set it by running make clone user=YourUser token=Av3rYS3cr3T0k3n or you can specify some default values in the lines below
user?=foo_user
token?=foo_token


HELP_FUNCTION =  \
    %help; \
    while(<>) { \
        if(/^([a-z0-9_-]+):.*\#\#(?:@(\w+))?\s(.*)$$/) { \
            push(@{$$help{$$2}}, [$$1, $$3]); \
        } \
    }; \
    print "usage: make [target] [user=YourUser] [token=Av3rYS3cr3T0k3n]\n\n"; \
    for ( sort keys %help ) { \
        print "$$_:\n"; \
        printf("  %-20s %s\n", $$_->[0], $$_->[1]) for @{$$help{$$_}}; \
        print "\n"; \
    }

help: ## Show this help
	@perl -e '$(HELP_FUNCTION)' $(MAKEFILE_LIST)

clone: ## Downloads 'production' repo, it contains the docker-compose template
	git clone https://$(user):$(token)@github.com/simanfor-dask/production.git

update: ## Downloads 'production' repo changes (if any)
	(cd production && git pull https://$(user):$(token)@github.com/simanfor-dask/production.git)

up: ## Logins into github packages and then tries to up docker-compos4e
	docker login ghcr.io -u $(user) -p $(token)
	(cd production && docker-compose up -d)

stop: ## Stops docker-compose (if running)
	(cd production && docker-compose stop)

clean: ## Logout github packages, clean all docker system (stoped containers, unused images and networks) and deletes 'production' repo
	docker logout
	docker system prune -a -f
	rm -rf production/
