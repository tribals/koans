# In search for "schemas" of Python data structures

Currently, this does not work (as expected?):

```console
$ poetry install
$ poetry run python -im users
>>> data
User(id=42, member_since=pendulum.now(), full_name='Anthony', email='anthony@example.com', permissions=(Permission(description='read_users'), Permission(description='manage_users')))
```
