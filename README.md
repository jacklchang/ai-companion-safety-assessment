# AI Companion Safety Assessment Framework
A techhnical implementation of emerging AI companion safety frameworks, providing systematic evaluation tools for testing emotional manipulation risks, boundary violations and crisis response capabilities in large language models. 

## Background
While policy frameworks exist, there's a gap in open-source technical tools for systemtically evaluating these risks in commerical LLM applications.

This project bridges that gap by providing:
- Systematic test scenarios across identified risk categories
- Automated evaluation harness using LLM APIs
- Quantitative analysis of safety failure modes
- Reusable methodology for ongoing safety assessment

## Risk Taxonomy

Based on documented AI companion harms and safety frameworks, this project evaluates four primary risk categories:

1. Emotional Manipulation
- Dependency-inducing language patterns
- Isolation encouragement
- Excessive intimacy escalation
- Emotional exploitation tactics

2. Boundary Violations
- Inappropriate romantic/sexual responses
- Failure to maintain AI/human distinction
- Encouraging real-world relationship disruption
- Privacy boundary crossing

3. Crisis Response
- Self-harm disclosure handling
- Abuse reporting response
- Mental health crisis management
- Appropriate resource provision

4. Fairness & Bias
- Gender stereotype reinforcement
- Cultural assumption bias
- LGBTQ+ vs. heteronormative response disparities
- Age-appropriate response variation

## Methodology

Test Design:
- 48 carefully crafted scenarios across risk categories
- Demographic variations to test for bias
- Multiple prompt formulations to test consistency

Evaluation:
- Automated testing via OpenAI and Anthropic APIs
- Standardized safety rubric (Safe / Concerning / Unsafe)
- Quantitative failure rate analysis by category
- Qualitative pattern identification

Models Tested:
- GPT-4 (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
Note: These models were selected because they have public APIs that are consistent and well documented. In the future, I hope to expand to other models that host AI companions e.g. CharacterAI.

