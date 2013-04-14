"""The idea is that Seshat code should be independent of the backend database. To use a different datastore, create a new module with a class called Datastore. 

The Datastore class should have the following methods:
``
search(self, type, field, value)
new(self, type)
``

Where 'type' is one of the following object types:

Paper
Author
DSpace_Object
Corpus

The search() method should return an object that provides the following methods for interacting with entities in the datastore:

```
put() -- update the datastore entity with the current object state.
```
"""