"""This library is used to update any nested dict and list object .


How to use :

DictUpdater : Used to map  operation and dictionary update data .

    @param
    operation_mapping :{ dictionary path separated by dot or ->  : {
             {
                "operation": "update/delete/append",
                "key": "versionnumber"
            }
    }}


Example 1:

sample.py

    value_1 = {"metafilesList": [{
        "groupname": "",
        "filetype": "CLI",
        "appversion": "1",
        "version": "1",
        "metafileobjectsList": [{
            "filename": "filename",
            "tempurl": ""}]},
        {
            "groupname": "",
            "filetype": "CLI",
            "appversion": "1",
            "version": "2",
            "metafileobjectsList": [{
                "filename": "filename",
                "tempurl": ""}, {
                "filename": "filename2",
                "tempurl": ""}]}]}

    # Step 1 : Create a operation mapping , All keys are path to update for operation
    # operation : update
    # key : it used for searching dict object in a list
    operation_mapping = {
        "metafilesList": {
            "operation": "update",
            "key": "version"
        },
        "metafilesList->metafileobjectsList": {
            "operation": "update",
            "key": "filename"
        }}

    # Step 2 Create Update value mapping
    update_value = {"metafilesList": [
        {
            "version": "2",
            "metafileobjectsList": [{
                "filename": "filename",
                "tempurl": "new value"}]}]}

    DictUpdater(operation_mapping=operation_mapping).recursive_dict_updater(data=value_1,
                                                                            update_value=update_value)
    print(value_1)

    # For delete and append operation , replace metafilesList->metafileobjectsList , operation : append or delete



Update :
Data        Update Value   Operation
Dict        Dict           Update All
List        Dict           Search in List , If it finds , update it .
Dict        List           No Need to further check.
List        List           Search every element in  update value in data , if it finds update it .




"""
import logging
from copy import deepcopy

_supported_operation = {"update", "append", "delete", "update_append", "search"}


class DictUpdater:
    class Operation:
        UPDATE = "update"
        UPDATE_APPEND = "update_append"
        APPEND = "append"
        DELETE = "delete"
        SEARCH = "search"

    def __init__(self, operation_mapping=None, seperator="->", opr_sep="::", path_check_only=False):

        self._logger = logging.getLogger(__name__)
        self._opr_sep = opr_sep
        self._seperator = seperator
        self._path_operation = path_check_only

        if operation_mapping is None:
            operation_mapping = {}
        self.default_operation = operation_mapping

    def _recursive_dict_updater(
            self,
            data,
            update_value,
            base_path=""):
        """It updates exiting data with update value ,

        @param data: Dictionary data which need to updated
        @param update_value: Value through which dictionary data get updated .
        @param base_path: It required to check mapping for operation.
        @return:
        """
        self._logger.info(base_path)
        base_path = base_path.strip(self._seperator)

        # Check already specified operation define for search
        operation = self.default_operation.get(base_path)

        if operation and type(data) == dict and operation["key"] in data.keys() and self._path_operation:
            opr = operation["operation"]

            if opr in (self.Operation.UPDATE, self.Operation.UPDATE_APPEND):
                return self._update_operation(data=data, search_key=operation["key"],
                                              update_value=update_value, base_path=base_path)
            if opr == self.Operation.APPEND:
                return self._append_operation(data=data, update_value=update_value)

            if opr == self.Operation.DELETE:
                return self._delete_operation(data=data, update_value=update_value, operation=operation)

        if isinstance(update_value, dict) :
            for key, each_value in update_value.items():

                if not data.get(key) and self._path_operation:
                    continue

                if not data.get(key) and not self._path_operation:
                    data[key] = each_value
                    continue

                # Update again recursively to validate changes
                data[key] = self._recursive_dict_updater(
                    data=data[key],
                    update_value=each_value,
                    base_path=base_path + self._seperator + str(key))

            # Return the update data dict
            return data

        # if instance is list and contain is dictionary
        if isinstance(update_value, list) and len(update_value) > 0:  # and isinstance(update_value[0], dict)

            # Check data dict also have type dict and if contain list is empty
            # then no need to perform operation
            if isinstance(data, list) and len(data) < 0:
                return update_value

            if isinstance(data, list) and len(data) > 0 and not isinstance(data[0], dict):
                ValueError(
                    f"You try to update non dictionary object : {data} and base path : {base_path}")

            # If no operation define
            if not operation:
                if self._path_operation and type(update_value) == list and type(data) == list:
                    return self.path_operation_only(data=data, update_value=update_value, base_path=base_path)
                return update_value

            if operation and self._path_operation and type(update_value) == list and type(data) == list \
                    and not (operation["operation"] == self.Operation.APPEND):
                return self.path_operation_only(data=data, update_value=update_value, base_path=base_path)

            if operation and (operation["operation"] == DictUpdater.Operation.UPDATE or operation[
                "operation"] == DictUpdater.Operation.UPDATE_APPEND):
                search_key = operation.get("key")

                return self._update_operation(base_path, data, search_key, update_value)

            if operation and operation["operation"] == DictUpdater.Operation.APPEND:
                return self._append_operation(data, update_value)

            if operation and operation["operation"] == DictUpdater.Operation.DELETE:
                return self._delete_operation(data, operation, update_value)



        # TODO : Implement string replacement algo
        elif isinstance(update_value, list) and len(update_value) > 0 and isinstance(update_value[0], str):
            # Check already specified operation define for search
            pass
        else:
            # Override the list as specified operation not mention
            return update_value

    def _delete_operation(self, data, operation, update_value):

        # data -> list and updated_value -> dict
        if type(data) == list and type(update_value) == dict:
            for index, value in enumerate(update_value):
                search_key = operation.get("key")
                search_value = value.get(search_key)
                found = False
                for data_index, data_value in enumerate(data):
                    if search_value == data_value.get(search_key):
                        del data[data_index]
                        found = True

                if not found:
                    self._logger.warning(
                        f"search key:{search_key} value:{search_key}  not found")
        return data

    def _append_operation(self, data, update_value):
        if not (type(data) == list):
            return data
        for index, value in enumerate(update_value):
            data.append(value)
        return data

    def path_operation_only(self, data: list, update_value: list, base_path=""):

        if len(update_value) == 0:
            return data

        for data_index, data_value in enumerate(data):
            for each_update_value in update_value:
                data[data_index] = self._recursive_dict_updater(data=data_value, update_value=each_update_value,
                                                                base_path=base_path)

        return data

    def _update_operation(self, base_path, data, search_key, update_value):
        # search if it is present else append
        operation = self.default_operation.get(base_path)

        if type(update_value) == list:
            for index, value in enumerate(update_value):
                search_value = value.get(search_key)
                if search_value is None:
                    data.append(value)
                    continue

                replace_value = None
                if type(search_value) == str and self._seperator in search_value:
                    split_result = search_value.split(self._seperator)
                    search_value = split_result[0]
                    replace_value = split_result[-1]

                found = False
                for data_index, data_value in enumerate(data):
                    if search_value == data_value.get(search_key):
                        # data[data_index] = value
                        data[data_index] = self._recursive_dict_updater(
                            data=data[data_index], update_value=value, base_path=base_path)

                        if replace_value:
                            data[data_index][search_key] = replace_value

                        found = True

                if not found:
                    if operation["operation"] == DictUpdater.Operation.UPDATE_APPEND:
                        data.append(value)
                # data.append(value)

        if type(update_value) == dict and type(data) == dict and update_value.get(search_key) == data.get(search_key):
            for each_key in update_value.keys():

                if data.get(each_key) is None:
                    data[each_key] = update_value[each_key]
                    continue

                data[each_key] = self._recursive_dict_updater(data=data[each_key],
                                                              update_value=update_value[each_key],
                                                              base_path=base_path + self._seperator + each_key)

            # data.update(update_value)

        return data

    @staticmethod
    def update(data, update_value, operation_mapping=None, separator="->", opr_sep="::", data_muted=True,
               path_check_only=False):

        if not data_muted:
            data = deepcopy(data)

        update_obj = DictUpdater(operation_mapping=operation_mapping, seperator=separator, opr_sep=opr_sep,
                                 path_check_only=path_check_only)
        update_obj._generate_valid_search_mapping(deepcopy(operation_mapping))
        return update_obj._recursive_dict_updater(data=data, update_value=update_value)

    def _generate_valid_search_mapping(self, search_mapping: dict):
        key: str
        for key, value in search_mapping.items():

            if self._opr_sep in key:
                separate_val = key.rsplit(self._opr_sep)
                new_key = separate_val[0]
                operation = separate_val[1]

                if operation.lower() not in _supported_operation:
                    raise ValueError("Mapping operation not proper , "
                                     "It support these operation only :{} ".format(_supported_operation))

                del self.default_operation[key]
                self.default_operation[new_key] = {"operation": operation,
                                                   "key": value
                                                   }
            else:
                if not (type(value) == dict):
                    raise ValueError(f"Operation Mapping value not proper , key : {key}, value : {value}")


if __name__ == '__main__':
    value_1 = {"metafilesList": [{
        "groupname": "",
        "filetype": "CLI",
        "appversion": "1",
        "version": "1",
        "metafileobjectsList": [{
            "filename": "filename",
            "tempurl": ""}]},
        {
            "groupname": "",
            "filetype": "CLI",
            "appversion": "1",
            "version": "2",
            "metafileobjectsList": [{
                "filename": "filename",
                "tempurl": ""}, {
                "filename": "filename2",
                "tempurl": ""}]}]}

    # Step 1 : Create a operation mapping , All keys are path to update for operation
    # operation : update
    # key : it used for searching dict object in a list
    operation_mapping_value = {
        "metafilesList": {
            "operation": "update",
            "key": "version"
        },
        "metafilesList->metafileobjectsList": {
            "operation": "update",
            "key": "filename"
        }}

    # Step 2 Create Update value mapping
    update_value_required = {"metafilesList": [
        {
            "version": "2",
            "metafileobjectsList": [{
                "filename": "filename->kunal",
                "tempurl": "new value"}]}]}

    DictUpdater.update(data=value_1, update_value=update_value_required)

    from pprint import pprint

    pprint(value_1)

    # Step 2 Updating the search key (use case 1)
    # filename2 get replace with new demo
    update_value_required = {"metafilesList": [
        {
            "version": "2",
            "metafileobjectsList": [{
                "filename": "filename2->new demo",
                "tempurl": "new value"}]}]}

    DictUpdater.update(
        data=value_1,
        update_value=update_value_required,
        operation_mapping=operation_mapping_value
    )
    from pprint import pprint

    pprint(value_1)

    # For delete and append operation , replace
    # metafilesList->metafileobjectsList , operation : append or delete
