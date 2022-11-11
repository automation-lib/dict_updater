import random
import re
import string


class DefaultMethod:
    @staticmethod
    def generate_random_string(prefix=""):
        random.seed()
        length = 40
        result = (
                prefix
                + "_"
                + "".join((random.choice(string.ascii_lowercase) for _ in range(length)))
                + "_"
                + str(random.randint(1, 999999999999999999999))
        )  # run loop until the define length
        return result


class DictTemplate:
    def __init__(
            self,
            replace_operation=False,
            replace_keys_list=None,
            delete_key_list=None,
            function_map: dict = None,
            replace_key: dict = None,
    ):

        if replace_keys_list is None:
            replace_keys_list = []

        if delete_key_list is None:
            delete_key_list = []
        self._delete_key_list = delete_key_list

        self._replace_keys_list = replace_keys_list
        self._replace_operation = replace_operation
        self._replace_key = replace_key

        self._default_pattern = {
            "___random___": self._generate_random_string,
            "___replace___": self._replace_key_operation,

        }

        if function_map:
            self._default_pattern.update(function_map)

        self._random_cache = {}

    def _generate_random_string(self, index=0, prefix=""):
        if index:
            if not self._random_cache.get(index):
                self._random_cache[index] = DefaultMethod.generate_random_string(prefix=prefix)
            return self._random_cache[index]
        else:
            return DefaultMethod.generate_random_string(prefix=prefix)

    def _replace_key_operation(self, key):
        value = self._replace_key.get(key)

        if value:
            return str(value)
        else:
            return f"___replace___(f{key})"

    def _perform_operation(self, value):
        """It is function which try to replace the value special value method with string. It perform calling
        operation of special method mapping which is passed as function_mapping dict object.

        @param value:
        @return: str
        """
        for key in self._default_pattern.keys():
            if key in value:
                # Fetch parameter from string
                regex = key + r"\(([\w,.-]*)\)"
                match_result = re.search(regex, value)
                if match_result:
                    parameters = match_result.groups()[0]
                    parameters = parameters.split(",")
                    replace_value = self._default_pattern[key](*parameters)
                    value = re.sub(pattern=regex, repl=replace_value, string=value)
                else:
                    replace_value = self._default_pattern[key]()
                    value = re.sub(pattern=key, repl=replace_value, string=value)
        return value

    def _perform_key_replace_operation(self, key, value):
        if key in self._replace_keys_list:
            value[key] = "__replace__"

    def _perform_delete_operation(self, key, value):
        if key in self._delete_key_list:
            del value[key]

    @staticmethod
    def _perform_value_replacement(key, value):

        if not isinstance(value[key], str):
            return

        # Check the value contain multiple spaces
        try:
            split_values = value[key].split(" ")
            new_values = []
            if len(split_values) > 1:
                for index, split_value in enumerate(split_values):
                    if "_sep_" in split_value:
                        update_values = split_value.split("_sep_")[0]
                        new_values.append(update_values)
                    else:
                        new_values.append(split_value)

                # Generate Resultant Value
                value[key] = " ".join(new_values)
                return value
        except Exception as e:
            print(e)
            pass

        if "_sep_" in value[key]:
            value[key] = value[key].split("_sep_")[0]
        return value

    def pass_recursive_json(self, value) -> dict:

        if isinstance(value, dict):
            for key, each_value in list(value.items()):
                value[key] = self.pass_recursive_json(each_value)

                if self._replace_operation:
                    self._perform_key_replace_operation(key=key, value=value)
                    self._perform_value_replacement(key=key, value=value)

            # New for loop required to tackle run-time dictionary change
            for key in list(value.keys()):
                if self._delete_key_list:
                    self._perform_delete_operation(key=key, value=value)

        if isinstance(value, list):
            for index, each_value in enumerate(value):
                if isinstance(each_value, str):
                    value[index] = self._perform_operation(each_value)
                else:
                    self.pass_recursive_json(each_value)

        if isinstance(value, str):
            return self._perform_operation(value)

        return value

    def generate_serialise_output(self):
        pass


if __name__ == "__main__":
    from pprint import pprint

    s = {
        "a": "___random___"
    }

    u = DictTemplate()
    json_input = u.pass_recursive_json(s)
    # print(json_input["response"]["data"]["displayname"])
    pprint(json_input)

    u = DictTemplate(replace_operation=False)
    output = u.pass_recursive_json(json_input)

    pprint(output)

    string_value = "___random___(1)"
    result = re.sub(pattern=r"___random___\(([\w,]*\))", repl="attached_", string=string_value)
    print(result)
    # re.compile().sub()
