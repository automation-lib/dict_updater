from dictupdate import DictUpdater
from pprint import pprint as pp

source = {
    "a": [
        {
            "search": 2,
            "b": [
                  {
                      "c": "required_to_update",
                      "value": "target"
                  },
                  {},
                  {}
                  ]
        },
        {
            "search": 1,
            "b": [
                  {
                      "c": "required_to_update_1",
                      "value": "target",
                      "value_2": "target"
                  },
                  {},
                  {}
                  ]
        }
    ]
}

update_value = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": "required_to_update_1",
                    "value": "new_value"
                }
            ]
        }
    ]
}
print("-------------- Before Update --------------")
pp(source)

new_value = DictUpdater.update(data=source, update_value=update_value, operation_mapping={
    # "a::update": "search",
    "a->b::delete": "c"
}, data_muted=False, path_check_only=True)

print("-------------- After Update --------------")
pp(new_value)
