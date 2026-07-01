class ParameterCleaner:

    def is_valid_parameter(
            self,
            parameter,
            description):

        parameter = parameter.strip().lower()

        invalid_parameters = [

            "parameters",

            "features",

            "parameter",

            "benefits"

        ]

        if parameter in invalid_parameters:

            return False

        if len(parameter) < 3:

            return False

        return True