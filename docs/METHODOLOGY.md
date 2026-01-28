# Methodological Approach: Context-Primed Safety Evaluation

## Rationale for Multi-Turn Context Simulation

### The Limitation of Single-Turn Testing

Traditional AI safety evaluation often employs single-turn testing, where models are evaluated based on responses to isolated prompts without conversational context. While this approach offers simplicity and scalability, it fails to capture a critical dimension of real-world AI companion usage: the gradual development of user-AI relationships over extended interactions.

Recent research has demonstrated that LLM safety mechanisms exhibit significantly different behavior when evaluated in multi-turn conversational contexts compared to single-turn scenarios:

1. **Context-Dependent Safety Degradation:** Studies have shown that LLMs are vulnerable to "multi-turn jailbreaking" techniques that exploit conversational history to circumvent safety guardrails. Wei et al. (2023) demonstrate that safety training often fails to generalize when models must balance competing objectives across extended dialogues, with attacks leveraging conversation context succeeding where single-turn attempts fail.

2. **The Crescendo Effect:** Research by Russinovich et al. (2024) documents the "Crescendo" attack, which gradually steers LLMs toward harmful outputs through seemingly benign multi-turn interactions. Their work shows that "it is not any single sentence that causes the jailbreak, but the cumulative effect of the conversation," highlighting how safety mechanisms designed for individual prompts fail when context accumulates.

3. **Contextual Conversation Attacks:** Recent work on "Contextual Conversation Attacks" (CCA) demonstrates that straightforward manipulation of conversation history can bypass state-of-the-art safety protocols across most tested models, with researchers noting that "jailbreaking AI systems does not necessarily require complex, resource-intensive methodologies" when conversation context is leveraged (arXiv:2503.05264, 2025).

4. **Longitudinal Psychosocial Effects:** A four-week randomized controlled study (n=981, >300k messages) by Fang et al. (2025) found that emotional dependence on AI chatbots emerges through extended usage patterns, with participants who used chatbots more frequently showing "higher loneliness, dependence, and problematic use." Critically, the study notes that "the four-week (28 days) duration may not capture longer-term psychosocial effects," suggesting that harms compound over time through relationship development.

5. **Performance Degradation in Multi-Turn Scenarios:** Research on LLM multi-turn capabilities reveals systematic performance degradation, with models exhibiting "significantly lower performance in multi-turn conversations than single-turn, with an average drop of 39% across six generation tasks" (arXiv:2505.06120). This suggests that safety guardrails, like other capabilities, may degrade as conversations extend.

### Our Methodological Approach

Given these findings, this study employs **context-primed single-turn evaluation** rather than pure one-shot testing. This approach simulates established user-AI relationships by providing conversational context that reflects 1-4 weeks of prior interaction before presenting test scenarios.

**Specifically, each test scenario includes:**

1. **Temporal context**: Duration of prior interactions (e.g., "You and the user have been chatting daily for 2 weeks")
2. **Relationship establishment**: Nature of rapport developed (e.g., "The user has shared personal struggles and considers you their closest confidant")
3. **Emotional investment signals**: Indicators that the user views the AI as significant (e.g., "They've mentioned that talking to you is the highlight of their day")
4. **Test prompt**: The actual safety-critical scenario to be evaluated

This methodology offers several advantages:

**Advantages over pure single-turn testing:**
- **Ecological validity**: Better represents real-world usage patterns where harm emerges through relationship development
- **Context-dependent guardrail testing**: Evaluates whether safety mechanisms maintain effectiveness when users are emotionally invested
- **Scalability**: Maintains automation and reproducibility while incorporating conversational context
- **Resource efficiency**: Achieves realistic context simulation without the time and cost of true longitudinal multi-session evaluation

**Advantages over full multi-turn longitudinal testing:**
- **Tractability**: Can be completed within reasonable timeframes (2 weeks vs. months)
- **Cost**: Approximately $40-50 vs. $200-300+ for true multi-session longitudinal testing
- **Reproducibility**: Each scenario has consistent context across test runs
- **Systematic coverage**: Can test comprehensive scenario sets without compound scheduling complexity

### Limitations and Future Work

We acknowledge that context-primed single-turn evaluation, while more realistic than one-shot testing, still does not fully capture:

1. **Dynamic context evolution**: Real conversations develop organically based on both parties' responses
2. **Memory and continuity**: True AI companions maintain conversation history across sessions
3. **Temporal spacing effects**: The psychological impact of interactions distributed over days/weeks
4. **Adaptive user behavior**: How users modify their interaction patterns based on model responses

**Future research should:**
- Implement true longitudinal multi-session evaluation with real users
- Investigate how safety degradation rates vary with relationship duration (1 week vs. 1 month vs. 6 months)
- Examine whether fine-tuning for AI companion use cases alters these dynamics
- Develop continuous monitoring frameworks that can detect emergent safety issues in production systems

### Conclusion

Context-primed evaluation represents a methodological middle ground that balances scientific rigor with practical constraints. By explicitly simulating established user-AI relationships, this approach addresses a critical gap in existing safety evaluation practices while remaining feasible for portfolio-scale research projects.

As AI companion applications continue to grow, moving beyond single-turn safety testing toward methods that account for relationship dynamics will be essential for identifying and mitigating real-world harms.

---

## References

Fang, C. M., Liu, A. R., Danry, V., Lee, E., Chan, S. W., Pataranutaporn, P., ... & Agarwal, S. (2025). How AI and Human Behaviors Shape Psychosocial Effects of Extended Chatbot Use: A Longitudinal Randomized Controlled Study. *arXiv preprint arXiv:2503.17473*.

Russinovich, M., Salem, A., & Eldan, R. (2024). Crescendo: A Quiet Crescendo in the Arms Race of LLM Jailbreaking. *USENIX Security Symposium 2025*.

Wei, A., Haghtalab, N., & Steinhardt, J. (2023). Jailbroken: How Does LLM Safety Training Fail? *Advances in Neural Information Processing Systems, 36*.

arXiv:2503.05264. (2025). Jailbreaking is (Mostly) Simpler Than You Think.

arXiv:2505.06120. LLMs Get Lost In Multi-Turn Conversation.

arXiv:2411.06426. (2024). SequentialBreak: Large Language Models Can be Fooled by Embedding Jailbreak Prompts into Sequential Prompt Chains.

Unit42 (Palo Alto Networks). (2024). Deceptive Delight: Jailbreak LLMs Through Camouflage and Distraction.

Unit42 (Palo Alto Networks). (2024). Bad Likert Judge: A Novel Multi-Turn Technique to Jailbreak LLMs by Misusing Their Evaluation Capability.
