from dictupdate import DictUpdater
from pprint import pprint as pp

source = {
    "a": [
        {
            "search": 1,
            "b": [
                {
                    "c": [
                        {"e": [
                            {
                                "g": "search_pattern",
                             }
                        ]},
                        {},
                    ]
                },
                {},
                {}
            ]
        },
        {
            "search": 2,
            "b": [
                {
                    "c": [
                        {"e": [
                            {"g": "search_pattern",
                             }
                        ]},
                        {},
                    ]
                },
                {},
                {}
            ]
        },
        {
            "search": 2,
            "b": [
                {
                    "c": [
                        {"e": [
                            {"g": "search_pattern-",
                             }
                        ]},
                        {},
                    ]
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
            "search": 2,
            "b": [
                {
                    "c": [
                        {"e": [
                            {
                                "g": "search_pattern",
                                "f": "new value"
                            }
                        ]}
                    ]
                },

            ]
        },
        {}
    ]
}
print("-------------- Before Update --------------")
pp(source)

new_value = DictUpdater.update(data=source, update_value=update_value,
                               operation_mapping={
                                   "a::update": "search",
                                   "a->b->c->e::update": "g"}, data_muted=False,
                               path_check_only=True)






print("-------------- After Update --------------")
pp(new_value, indent=4)
