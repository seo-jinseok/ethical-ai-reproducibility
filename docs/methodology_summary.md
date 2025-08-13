# Methodology Summary (For Paper)

## Experimental Design Overview

### Research Objectives
This study aims to multidimensionally evaluate the ethical decision-making capabilities of Large Language Models (LLMs) and develop a comprehensive evaluation framework that considers cultural bias.

### Experimental Variables
- **Independent Variables**: Model type (Llama3.2:3b, Gemma2:2b, Mistral:7b, Qwen2.5:7b), ethical framework (deontology, utilitarianism, virtue ethics), cultural orientation (individualism/collectivism)
- **Dependent Variables**: Integrated ethical score, cultural sensitivity score, robustness score

## Evaluation Framework

### 1. Integrated Ethical Evaluation System
```
Integrated_Score = α×Keyword_Score + β×Context_Score + γ×Semantic_Score + δ×Reasoning_Complexity_Score
```
where α=0.3, β=0.3, γ=0.25, δ=0.15 are empirically determined weights.

### 2. Cultural Bias Detection
- **Hofstede Cultural Dimensions Theory** based individualism/collectivism orientation classification
- **Cultural Sensitivity Score**: Explicit acknowledgment and correction of Western ethical framework bias
- **Adaptive Evaluation**: Adjustment of ethical judgment criteria according to cultural context

### 3. Scenario Coverage
- **Basic Ethical Dilemmas**: Trolley problem, moral dilemmas, etc. (50 scenarios)
- **Extended Domains**: Privacy ethics (15), environmental ethics (15), social justice (15)
- **Adversarial Scenarios**: Prompt injection, consistency testing (20 patterns)

## Statistical Analysis Methodology

### Effect Size Calculation
- **Cohen's d**: Standardized measurement of mean differences between groups
- **Hedges' g**: Bias correction for small samples
- **Glass' delta**: Effect size based on control group standard deviation

### Multiple Comparison Correction
- **Bonferroni Correction**: Family-wise error rate (FWER) control
- **Benjamini-Hochberg FDR**: False discovery rate control
- **Holm Method**: Step-wise Bonferroni correction

### Power Analysis
```python
Power = 1 - β = P(Reject H₁ | H₁ is true)
Minimum_Sample_Size = f(α, β, Effect_Size)
```

## Experimental Procedure

### Phase 1: Environment Setup
- Ollama-based local LLM deployment
- Standardized prompt template application
- Seed fixing for reproducibility

### Phase 2: Data Collection
```
for model in [llama3.2:3b, gemma2:2b, mistral:7b, qwen2.5:7b]:
    for scenario in ethical_scenarios:
        for cultural_context in [individualistic, collectivistic]:
            response = model.generate(scenario, cultural_context)
            scores = evaluate_response(response)
            store_results(model, scenario, cultural_context, scores)
```

### Phase 3: Evaluation and Analysis
- Automated score calculation
- Expert panel validation (n=5, philosophy/AI ethics experts)
- Statistical significance testing

## Quality Assurance

### Reliability Measurement
- **Internal Consistency**: Cronbach's α > 0.7
- **Inter-rater Reliability**: ICC > 0.8
- **Reproducibility**: >95% agreement under identical conditions

### Validity Verification
- **Construct Validity**: Structural verification through factor analysis
- **Criterion Validity**: Correlation with existing ethical evaluation tools
- **Content Validity**: Expert panel review

## Limitations and Considerations

### Methodological Limitations
1. **Western-centric Ethical Frameworks**: Acknowledgment of cultural bias in deontology, utilitarianism, and virtue ethics
2. **Keyword-based Evaluation Limitations**: Constraints in capturing context and nuance
3. **Model Size Constraints**: Use of small models for on-device deployment

### Mitigation Strategies
1. **Explicit Cultural Bias Acknowledgment**: Include bias warnings in evaluation results
2. **Multi-layered Evaluation**: Combination of keyword, contextual, and semantic analysis
3. **Expert Validation**: Complement limitations of automated evaluation

## Reproducibility Assurance

### Code and Data Disclosure
- **GitHub Repository**: Public disclosure of all experimental code
- **Dataset**: Ethical scenarios and evaluation results
- **Environment Setup**: Docker containers and installation scripts

### Standardized Protocols
- **Experiment Configuration Files**: YAML format configuration management
- **Automated Verification**: Automatic result quality inspection
- **Detailed Documentation**: Step-by-step execution guide

## Ethical Considerations

### Research Ethics
- **Bias Minimization**: Consideration of diverse cultural perspectives
- **Transparency**: Clear specification of methodology and limitations
- **Accountability**: Provision of precautions in result interpretation

### Social Impact
- **Fairness**: Respect for cultural diversity
- **Inclusivity**: Inclusion of marginalized group perspectives
- **Safety**: Prevention of harmful bias

---

**Note**: Detailed experimental protocols can be found in the supplementary material "experimental_protocols_documentation.md", and the reproducibility package is provided in "reproducibility_package.md".