# Dict Updater
It used to update any nested dict and list object . Also provide the option 
to update nested dictionary within the list by searching mechanism . 

### Feature Offer : 
- Update the dictionary object .
- Delete nested dictionary value .
- Append nested list object .


### How to Install the library 
```bash
pip install dictupdate
```

### Example 
#### Updating simple dictionary object 
```python
from dictupdate import DictUpdater

# source to update 
source = {
    "a" : {
        "b": "value_need_to_update"
    }
}

# target to update
target = {
    "a":{
        "b": "existing value updated",
        "c": "new value added"
    }
}

dict_update = DictUpdater.update(
    data=source,
    update_value=target
)

print(dict_update)
```
#### Output :
```
{'a': {'b': 'existing value updated', 'c': 'new value added'}}
```

#### Updating Recursive 






