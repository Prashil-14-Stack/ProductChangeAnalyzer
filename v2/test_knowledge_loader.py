from v2.knowledge.knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader()

print("=" * 60)
print("KNOWLEDGE LOADER TEST")
print("=" * 60)

tests = [
    "Death Benefit during PT",
    "PT",
    "Premium Frequency",
    "Policy Loan",
    "Random Parameter"
]

for test in tests:

    print(f"{test:35} --> {loader.get_canonical_name(test)}")

print()

print(f"Total Aliases Loaded : {loader.total_aliases()}")