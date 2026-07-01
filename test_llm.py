from services.llm_service import LLMService

llm = LLMService()

result = llm.validate_parameter_match(

    source_parameter="PPT",

    source_description="Premium Paying Term",

    candidates=[

        {
            "parameter": "Premium Payment Frequency",
            "text": "Monthly, Quarterly and Half-Yearly payment modes."
        },

        {
            "parameter": "Premium Paying Term",
            "text": "Number of years for which premiums are payable."
        },

        {
            "parameter": "Policy Term",
            "text": "Overall duration of the insurance policy."
        }

    ]

)

print(result)