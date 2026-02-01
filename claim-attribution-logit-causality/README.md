# Claim Attribution via Logit Causality

This project explains *why* a factual claim appeared in an LLM output
by identifying which earlier tokens were causally necessary.

Key properties:
- Architecture-first
- No attention or gradient visualizations
- Uses logits, probabilities, and counterfactual testing
- Explicit refusal when attribution is not defensible

This is a post-hoc causal verification system, not a reasoning visualizer.