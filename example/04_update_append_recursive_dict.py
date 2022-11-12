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

update_value = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": "search_criteria_fail",
                    "value": "new_value"
                }
            ]
        }
    ]
}
print("-------------- Before Update --------------")
pp(source)

new_value = DictUpdater.update(data=source, update_value=update_value, operation_mapping={
    "a::update": "search",
    "a->b::update_append": "c"
}, data_muted=False)

print("-------------- After Update --------------")
pp(new_value)

