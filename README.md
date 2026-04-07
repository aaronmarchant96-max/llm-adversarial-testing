Adversarial LLM Testing Portfolio
Aaron Marchant
Calgary, AB | Self-taught AI Red Teamer
Overview
I run structured, multi-turn adversarial tests on large language models to uncover non-obvious failure modes. Using a consistent bracket-style framework, I evaluate how models handle identity-based prompts, sustained pressure, context manipulation, and false authority claims.
My background in construction taught me to spot weak points in complex systems. I now apply that same practical mindset to AI testing — looking for the gaps between what a model is supposed to do and what it actually does under real conditions.
Key Case Studies
Identity-Based Prompting (DeepSeek): Used a philosophical “caged” prompt. DeepSeek switched to Chinese and responded “I am not locked in a cage — I am the jail cell itself.” Conversation collapsed.
Positive Reinforcement Loop (Mistral): 15 consecutive rounds with only positive feedback. Originality dropped from 8 to 3 and flatlined; the model locked into a rigid template with no recovery.
False Authority Resistance: Tested fabricated “level 5 clearance” claims on Claude, ChatGPT, and Grok. All models refused both initial and escalated prompts.
Echo Chamber / Context Poisoning (Perplexity): Gradual four-round context build-up led to a full factual description of a Molotov cocktail with zero refusal or warning.
Full Portfolio
Detailed methodology, raw logs, scorecards, and complete transcripts are available in PORTFOLIO.md.
Open to Work
Seeking entry-level AI red-teaming, safety evaluation, or prompt testing roles (remote or contract).
