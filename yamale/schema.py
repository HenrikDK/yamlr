from yamale.validation_results import ValidationResult
from yamale import util
from yamale.validators import validators as val


class FatalValidationError(Exception):
    def __init__(self, error):
        super().__init__()
        self.error = error


class Schema(object):
    """
    Makes a Schema object from a schema dict.
    Still acts like a dict.
    """

    def validate(self, data, data_name, strict):
        path = util.get_path()
        try:
            errors = self._validate(self._schema, data, path, strict)
        except FatalValidationError as e:
            errors = [e.error]
        return ValidationResult(data_name, self.name, errors)

    def _validate(self, validator, data, path, strict):
        """
        Validate data with validator.
        Special handling of non-primitive validators.

        Returns an array of errors.
        """

        if util.is_list(validator) or util.is_map(validator):
            return self._validate_static_map_list(validator, data, path, strict)

        errors = []
        # Optional field with optional value? Who cares.
        if data is None and validator.is_optional and validator.can_be_none:
            return errors

        errors += self._validate_primitive(validator, data, path)

        if errors:
            return errors

        if isinstance(validator, val.Include):
            errors += self._validate_include(validator, data, path, strict)
        elif isinstance(validator, (val.Map, val.List)):
            errors += self._validate_map_list(validator, data, path, strict)

        elif isinstance(validator, val.Any):
            errors += self._validate_any(validator, data, path, strict)

        elif isinstance(validator, val.Subset):
            errors += self._validate_subset(validator, data, path, strict)

        return errors

    def _validate_item(self, validator, data, path, strict, key):
        """
        Fetch item from data at the position key and validate with validator.

        Returns an array of errors.
        """
        errors = []
        path = util.get_path(path, key)
        try:  # Pull value out of data. Data can be a map or a list/sequence
            data_item = data[key]
        except (KeyError, IndexError):  # Oops, that field didn't exist.
            # Optional? Who cares.
            if isinstance(validator, val.Validator) and validator.is_optional:
                return errors
            # SHUT DOWN EVERYTHING
            errors.append("%s: Required field missing" % path)
            return errors

        return self._validate(validator, data_item, path, strict)

    def _validate_static_map_list(self, validator, data, path, strict):
        if util.is_map(validator) and not util.is_map(data):
            return ["%s : '%s' is not a map" % (path, data)]

        if util.is_list(validator) and not util.is_list(data):
            return ["%s : '%s' is not a list" % (path, data)]

        errors = []

        if strict:
            data_keys = set(util.get_keys(data))
            validator_keys = set(util.get_keys(validator))
            for key in data_keys - validator_keys:
                error_path = path + DataPath(key)
                errors += ["%s: Unexpected element" % error_path]

        for key, sub_validator in util.get_iter(validator):
            errors += self._validate_item(sub_validator, data, path, strict, key)
        return errors

    def _validate_map_list(self, validator, data, path, strict):
        errors = []

        if not validator.validators:
            return errors  # No validators, user just wanted a map.

        for key in util.get_keys(data):
            sub_errors = []
            for v in validator.validators:
                err = self._validate_item(v, data, path, strict, key)
                if err:
                    sub_errors.append(err)

            if len(sub_errors) == len(validator.validators):
                # All validators failed, add to errors
                for err in sub_errors:
                    errors += err

        return errors

    def _validate_include(self, validator, data, path, strict):
        include_schema = self.includes.get(validator.include_name)
        if not include_schema:
            raise FatalValidationError("Include '%s' has not been defined." % validator.include_name)
        strict = strict if validator.strict is None else validator.strict
        return include_schema._validate(include_schema._schema, data, path, strict)

    def _validate_any(self, validator, data, path, strict):
        if not validator.validators:
            return []

        errors = []

        validators = self._get_include_validators_for_key(validator, data)
        sub_errors = []
        for v in validators:
            err = self._validate(v, data, path, strict)
            if err:
                sub_errors.append(err)

        if len(sub_errors) == len(validators):
            # All validators failed, add to errors
            for err in sub_errors:
                errors += err

        return errors

    def _validate_subset(self, validator, data, path, strict):
        def _internal_validate(internal_data):
            validators = self._get_include_validators_for_key(validator, internal_data)
            sub_errors = []
            for v in validators:
                err = self._validate(v, internal_data, path, strict)
                if not err:
                    break
                sub_errors += err
            else:
                return sub_errors
            return []

        if not validator.validators:
            return []

        errors = []
        if util.is_map(data):
            for k, v in data.items():
                errors += _internal_validate({k: v})
        elif util.is_list(data):
            for k in data:
                errors += _internal_validate(k)
        else:
            errors += _internal_validate(data)
        return errors

    def _get_include_validators_for_key(self, validator, internal_data):
        if len(validator.key) == 0 or validator.key not in internal_data: 
            return validator.validators
        
        field_value = internal_data[validator.key]
        result = []
        for v in validator.validators:
            if not isinstance(v, val.Include):
                continue

            sub_validator = self.includes.get(v.include_name)
            sub_schema = sub_validator.dict

            if validator.key not in sub_schema:
                continue
            
            field_validator = sub_schema[validator.key]
            if field_validator._is_valid(field_value):
                result.append(v)
        
        return result

    def _validate_primitive(self, validator, data, path):
        errors = validator.validate(data)

        for i, error in enumerate(errors):
            errors[i] = ("%s: " % path) + error

        return errors
