from comparators.parameter_matcher import ParameterMatcher

matcher = ParameterMatcher()

candidates = [

    {
        "parameter": "Minimum/ Maximum Maturity Age",
        "text": "Maximum maturity age allowed.",
        "similarity": 88,
        "version": 2,
        "filename": "Version2.docx"
    },

    {
        "parameter": "Maximum Entry Age",
        "text": "Maximum age at entry.",
        "similarity": 86,
        "version": 2,
        "filename": "Version2.docx"
    },

    {
        "parameter": "Policy Term",
        "text": "Policy duration.",
        "similarity": 84,
        "version": 2,
        "filename": "Version2.docx"
    }

]

result = matcher.match(

    source_parameter="Minimum Entry Age",

    source_description="Minimum age at which the policy can be purchased.",

    candidates=candidates

)

print(result)