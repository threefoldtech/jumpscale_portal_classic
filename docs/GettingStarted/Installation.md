## Installing Jumpscale Portal

### Requirements

**Jumpscale Portal** has two major dependencies:

 - **Jumpscale Core**, also referenced to as the Jumpscale framework, needs to be installed
  - See the [installation secion in the Jumpscale Core documentation](https://gig.gitbooks.io/jumpscale-core8/content/GettingStarted/Installation.html) for detailed instructions
 - A connection to a running MongoDB instance
  - In order to install a MongoDB instance locally:

```py
    j.tools.prefab.local.db.mongo.install()
```

  - In order to install a MongoDB instance on a remote node:

```py
    executor = j.tools.executor.getSSHBased(addr="<IP address of remote machine>", port="SSH port of remote machine", login="username", passwd= "password")
    prefab = j.tools.prefab.get(executor)
    prefab.db.mongo.install()
```


### Local installion of a Jumpscale Portal

Using Cuisine:

```py
j.tools.prefab.local.web.portal.install()
```

Your portal content and code can now be placed in the `$JSBASEDIR/apps/portal/main` directory.


### Remote installation of a Jumpscale Portal

Using Cuisine:

```py
    j.tools.prefab.local.web.portal.install(mongodbip="<IP address of machine with MongoDB>", mongoport="<MondoDB port>")
```
