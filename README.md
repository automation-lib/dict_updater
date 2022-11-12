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

#### Updating Recursive dictionary with list object.
Updating dictionary with listing object which again contain dictionary object, Normal recursive update operation will 
fail to update these type value because it required extra search layer. To tackle this issue DictUpdater.update have 
extra parameter which help to identify key and update value .

operation mapping value structure 
```text
{  
< search path separated by seperator(->)::operation : search_key
 }
```
Let's understand what is search path 
Bellow  given dictionary object which contain list  .
```python
source = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": "required_to_update",
                    "value": "target"
                },
                {},
                {}
            ]
        },
        {}
    ]
}
```
There is 'target' value is present . If you look carefully there is path generated from root location . 
which is 'a->b', So technically search path in list contain value is a dictionary key path followed by seperator . 

Let try to understand , what is search value ? . In a list of dictionary , which dictionary object we want to update . 
Means filter dictionary by  search.  
```text
{ 
  a::operation : search,
  a->b:operation : c,
}

"search" and "c" are dictionary key which help to indentify dict objet . 
```
   
What kind of operation currently it supports . 
update : update the all search dictionary .
update_append : update the all search dictionary ,if it failed then append the value in list.
insert : it is default operation . 
append : it append the value in dictionary . 
delete : it delete the dict value in list.

### Example to update recursive list dictionary object . 
Update the only target value
```python
from dictupdate import DictUpdater
from pprint import pprint as pp

source = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": "required_to_update",
                    "value": "target"
                },
                {},
                {}
            ]
        },
        {}
    ]
}

# things which required to update must have exact structure .
update_value = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": "required_to_update",
                    "value": "new_value"
                }
            ]
        }
    ]
}
print("-------------- Before Update --------------")
pp(source)

new_value = DictUpdater.update(data=source, update_value=update_value, operation_mapping={
    "a::update_append": "search",
    "a->b::update_append": "c"
}, data_muted=False)

print("-------------- After Update --------------")
pp(new_value)

```

#### Output :
```commandline
-------------- Before Update --------------
{'a': [{'b': [{'c': 'required_to_update', 'value': 'target'}, {}, {}],
        'search': 1},
       {}]}
-------------- After Update --------------
{'a': [{'b': [{'c': 'required_to_update', 'value': 'new_value'}, {}, {}],
        'search': 1},
       {}]}

```








