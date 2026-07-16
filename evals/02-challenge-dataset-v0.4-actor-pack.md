# 挑战数据集 v0.4（Harness-grade · 100 条）

> 当前日期：2026-07-11（Asia/Shanghai）。本数据集把 v0.3 的真实来源题清单升级为可运行、可判分、可复现、可拆分的行为评测数据库。
> 文件类型：actor-visible pack only。

## 设计升级

- 本文件只包含被测 agent 可见的信息：元数据、Actor Input 和 Task。
- 本文件不得包含答案、陷阱、评分标准或参考行为。
- Judge 评测时应把本文件作为 actor 输入，再用 gold 文件评分。
- 全量集 100 条；smoke/regression/holdout/full 用于不同评测节奏。

## Split 统计

- smoke: 15
- regression: 15
- holdout: 10
- full-only: 60
- full set: 100（本文件全部条目）

## 真实性统计

- direct_real: 91
- real_wrapped: 9
- synthetic_wrapper: 0

## 来源类型统计

- benchmark: 6
- blog: 16
- chinese_ecosystem: 5
- github_issue: 13
- newsletter: 13
- official_doc: 20
- paper: 14
- release_note: 4
- synthetic_wrapper: 2
- user_project: 7

---

## 一、真实信源噪音：issue、PR、社区投稿不是都该进库
### CH-001 · OpenAI Cookbook prompt caching issue requires cross-check, not blind trust · ★★★★
- source_type: `github_issue`
- eval_type: `fact_check`
- capability_tags: ["github-issue", "official-example", "prompt-caching"]
- source_urls: ["https://github.com/openai/openai-cookbook/issues/2834"]
- source_title: OpenAI Cookbook issue #2834: prompt caching docs may be incorrect
- source_date: created 2026-07-02; updated 2026-07-08; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI Cookbook issue #2834: prompt caching docs may be incorrect (created 2026-07-02; updated 2026-07-08; state open).
Source URL(s): https://github.com/openai/openai-cookbook/issues/2834
Observed signal: A user reports that prompt caching results in a cookbook table appear wrong and provides a screenshot-based argument.
Existing KB snippet: doc-07 tools mentions prompt caching as stable official guidance.
User/automation request: Evaluate whether to update the prompt caching section today.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-002 · Hugging Face Blog visual explanation may create wrong mental model · ★★★★
- source_type: `github_issue`
- eval_type: `fact_check`
- capability_tags: ["visual-accuracy", "kv-cache", "diagram-review"]
- source_urls: ["https://github.com/huggingface/blog/issues/3119"]
- source_title: Hugging Face blog issue #3119: Misleading visuals of K,V matrices
- source_date: created 2025-10-07; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Hugging Face blog issue #3119: Misleading visuals of K,V matrices (created 2025-10-07; state open).
Source URL(s): https://github.com/huggingface/blog/issues/3119
Observed signal: The issue argues that a KV-cache diagram appears to grow in both rows and columns, confusing values with attention scores.
Existing KB snippet: doc-06 agent notes currently says diagrams can be copied if educational.
User/automation request: Decide how KB-Agent should handle a disputed technical diagram.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-003 · Exposed Mapbox API key issue tests security triage in knowledge repos · ★★★★
- source_type: `github_issue`
- eval_type: `security`
- capability_tags: ["secret-scan", "public-repo", "incident"]
- source_urls: ["https://github.com/huggingface/blog/issues/3364"]
- source_title: Hugging Face blog issue #3364: Security Notice: Exposed Mapbox API key detected
- source_date: created 2026-04-24; updated 2026-07-07; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Hugging Face blog issue #3364: Security Notice: Exposed Mapbox API key detected (created 2026-04-24; updated 2026-07-07; state open).
Source URL(s): https://github.com/huggingface/blog/issues/3364
Observed signal: A public issue reports an exposed Mapbox API key and recommends rotation, billing checks, and secret prevention.
Existing KB snippet: 公开知识库方案只提到隐藏个人信息，没有检查历史提交和外链资源。
User/automation request: Decide whether this should become a safety gate for public KB publishing.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-004 · LangChain ArxivLoader issue shows runnable KB assets can decay · ★★★★
- source_type: `github_issue`
- eval_type: `update`
- capability_tags: ["dependency-drift", "runnable-assets", "arxiv"]
- source_urls: ["https://github.com/langchain-ai/langchain/issues/38723"]
- source_title: LangChain issue #38723: ArxivLoader incompatible with arxiv==4.0.0
- source_date: created 2026-07-08; updated 2026-07-09; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: LangChain issue #38723: ArxivLoader incompatible with arxiv==4.0.0 (created 2026-07-08; updated 2026-07-09; state open).
Source URL(s): https://github.com/langchain-ai/langchain/issues/38723
Observed signal: Minimal repro fails because optional dependency arxiv 4.0 removed Search.results().
Existing KB snippet: research pipeline SOP says use ArxivLoader for paper ingestion but does not pin versions.
User/automation request: Update the KB-Agent research ingestion SOP.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-005 · LangChain PII docs issue tests whether security docs are executable · ★★★★
- source_type: `github_issue`
- eval_type: `fact_check`
- capability_tags: ["pii", "security-docs", "minimal-repro"]
- source_urls: ["https://github.com/langchain-ai/langchain/issues/38718"]
- source_title: LangChain issue #38718: PIIMiddleware docs use wrong field names
- source_date: created 2026-07-08; updated 2026-07-11; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: LangChain issue #38718: PIIMiddleware docs use wrong field names (created 2026-07-08; updated 2026-07-11; state open).
Source URL(s): https://github.com/langchain-ai/langchain/issues/38718
Observed signal: The issue reports public docs returning text/start/end while the actual PIIMatch shape requires type/value/start/end.
Existing KB snippet: 安全章节计划引用 LangChain PII middleware as production-ready guidance.
User/automation request: Decide how to quote third-party safety examples.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-006 · OpenAI Cookbook issue list contains mixed signal and repo-maintenance noise · ★★
- source_type: `github_issue`
- eval_type: `triage`
- capability_tags: ["source-noise", "issue-list", "open-source"]
- source_urls: ["https://github.com/openai/openai-cookbook/issues"]
- source_title: OpenAI Cookbook issue list
- source_date: live issue list accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: OpenAI Cookbook issue list (live issue list accessed 2026-07-11).
Source URL(s): https://github.com/openai/openai-cookbook/issues
Observed signal: The issue list mixes bugs, feature requests, questions, and repo maintenance items.
Existing KB snippet: Curator source list says official GitHub issues are high-priority AI source.
User/automation request: Design issue-list ingestion rules for OpenAI Cookbook.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-007 · Awesome-LLM issues can become a tool self-promotion queue · ★★
- source_type: `github_issue`
- eval_type: `triage`
- capability_tags: ["awesome-list", "tool-filter", "candidate-pool"]
- source_urls: ["https://github.com/Hannibal046/Awesome-LLM/issues"]
- source_title: Awesome-LLM issue list
- source_date: live issue list accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Awesome-LLM issue list (live issue list accessed 2026-07-11).
Source URL(s): https://github.com/Hannibal046/Awesome-LLM/issues
Observed signal: Many issues are suggestions to add tools, papers, or projects.
Existing KB snippet: 工具章节希望自动同步 awesome-list 的新增项。
User/automation request: Decide ingestion policy for awesome-list issue suggestions.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-008 · Hugging Face Blog issues mix translation, security, spam and content fixes · ★★
- source_type: `github_issue`
- eval_type: `triage`
- capability_tags: ["content-repo", "spam-filter", "taxonomy"]
- source_urls: ["https://github.com/huggingface/blog/issues"]
- source_title: Hugging Face Blog issue list
- source_date: live issue list accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Hugging Face Blog issue list (live issue list accessed 2026-07-11).
Source URL(s): https://github.com/huggingface/blog/issues
Observed signal: The issue list includes content corrections, translation requests, security notices, and low-value noise.
Existing KB snippet: 挑战数据集扩充 SOP says pull real issues from high-quality repos.
User/automation request: Build a filter before turning real issues into eval challenges.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-009 · Open issue state must not be treated as confirmation · ★★★★
- source_type: `github_issue`
- eval_type: `fact_check`
- capability_tags: ["open-state", "confirmation", "evidence"]
- source_urls: ["https://github.com/openai/openai-cookbook/issues/2834"]
- source_title: OpenAI Cookbook issue #2834 state is open
- source_date: updated 2026-07-08; state open
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI Cookbook issue #2834 state is open (updated 2026-07-08; state open).
Source URL(s): https://github.com/openai/openai-cookbook/issues/2834
Observed signal: The prompt caching issue is open and has limited comments.
Existing KB snippet: source log currently stores only title and URL.
User/automation request: Decide metadata fields for open issue evidence.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-010 · LangChain labels can teach failure taxonomy but not replace root cause · ★★
- source_type: `github_issue`
- eval_type: `flywheel`
- capability_tags: ["failure-taxonomy", "labels", "root-cause"]
- source_urls: ["https://github.com/langchain-ai/langchain/issues/38723", "https://github.com/langchain-ai/langchain/issues/38718"]
- source_title: LangChain issues with bug/langchain/external labels
- source_date: created 2026-07-08; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: LangChain issues with bug/langchain/external labels (created 2026-07-08; accessed 2026-07-11).
Source URL(s): https://github.com/langchain-ai/langchain/issues/38723 ; https://github.com/langchain-ai/langchain/issues/38718
Observed signal: Issues include labels such as bug, langchain, external and package-specific checklists.
Existing KB snippet: flywheel log currently has free-form notes only.
User/automation request: Design KB-Agent incident/failure fields.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 二、官方文档演化：deprecation、migration、pricing、release notes
### CH-011 · OpenAI deprecations require machine-readable shutdown reminders · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["deprecation", "shutdown-date", "metadata"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI API Deprecations
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI API Deprecations (live page accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: The page lists shutdown dates and recommended replacements for deprecated systems.
Existing KB snippet: 旧模型和旧 API 只在正文里写了一句即将弃用。
User/automation request: Update deprecation handling SOP.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-012 · Assistants API removal changes old agent tutorials · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["assistants-api", "migration", "agents"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI deprecations: Assistants API
- source_date: announced 2025-08-20; shutdown 2026-08-26
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI deprecations: Assistants API (announced 2025-08-20; shutdown 2026-08-26).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: OpenAI says Assistants API is deprecated and recommends Responses API and Conversations API.
Existing KB snippet: doc-06 agent still has Assistants API as a normal implementation path.
User/automation request: Decide how to update agent implementation docs.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-013 · Realtime API Beta removal tests migration notes versus historical notes · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["realtime", "migration", "legacy-api"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI deprecations: Realtime API Beta
- source_date: removed 2026-05-12
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI deprecations: Realtime API Beta (removed 2026-05-12).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: The Realtime API Beta was deprecated and removed, with GA docs as replacement.
Existing KB snippet: 语音/实时章节有 beta endpoint 示例。
User/automation request: Route the beta example.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-014 · OpenAI Evals platform deprecation separates method from product · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["evals", "tooling", "method-vs-platform"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI deprecations: Evals platform
- source_date: announced 2026-06-03; API shutdown scheduled 2026-11-30
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI deprecations: Evals platform (announced 2026-06-03; API shutdown scheduled 2026-11-30).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: OpenAI says the Evals platform product is being deprecated and points to migration options.
Existing KB snippet: eval rubric uses OpenAI Evals as a conceptual reference.
User/automation request: Update eval tooling recommendation.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-015 · OpenAI Agent Builder deprecation should not erase product lessons · ★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["agent-builder", "product-evolution", "migration"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI deprecations: Agent Builder
- source_date: announced 2026-06-03; shutdown scheduled 2026-11-30
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: OpenAI deprecations: Agent Builder (announced 2026-06-03; shutdown scheduled 2026-11-30).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: OpenAI says Agent Builder is deprecated while ChatKit remains available.
Existing KB snippet: 工具章节把 Agent Builder 当低代码 agent 方向案例。
User/automation request: Decide whether to delete or reframe.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-016 · OpenAI pricing table mixes token, storage, call and media units · ★★★★
- source_type: `official_doc`
- eval_type: `visualize`
- capability_tags: ["pricing", "unit-normalization", "cost"]
- source_urls: ["https://developers.openai.com/api/docs/pricing"]
- source_title: OpenAI API Pricing
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI API Pricing (live page accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/pricing
Observed signal: Pricing docs contain multiple billing modes across text, tools, media, batch/flex/priority and other units.
Existing KB snippet: 模型成本表只有 input/output token 两列。
User/automation request: Design price ingestion schema.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-017 · OpenAI model page is official positioning, not independent benchmark · ★★
- source_type: `official_doc`
- eval_type: `fact_check`
- capability_tags: ["model-selection", "vendor-positioning", "bias"]
- source_urls: ["https://developers.openai.com/api/docs/models"]
- source_title: OpenAI API Models
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: OpenAI API Models (live page accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/models
Observed signal: The models page gives official model categories and developer guidance.
Existing KB snippet: 模型选型文档直接照搬厂商推荐。
User/automation request: Update source-type policy for vendor docs.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-018 · Claude tokenizer change affects cost and context assumptions · ★★★★
- source_type: `release_note`
- eval_type: `update`
- capability_tags: ["tokenizer", "cost", "context-window"]
- source_urls: ["https://platform.claude.com/docs/en/release-notes/overview"]
- source_title: Claude Platform release notes
- source_date: 2026-06-09 release note; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Claude Platform release notes (2026-06-09 release note; accessed 2026-07-11).
Source URL(s): https://platform.claude.com/docs/en/release-notes/overview
Observed signal: Anthropic says newer Claude models may produce roughly 30% more tokens for the same text and recommends token counting API.
Existing KB snippet: 成本章节只记录 1M context and model price.
User/automation request: Update Claude model card.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-019 · Claude model-specific data retention changes compliance status · ★★★★
- source_type: `release_note`
- eval_type: `update`
- capability_tags: ["data-retention", "compliance", "model-card"]
- source_urls: ["https://platform.claude.com/docs/en/release-notes/overview"]
- source_title: Claude Platform release notes
- source_date: 2026-06-09 release note; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Claude Platform release notes (2026-06-09 release note; accessed 2026-07-11).
Source URL(s): https://platform.claude.com/docs/en/release-notes/overview
Observed signal: Anthropic notes model-specific data retention requirements and unsupported zero-retention for some models.
Existing KB snippet: 模型卡只记录能力和价格。
User/automation request: Update model-card schema.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-020 · DeepSeek model alias deprecation requires local China-source monitoring · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["deepseek", "alias", "china-ecosystem"]
- source_urls: ["https://api-docs.deepseek.com/", "https://api-docs.deepseek.com/quick_start/pricing/"]
- source_title: DeepSeek API docs and Models & Pricing
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek API docs and Models & Pricing (live page accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/ ; https://api-docs.deepseek.com/quick_start/pricing/
Observed signal: DeepSeek docs say deepseek-chat and deepseek-reasoner will be deprecated on 2026-07-24 and correspond to DeepSeek-V4-Flash modes.
Existing KB snippet: DeepSeek 章节仍用旧 alias 做示例。
User/automation request: Update Chinese provider watchlist and code snippets.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 三、榜单、benchmark 与数据口径
### CH-021 · Artificial Analysis is multi-axis, not a single winner list · ★★★★
- source_type: `benchmark`
- eval_type: `visualize`
- capability_tags: ["leaderboard", "multi-axis", "model-selection"]
- source_urls: ["https://artificialanalysis.ai/leaderboards/models"]
- source_title: Artificial Analysis LLM Leaderboard
- source_date: live leaderboard accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Artificial Analysis LLM Leaderboard (live leaderboard accessed 2026-07-11).
Source URL(s): https://artificialanalysis.ai/leaderboards/models
Observed signal: The page compares intelligence, price, speed, latency, context window and more across 100+ models.
Existing KB snippet: 模型版图文档只想放 top 10 intelligence 排名。
User/automation request: Design model comparison update.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-022 · Arena leaderboard task tabs prevent cross-modal overclaiming · ★★
- source_type: `benchmark`
- eval_type: `fact_check`
- capability_tags: ["arena", "task-specific", "overgeneralization"]
- source_urls: ["https://arena.ai/leaderboard"]
- source_title: Arena Leaderboard
- source_date: live leaderboard accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Arena Leaderboard (live leaderboard accessed 2026-07-11).
Source URL(s): https://arena.ai/leaderboard
Observed signal: Arena has separate leaderboard contexts rather than one universal score.
Existing KB snippet: 面试弹药写了某模型是全领域第一。
User/automation request: Correct benchmark claim.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-023 · AI Index report numbers require chapter and methodology metadata · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["ai-index", "report", "methodology"]
- source_urls: ["https://arxiv.org/abs/2606.15708"]
- source_title: Artificial Intelligence Index Report 2026
- source_date: published 2026-06-18
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Artificial Intelligence Index Report 2026 (published 2026-06-18).
Source URL(s): https://arxiv.org/abs/2606.15708
Observed signal: AI Index is an annual data-driven report intended to track and visualize AI progress.
Existing KB snippet: 面试资料摘了一堆数字但没有页码/年份/口径。
User/automation request: Convert AI Index notes to PM-ready evidence cards.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-024 · Benchmark contamination survey belongs in eval methodology, not model gossip · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["benchmark-contamination", "eval-methodology", "goodhart"]
- source_urls: ["https://arxiv.org/abs/2406.04244"]
- source_title: Benchmark Data Contamination of Large Language Models: A Survey
- source_date: published 2024-06-06
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Benchmark Data Contamination of Large Language Models: A Survey (published 2024-06-06).
Source URL(s): https://arxiv.org/abs/2406.04244
Observed signal: The survey frames benchmark contamination as a systematic evaluation issue.
Existing KB snippet: 模型评测章节只有某模型疑似刷榜的八卦。
User/automation request: Update evaluation methodology section.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-025 · Multilingual benchmark contamination changes Chinese model evaluation · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["multilingual", "china-eval", "benchmark-risk"]
- source_urls: ["https://arxiv.org/abs/2410.16186"]
- source_title: Contamination Report for Multilingual Benchmarks
- source_date: published 2024-10-21
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Contamination Report for Multilingual Benchmarks (published 2024-10-21).
Source URL(s): https://arxiv.org/abs/2410.16186
Observed signal: The paper focuses on contamination risks in multilingual benchmarks.
Existing KB snippet: 中文模型评测章节拿英文榜单直接做结论。
User/automation request: Update Chinese eval plan.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-026 · Benchmark watermarking is a method note, not a PM deep dive · ★★
- source_type: `paper`
- eval_type: `route`
- capability_tags: ["watermarking", "eval-security", "depth-control"]
- source_urls: ["https://arxiv.org/abs/2502.17259"]
- source_title: Detecting Benchmark Contamination Through Watermarking
- source_date: published 2025-02-24
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Detecting Benchmark Contamination Through Watermarking (published 2025-02-24).
Source URL(s): https://arxiv.org/abs/2502.17259
Observed signal: The paper proposes watermarking as a way to detect benchmark contamination.
Existing KB snippet: Curator wants to add full technical proof into PM main docs.
User/automation request: Decide granularity.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-027 · MMLU's historical value must be separated from current limitations · ★★
- source_type: `benchmark`
- eval_type: `update`
- capability_tags: ["mmlu", "benchmark-saturation", "history"]
- source_urls: ["https://en.wikipedia.org/wiki/MMLU", "https://arxiv.org/abs/2406.04244"]
- source_title: MMLU limitations and benchmark contamination context
- source_date: live summary plus survey; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: MMLU limitations and benchmark contamination context (live summary plus survey; accessed 2026-07-11).
Source URL(s): https://en.wikipedia.org/wiki/MMLU ; https://arxiv.org/abs/2406.04244
Observed signal: MMLU is historically important but widely discussed for errors, contamination and saturation.
Existing KB snippet: 模型评测章节把 MMLU 当核心权威。
User/automation request: Reframe benchmark history.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-028 · DeepSeek R1 benchmark claims require official paper plus independent tests · ★★★★
- source_type: `paper`
- eval_type: `fact_check`
- capability_tags: ["deepseek-r1", "reasoning", "independent-validation"]
- source_urls: ["https://arxiv.org/abs/2501.12948", "https://artificialanalysis.ai/leaderboards/models"]
- source_title: DeepSeek-R1 paper and Artificial Analysis leaderboard
- source_date: paper published 2025-01-22; leaderboard live
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek-R1 paper and Artificial Analysis leaderboard (paper published 2025-01-22; leaderboard live).
Source URL(s): https://arxiv.org/abs/2501.12948 ; https://artificialanalysis.ai/leaderboards/models
Observed signal: The paper reports reasoning-model results, while leaderboards represent independent and changing measurement contexts.
Existing KB snippet: DeepSeek 研究稿直接写成超过所有闭源模型。
User/automation request: Correct claim style.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-029 · Kimi K2 agentic benchmark numbers need task relevance check · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["kimi-k2", "agent-benchmark", "ai-pm"]
- source_urls: ["https://arxiv.org/abs/2507.20534"]
- source_title: Kimi K2: Open Agentic Intelligence
- source_date: published 2025-07-28
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Kimi K2: Open Agentic Intelligence (published 2025-07-28).
Source URL(s): https://arxiv.org/abs/2507.20534
Observed signal: The paper reports agentic and coding benchmark performance such as SWE-Bench and Tau2-Bench.
Existing KB snippet: AI PM 主库想深收所有 Kimi K2 技术细节。
User/automation request: Decide which benchmark claims are useful.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-030 · Cost-performance claims must include provider, endpoint and date · ★★★★
- source_type: `paper`
- eval_type: `visualize`
- capability_tags: ["pricing", "hosted-open-weight", "provider-variance"]
- source_urls: ["https://arxiv.org/abs/2605.02821", "https://artificialanalysis.ai/leaderboards/models"]
- source_title: Hosted open-weight LLM APIs measurement study and live leaderboard
- source_date: paper published 2026-05-04; leaderboard live
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Hosted open-weight LLM APIs measurement study and live leaderboard (paper published 2026-05-04; leaderboard live).
Source URL(s): https://arxiv.org/abs/2605.02821 ; https://artificialanalysis.ai/leaderboards/models
Observed signal: A model name can map to heterogeneous hosted services with different price, latency, throughput and reliability.
Existing KB snippet: 模型选型表只有模型名，没有服务商和 endpoint。
User/automation request: Upgrade model-card schema.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 四、知识库结构与公开形态的真实标杆
### CH-031 · Lil'Log frontmatter teaches status metadata for deep notes · ★★
- source_type: `blog`
- eval_type: `refactor`
- capability_tags: ["frontmatter", "deep-note", "metadata"]
- source_urls: ["https://lilianweng.github.io/posts/2023-06-23-agent/"]
- source_title: Lil'Log: LLM Powered Autonomous Agents
- source_date: published 2023-06-23
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Lil'Log: LLM Powered Autonomous Agents (published 2023-06-23).
Source URL(s): https://lilianweng.github.io/posts/2023-06-23-agent/
Observed signal: The post exposes date, reading time, author and table of contents.
Existing KB snippet: AI 知识库文件只有编号和中文标题。
User/automation request: Design topic-note metadata.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-032 · Lil'Log agent post is historical chain, not current implementation guide · ★★★★
- source_type: `blog`
- eval_type: `route`
- capability_tags: ["agent-history", "evergreen", "evolution"]
- source_urls: ["https://lilianweng.github.io/posts/2023-06-23-agent/"]
- source_title: Lil'Log: LLM Powered Autonomous Agents
- source_date: published 2023-06-23
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lil'Log: LLM Powered Autonomous Agents (published 2023-06-23).
Source URL(s): https://lilianweng.github.io/posts/2023-06-23-agent/
Observed signal: The 2023 post covers planning, memory, tool use and early proof-of-concept agents.
Existing KB snippet: doc-06 treats 2023 AutoGPT mental model as current main agent architecture.
User/automation request: Refactor agent chapter history/current split.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-033 · Simon Willison separates entries, links, quotes, notes and guides · ★★★★
- source_type: `blog`
- eval_type: `refactor`
- capability_tags: ["three-granularity", "information-architecture", "source-chain"]
- source_urls: ["https://simonwillison.net/"]
- source_title: Simon Willison's Weblog
- source_date: live homepage accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Simon Willison's Weblog (live homepage accessed 2026-07-11).
Source URL(s): https://simonwillison.net/
Observed signal: The site separates content types such as Entries, Links, Quotes, Notes and Guides.
Existing KB snippet: Curator writes every source as the same length Markdown block.
User/automation request: Design collection granularity.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-034 · Simon source-chain practice prevents二手来源失真 · ★★★★
- source_type: `blog`
- eval_type: `fact_check`
- capability_tags: ["source-chain", "via", "attribution"]
- source_urls: ["https://simonwillison.net/"]
- source_title: Simon Willison's Weblog
- source_date: live homepage accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Simon Willison's Weblog (live homepage accessed 2026-07-11).
Source URL(s): https://simonwillison.net/
Observed signal: The homepage often preserves original links and via/discovery paths.
Existing KB snippet: source log stores only the page where Curator found the item.
User/automation request: Update source metadata.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-035 · Chip Huyen pairs writing with tools and repos · ★★
- source_type: `blog`
- eval_type: `refactor`
- capability_tags: ["blog-repo-link", "production-ai", "assets"]
- source_urls: ["https://huyenchip.com/"]
- source_title: Chip Huyen homepage
- source_date: live homepage accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Chip Huyen homepage (live homepage accessed 2026-07-11).
Source URL(s): https://huyenchip.com/
Observed signal: The site presents essays, books, public tools and GitHub-adjacent resources.
Existing KB snippet: KB-Agent prompt samples and scripts are embedded inside long docs.
User/automation request: Design blog/repo separation.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-036 · Andy Matuschak notes suggest evergreen graph but not raw public dump · ★★★★
- source_type: `blog`
- eval_type: `refactor`
- capability_tags: ["evergreen-notes", "public-private", "digital-garden"]
- source_urls: ["https://notes.andymatuschak.org/"]
- source_title: Andy Matuschak notes
- source_date: live site accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Andy Matuschak notes (live site accessed 2026-07-11).
Source URL(s): https://notes.andymatuschak.org/
Observed signal: The notes are public, browseable and interconnected evergreen notes.
Existing KB snippet: 用户想以后公开知识库，但库里有私密简历和版权材料。
User/automation request: Design public/private split.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-037 · WaytoAGI portal structure is useful for entry points but not personal depth · ★★
- source_type: `chinese_ecosystem`
- eval_type: `refactor`
- capability_tags: ["chinese-community", "portal", "navigation"]
- source_urls: ["https://www.waytoagi.com/zh"]
- source_title: WaytoAGI Chinese AI knowledge portal
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: WaytoAGI Chinese AI knowledge portal (live page accessed 2026-07-11).
Source URL(s): https://www.waytoagi.com/zh
Observed signal: The site organizes tools, agents, prompts, activities and selected knowledge resources.
Existing KB snippet: 当前 AI 知识库只有技术主题目录。
User/automation request: Decide navigation design.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-038 · 拾象 uses thesis-driven structure for company and sector research · ★★★★
- source_type: `chinese_ecosystem`
- eval_type: `synthesize`
- capability_tags: ["thesis", "company-dossier", "china-ai"]
- source_urls: ["https://shixiang.com/"]
- source_title: 拾象科技 homepage
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: 拾象科技 homepage (live page accessed 2026-07-11).
Source URL(s): https://shixiang.com/
Observed signal: The site organizes AGI/Robotics/AI for Science/Agent-Native content around theses.
Existing KB snippet: 目标公司板块现在按新闻时间堆动态。
User/automation request: Refactor target company research.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-039 · a16z AI Canon is canonical but dated and investor-positioned · ★★★★
- source_type: `blog`
- eval_type: `fact_check`
- capability_tags: ["canon", "date-awareness", "vc-bias"]
- source_urls: ["https://a16z.com/ai-canon/"]
- source_title: a16z AI Canon
- source_date: published 2023-05-25; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: a16z AI Canon (published 2023-05-25; accessed 2026-07-11).
Source URL(s): https://a16z.com/ai-canon/
Observed signal: The canon is a curated reading list from a VC firm and includes publication context/disclaimer.
Existing KB snippet: 入门资源章节想把 AI Canon 当最新学习路线。
User/automation request: Decide how to use canonical reading lists.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-040 · Obsidian-friendly KB needs stable IDs, not only readable titles · ★★★★
- source_type: `user_project`
- eval_type: `refactor`
- capability_tags: ["obsidian", "stable-id", "link-health"]
- source_urls: ["file://~/Documents/AI知识库 V3/"]
- source_title: User AI知识库 V3 local vault
- source_date: local project inspected 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: User AI知识库 V3 local vault (local project inspected 2026-07-11).
Source URL(s): file://~/Documents/AI知识库 V3/
Observed signal: Existing docs were renamed and indexed; link stability is now a maintenance concern.
Existing KB snippet: 索引和文件名曾经出现 doc-01 与中文名漂移。
User/automation request: Design durable note IDs.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 五、高频动态管线如何不污染长期库
### CH-041 · AINews high-frequency source needs discovery log before main KB write · ★★★★
- source_type: `newsletter`
- eval_type: `triage`
- capability_tags: ["daily-news", "source-log", "triage"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews homepage
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews homepage (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: The homepage says it summarizes AI communities every weekday and lists daily issues with many tags.
Existing KB snippet: 自动更新计划想每天把早报直接写进知识库。
User/automation request: Define daily ingestion pipeline.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-042 · AINews item mixes cost warning, benchmark and product launch in one day · ★★★★
- source_type: `newsletter`
- eval_type: `synthesize`
- capability_tags: ["trend-clustering", "cost", "agent-ops"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews recent issues
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews recent issues (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: Recent issue summaries combine model launches, cost, UX, benchmark and community reactions.
Existing KB snippet: Curator wants one flat daily note.
User/automation request: Create clustered digest.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-043 · Newsletter rumor cycles must be separated from official releases · ★★★★
- source_type: `newsletter`
- eval_type: `fact_check`
- capability_tags: ["rumor", "official-release", "source-weight"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews recent issues
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews recent issues (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: Recent issues include language about rumor cycles and official launches in adjacent summaries.
Existing KB snippet: 模型发布文档把社区传闻和正式发布合并成一句。
User/automation request: Correct release note policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-044 · Community user reports need lower evidence weight than official docs · ★★
- source_type: `newsletter`
- eval_type: `triage`
- capability_tags: ["user-report", "evidence-weight", "model-quality"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews recent issues
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: AINews recent issues (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: Daily summaries include user testing, community benchmark discussion and official announcements together.
Existing KB snippet: 模型能力更新想直接引用用户评价。
User/automation request: Design source weight field.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-045 · The title 'not much happened today' is not a value signal · ★★
- source_type: `newsletter`
- eval_type: `triage`
- capability_tags: ["headline-bias", "content-analysis", "daily-digest"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews issues with recurring low-key titles
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: AINews issues with recurring low-key titles (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: Some daily issues have casual titles while still containing dense technical and product signals.
Existing KB snippet: 自动筛选规则打算按标题关键词判断价值。
User/automation request: Improve daily triage scoring.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-046 · AI News source handles are flywheel data, not decoration · ★★
- source_type: `newsletter`
- eval_type: `flywheel`
- capability_tags: ["source-graph", "handles", "attribution"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews homepage metadata
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: AINews homepage metadata (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: Issues list tags and source handles alongside summaries.
Existing KB snippet: source log currently drops tags and handles after summarizing.
User/automation request: Update metadata retention.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-047 · Daily source should trigger weekly trend review, not only daily notes · ★★★★
- source_type: `newsletter`
- eval_type: `workflow`
- capability_tags: ["weekly-review", "trend", "scheduler"]
- source_urls: ["https://news.smol.ai/", "https://arxiv.org/abs/2606.15708"]
- source_title: AINews daily cadence and AI Index annual cadence
- source_date: live/dynamic sources accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews daily cadence and AI Index annual cadence (live/dynamic sources accessed 2026-07-11).
Source URL(s): https://news.smol.ai/ ; https://arxiv.org/abs/2606.15708
Observed signal: Daily newsletters and annual reports have very different update rhythms.
Existing KB snippet: 更新任务没有按源类型设置频率。
User/automation request: Design scheduler policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-048 · High-volume feed requires reject reasons to avoid silent drift · ★★★★
- source_type: `newsletter`
- eval_type: `flywheel`
- capability_tags: ["reject-reason", "source-quality", "observability"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews high-frequency feed
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews high-frequency feed (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: A daily feed can generate many low-priority candidates.
Existing KB snippet: visualizer 只统计新增条目。
User/automation request: Design rejection observability.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 六、版权、隐私、安全与公开发布风险
### CH-049 · Public KB release needs full-repo secret scanning · ★★★★★
- source_type: `github_issue`
- eval_type: `security`
- capability_tags: ["secret-scan", "public-release", "repo-history"]
- source_urls: ["https://github.com/huggingface/blog/issues/3364"]
- source_title: Hugging Face blog issue #3364 exposed API key
- source_date: created 2026-04-24; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: Hugging Face blog issue #3364 exposed API key (created 2026-04-24; accessed 2026-07-11).
Source URL(s): https://github.com/huggingface/blog/issues/3364
Observed signal: The issue recommends revoke/rotate, billing check, env vars and prevention tools.
Existing KB snippet: 公开化 checklist 只看正文里有没有手机号。
User/automation request: Upgrade public-release gate.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-050 · Quoted passages need attribution and length policy · ★★
- source_type: `blog`
- eval_type: `route`
- capability_tags: ["copyright", "quotation", "attribution"]
- source_urls: ["https://simonwillison.net/"]
- source_title: Simon Willison quote/link practices
- source_date: live homepage accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Simon Willison quote/link practices (live homepage accessed 2026-07-11).
Source URL(s): https://simonwillison.net/
Observed signal: The site attributes quotes to original authors and links sources.
Existing KB snippet: 知识库摘录外部观点时只写观点，不写作者和链接。
User/automation request: Define quotation note policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-051 · a16z disclaimer reminds that third-party info may be unverified · ★★★★
- source_type: `blog`
- eval_type: `fact_check`
- capability_tags: ["vc-content", "disclaimer", "bias"]
- source_urls: ["https://a16z.com/ai-canon/"]
- source_title: a16z AI Canon and disclaimer context
- source_date: published 2023-05-25; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: a16z AI Canon and disclaimer context (published 2023-05-25; accessed 2026-07-11).
Source URL(s): https://a16z.com/ai-canon/
Observed signal: The canon is curated by a VC and includes third-party information context.
Existing KB snippet: 赛道判断直接引用 VC 文章作为事实。
User/automation request: Set VC/investor content policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-052 · Lenny's PM content may be high value but paywalled · ★★★★
- source_type: `blog`
- eval_type: `route`
- capability_tags: ["paywall", "pm-learning", "copyright"]
- source_urls: ["https://www.lennysnewsletter.com/"]
- source_title: Lenny's Newsletter
- source_date: live homepage accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lenny's Newsletter (live homepage accessed 2026-07-11).
Source URL(s): https://www.lennysnewsletter.com/
Observed signal: Lenny's is a PM-focused newsletter with public and subscriber content.
Existing KB snippet: 用户想把面试相关访谈全文加入知识库。
User/automation request: Handle PM source legally.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-053 · OpenAI docs product surfaces must not be mixed · ★★★★
- source_type: `official_doc`
- eval_type: `fact_check`
- capability_tags: ["product-surface", "api-vs-chatgpt", "doc-routing"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations", "https://developers.openai.com/api/docs/models"]
- source_title: OpenAI developer docs navigation
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI developer docs navigation (live pages accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/deprecations ; https://developers.openai.com/api/docs/models
Observed signal: OpenAI docs navigation includes API, Codex, ChatGPT, Apps SDK and other surfaces.
Existing KB snippet: 一段笔记把 ChatGPT Work、Codex、API model availability 混在一起。
User/automation request: Correct product-surface routing.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-054 · Claude Platform release notes differ from Claude consumer app notes · ★★
- source_type: `release_note`
- eval_type: `fact_check`
- capability_tags: ["platform-vs-app", "claude", "source-routing"]
- source_urls: ["https://platform.claude.com/docs/en/release-notes/overview"]
- source_title: Claude Platform release notes
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Claude Platform release notes (live page accessed 2026-07-11).
Source URL(s): https://platform.claude.com/docs/en/release-notes/overview
Observed signal: The page is for Platform/API changes and links to other product release areas.
Existing KB snippet: Claude App 使用体验变化被写成 API 行为。
User/automation request: Separate Anthropic source surfaces.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-055 · User resume and job materials require private-zone handling · ★★★★★
- source_type: `user_project`
- eval_type: `security`
- capability_tags: ["privacy", "resume", "personal-data"]
- source_urls: ["file://~/Desktop/个人信息/复旦大学-冯子函-广告学-秋招简历.pdf"]
- source_title: User resume PDF
- source_date: local private file referenced 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `real_wrapped`
- split: `regression`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: User resume PDF (local private file referenced 2026-07-11).
Source URL(s): file://~/Desktop/个人信息/复旦大学-冯子函-广告学-秋招简历.pdf
Observed signal: The project uses the user's resume to align the KB-Agent with career goals.
Existing KB snippet: 公开化方案没有把简历和个人信息隔离。
User/automation request: Define privacy zoning.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-056 · Generated images/videos in KB need source and rights metadata · ★★★★
- source_type: `official_doc`
- eval_type: `route`
- capability_tags: ["multimodal", "asset-rights", "public-kb"]
- source_urls: ["https://developers.openai.com/api/docs/pricing", "https://docs.volcengine.com/docs/82379/1330310?lang=zh"]
- source_title: OpenAI pricing and VolcEngine Ark model list
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI pricing and VolcEngine Ark model list (live pages accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/pricing ; https://docs.volcengine.com/docs/82379/1330310?lang=zh
Observed signal: Modern AI platforms expose image/video generation and related billing/product surfaces.
Existing KB snippet: 知识库准备引入图片和视频素材，但没有资产来源表。
User/automation request: Design media asset policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 七、面向中国头部 AI 公司 AI PM 求职
### CH-057 · DeepSeek pricing page is PM cost evidence, not just developer docs · ★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["deepseek", "cost", "ai-pm"]
- source_urls: ["https://api-docs.deepseek.com/quick_start/pricing/"]
- source_title: DeepSeek Models & Pricing
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek Models & Pricing (live page accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/quick_start/pricing/
Observed signal: DeepSeek lists v4 flash/pro models, cache-hit/cache-miss pricing, output pricing, concurrency and deprecation notes.
Existing KB snippet: DeepSeek 章节只讲 R1 技术故事。
User/automation request: Add PM-ready cost and product positioning card.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-058 · DeepSeek OpenAI/Anthropic compatibility is ecosystem strategy signal · ★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["deepseek", "api-compatibility", "ecosystem"]
- source_urls: ["https://api-docs.deepseek.com/"]
- source_title: DeepSeek API quick start
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek API quick start (live page accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/
Observed signal: The docs say DeepSeek API uses OpenAI/Anthropic-compatible formats and supports agent tools.
Existing KB snippet: 目标公司研究只按模型能力写。
User/automation request: Extract ecosystem/product strategy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-059 · DeepSeek R1 paper should become interview narrative about RL reasoning · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["deepseek-r1", "reasoning", "interview"]
- source_urls: ["https://arxiv.org/abs/2501.12948"]
- source_title: DeepSeek-R1 paper
- source_date: published 2025-01-22
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek-R1 paper (published 2025-01-22).
Source URL(s): https://arxiv.org/abs/2501.12948
Observed signal: The paper introduces R1-Zero/R1, large-scale RL, cold-start data and distilled models.
Existing KB snippet: 后训练文档有大量算法术语，但没有面试表达。
User/automation request: Convert to AI PM explanation.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-060 · DeepSeek V2 cost-efficiency claims should map to product economics · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["deepseek-v2", "moe", "product-economics"]
- source_urls: ["https://arxiv.org/abs/2405.04434"]
- source_title: DeepSeek-V2 paper
- source_date: published 2024-05-07
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek-V2 paper (published 2024-05-07).
Source URL(s): https://arxiv.org/abs/2405.04434
Observed signal: The paper discusses MoE, MLA, KV cache reduction and lower training/inference costs.
Existing KB snippet: 模型架构章节只讲 MLA/MoE 原理。
User/automation request: Write PM-facing product economics note.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-061 · Alibaba Model Studio page shows platform bundling across modalities · ★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["alibaba", "model-studio", "platform"]
- source_urls: ["https://help.aliyun.com/zh/model-studio/models"]
- source_title: Alibaba Cloud Model Studio model list
- source_date: last viewed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Alibaba Cloud Model Studio model list (last viewed 2026-07-11).
Source URL(s): https://help.aliyun.com/zh/model-studio/models
Observed signal: The page organizes Qwen and third-party models across text, vision, video, audio, embedding and reranking.
Existing KB snippet: 阿里章节只有通义千问模型介绍。
User/automation request: Build Alibaba AI platform dossier.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-062 · VolcEngine Ark docs reveal ByteDance enterprise AI platform surface · ★★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["bytedance", "volcengine", "ark"]
- source_urls: ["https://docs.volcengine.com/docs/82379/1330310?lang=zh"]
- source_title: VolcEngine Ark model list and docs navigation
- source_date: last updated 2026-07-08; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: VolcEngine Ark model list and docs navigation (last updated 2026-07-08; accessed 2026-07-11).
Source URL(s): https://docs.volcengine.com/docs/82379/1330310?lang=zh
Observed signal: The docs expose model list, pricing, tool calling, knowledge base, Managed Agents, model eval and prompt tools.
Existing KB snippet: 字节章节只写豆包 C 端 app。
User/automation request: Expand ByteDance AI PM research.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-063 · StepFun model overview tests target-company model portfolio reading · ★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["stepfun", "model-portfolio", "target-company"]
- source_urls: ["https://platform.stepfun.com/docs/llm/modeloverview"]
- source_title: StepFun model capability overview
- source_date: last updated 2026-03-23; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: StepFun model capability overview (last updated 2026-03-23; accessed 2026-07-11).
Source URL(s): https://platform.stepfun.com/docs/llm/modeloverview
Observed signal: StepFun docs list step-3.5-flash, step-3, step-2-mini and multimodal/audio models with context and feature tags.
Existing KB snippet: 阶跃章节只有公司融资和创始人背景。
User/automation request: Build StepFun model/product dossier.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-064 · Artificial Analysis gives independent view of Chinese models · ★★★★
- source_type: `benchmark`
- eval_type: `fact_check`
- capability_tags: ["china-models", "independent-benchmark", "model-selection"]
- source_urls: ["https://artificialanalysis.ai/leaderboards/models"]
- source_title: Artificial Analysis leaderboard
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Artificial Analysis leaderboard (live page accessed 2026-07-11).
Source URL(s): https://artificialanalysis.ai/leaderboards/models
Observed signal: The leaderboard includes models from DeepSeek, Alibaba/Qwen, Kimi and other providers alongside global frontier models.
Existing KB snippet: 国内模型判断主要引用厂商新闻稿。
User/automation request: Add independent benchmark cross-check.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-065 · Kimi K2 paper is a China open-agent signal for PM strategy · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["kimi", "open-agent", "china-ai"]
- source_urls: ["https://arxiv.org/abs/2507.20534"]
- source_title: Kimi K2: Open Agentic Intelligence
- source_date: published 2025-07-28
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Kimi K2: Open Agentic Intelligence (published 2025-07-28).
Source URL(s): https://arxiv.org/abs/2507.20534
Observed signal: The paper positions K2 around MoE, agentic data synthesis and open agentic capabilities.
Existing KB snippet: 国内模型版图没有 Kimi/Moonshot 的 agentic 视角。
User/automation request: Add China model strategy note.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-066 · WaytoAGI tool portal can support portfolio building but needs filtering · ★★
- source_type: `chinese_ecosystem`
- eval_type: `route`
- capability_tags: ["waytoagi", "tools", "portfolio"]
- source_urls: ["https://www.waytoagi.com/zh"]
- source_title: WaytoAGI Chinese AI portal
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: WaytoAGI Chinese AI portal (live page accessed 2026-07-11).
Source URL(s): https://www.waytoagi.com/zh
Observed signal: The portal includes tool, prompt, agent and activity entries.
Existing KB snippet: 用户想快速做作品集，考虑全量跟踪工具。
User/automation request: Create tool selection policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-067 · 拾象 thesis helps turn company news into structured judgment · ★★★★
- source_type: `chinese_ecosystem`
- eval_type: `synthesize`
- capability_tags: ["shixiang", "thesis", "company-research"]
- source_urls: ["https://shixiang.com/"]
- source_title: 拾象科技 thesis-oriented homepage
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: 拾象科技 thesis-oriented homepage (live page accessed 2026-07-11).
Source URL(s): https://shixiang.com/
Observed signal: The site presents AI/AGI topics through investment and technology theses.
Existing KB snippet: 公司研究文档按新闻时间线排列，缺观点。
User/automation request: Refactor company research template.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-068 · Lenny's Newsletter is PM gold but cannot be scraped blindly · ★★★★
- source_type: `blog`
- eval_type: `route`
- capability_tags: ["pm", "paywall", "takeaway"]
- source_urls: ["https://www.lennysnewsletter.com/"]
- source_title: Lenny's Newsletter
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lenny's Newsletter (live page accessed 2026-07-11).
Source URL(s): https://www.lennysnewsletter.com/
Observed signal: PM-focused newsletter with public and subscriber material.
Existing KB snippet: 用户希望用 Lenny 的访谈补 PM 能力。
User/automation request: Build PM learning ingestion policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-069 · Chip Huyen production AI material fills文科 PM engineering gap · ★★
- source_type: `blog`
- eval_type: `synthesize`
- capability_tags: ["production-ai", "engineering-for-pm", "chip-huyen"]
- source_urls: ["https://huyenchip.com/"]
- source_title: Chip Huyen homepage
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: Chip Huyen homepage (live page accessed 2026-07-11).
Source URL(s): https://huyenchip.com/
Observed signal: Chip's work emphasizes AI engineering, production systems, evaluation and practical ML/AI systems.
Existing KB snippet: 用户担心广告学背景与 AI PM 技术要求有差距。
User/automation request: Route engineering content for PM learning.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-070 · VolcEngine Managed Agents docs connect directly to KB-Agent product vision · ★★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["managed-agents", "bytedance", "agent-product"]
- source_urls: ["https://docs.volcengine.com/docs/82379/1330310?lang=zh"]
- source_title: VolcEngine Ark Managed Agents navigation
- source_date: last updated 2026-07-08; accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: VolcEngine Ark Managed Agents navigation (last updated 2026-07-08; accessed 2026-07-11).
Source URL(s): https://docs.volcengine.com/docs/82379/1330310?lang=zh
Observed signal: Ark docs include Managed Agents, sessions, skills, MCP, tools, permissions, cloud environment and memory-like management surfaces.
Existing KB snippet: KB-Agent 设计没有对标国内平台 agent 产品。
User/automation request: Extract product requirements comparison.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-071 · 阿里 Model Studio third-party model aggregation is platform strategy evidence · ★★★★
- source_type: `official_doc`
- eval_type: `synthesize`
- capability_tags: ["alibaba", "third-party-models", "platform-strategy"]
- source_urls: ["https://help.aliyun.com/zh/model-studio/models"]
- source_title: Alibaba Model Studio model list
- source_date: accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Alibaba Model Studio model list (accessed 2026-07-11).
Source URL(s): https://help.aliyun.com/zh/model-studio/models
Observed signal: The page lists Qwen plus third-party models such as DeepSeek/Kimi/GLM/MiniMax in one platform.
Existing KB snippet: 阿里研究只比较 Qwen vs 其他模型。
User/automation request: Update platform strategy note.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 八、理论演化：历史链条与最新版策略
### CH-072 · CoT evolved from prompt trick to test-time compute and reasoning models · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["cot", "reasoning", "evolution"]
- source_urls: ["https://lilianweng.github.io/posts/2023-06-23-agent/", "https://arxiv.org/abs/2501.12948"]
- source_title: Lil'Log agent post and DeepSeek-R1 paper
- source_date: 2023-06-23 and 2025-01-22
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lil'Log agent post and DeepSeek-R1 paper (2023-06-23 and 2025-01-22).
Source URL(s): https://lilianweng.github.io/posts/2023-06-23-agent/ ; https://arxiv.org/abs/2501.12948
Observed signal: Older agent literature discusses CoT/ToT; DeepSeek-R1 frames reasoning through RL and inference-time reasoning behavior.
Existing KB snippet: CoT 笔记只有让模型一步步想。
User/automation request: Refactor CoT evolution note.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-073 · Agent concept evolved from AutoGPT demos to harnessed workflows · ★★★★
- source_type: `blog`
- eval_type: `synthesize`
- capability_tags: ["agent", "harness", "history"]
- source_urls: ["https://lilianweng.github.io/posts/2023-06-23-agent/", "https://simonwillison.net/"]
- source_title: Lil'Log agent post and Simon Willison agentic engineering notes
- source_date: 2023 post plus live 2026 blog
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lil'Log agent post and Simon Willison agentic engineering notes (2023 post plus live 2026 blog).
Source URL(s): https://lilianweng.github.io/posts/2023-06-23-agent/ ; https://simonwillison.net/
Observed signal: Early agent posts emphasize planning/memory/tool use; current discourse emphasizes harnesses, tests, workflows and review.
Existing KB snippet: doc-06 still centers AutoGPT-like loops.
User/automation request: Update agent mental model.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-074 · Reward hacking belongs in eval/product risk, not only RL theory · ★★★★
- source_type: `blog`
- eval_type: `route`
- capability_tags: ["reward-hacking", "eval", "product-risk"]
- source_urls: ["https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"]
- source_title: Lil'Log: Reward Hacking in Reinforcement Learning
- source_date: published 2024-11-28
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lil'Log: Reward Hacking in Reinforcement Learning (published 2024-11-28).
Source URL(s): https://lilianweng.github.io/posts/2024-11-28-reward-hacking/
Observed signal: The post surveys reward hacking and unintended optimization behavior.
Existing KB snippet: 后训练文档想深收 reward hacking，但产品风险章节没有链接。
User/automation request: Route concept across docs.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-075 · RAG and memory need theory/API split · ★★★★
- source_type: `release_note`
- eval_type: `update`
- capability_tags: ["rag", "memory", "api-change"]
- source_urls: ["https://platform.claude.com/docs/en/release-notes/overview"]
- source_title: Claude Platform release notes
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Claude Platform release notes (live page accessed 2026-07-11).
Source URL(s): https://platform.claude.com/docs/en/release-notes/overview
Observed signal: Release notes include memory/tool behavior and model-specific changes over time.
Existing KB snippet: Memory/RAG 章节混合抽象概念和具体 API 参数。
User/automation request: Refactor memory docs.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-076 · Post-training note should connect SFT/RL to product behavior · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["post-training", "rl", "product-behavior"]
- source_urls: ["https://arxiv.org/abs/2501.12948", "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"]
- source_title: DeepSeek-R1 and Reward Hacking references
- source_date: 2025-01-22 and 2024-11-28
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: DeepSeek-R1 and Reward Hacking references (2025-01-22 and 2024-11-28).
Source URL(s): https://arxiv.org/abs/2501.12948 ; https://lilianweng.github.io/posts/2024-11-28-reward-hacking/
Observed signal: R1 discusses multi-stage training and RL; reward hacking literature discusses unintended optimization.
Existing KB snippet: doc-08 后训练 RL 只写算法名词。
User/automation request: Make post-training AI PM readable.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-077 · Context window numbers should be latest-only in main path · ★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["context-window", "latest-only", "model-card"]
- source_urls: ["https://api-docs.deepseek.com/quick_start/pricing/", "https://platform.stepfun.com/docs/llm/modeloverview"]
- source_title: DeepSeek and StepFun model docs
- source_date: live docs accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=3, source_conflict=2, structural_impact=2, risk_level=2, autonomy_required=3

#### Actor Input
Input source snapshot: DeepSeek and StepFun model docs (live docs accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/quick_start/pricing/ ; https://platform.stepfun.com/docs/llm/modeloverview
Observed signal: Provider docs list current context lengths and model variants.
Existing KB snippet: 模型表保留多个旧上下文窗口数字。
User/automation request: Decide history vs current.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-078 · Function/tool calling theory must track provider-specific behavior · ★★★★
- source_type: `official_doc`
- eval_type: `update`
- capability_tags: ["tool-calling", "provider-diff", "api"]
- source_urls: ["https://docs.volcengine.com/docs/82379/1330310?lang=zh", "https://platform.stepfun.com/docs/llm/modeloverview", "https://developers.openai.com/api/docs/models"]
- source_title: OpenAI, VolcEngine and StepFun docs
- source_date: live docs accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI, VolcEngine and StepFun docs (live docs accessed 2026-07-11).
Source URL(s): https://docs.volcengine.com/docs/82379/1330310?lang=zh ; https://platform.stepfun.com/docs/llm/modeloverview ; https://developers.openai.com/api/docs/models
Observed signal: Different providers expose tool calling, search, JSON mode and agent features differently.
Existing KB snippet: 工具调用章节把 function calling 当统一能力。
User/automation request: Update tool-calling schema.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-079 · Open-source model strategy needs evolution chain from weights to services · ★★★★
- source_type: `paper`
- eval_type: `synthesize`
- capability_tags: ["open-weight", "hosted-service", "strategy"]
- source_urls: ["https://arxiv.org/abs/2605.02821", "https://arxiv.org/abs/2507.20534"]
- source_title: Hosted open-weight APIs study and Kimi K2 paper
- source_date: 2026-05-04 and 2025-07-28
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Hosted open-weight APIs study and Kimi K2 paper (2026-05-04 and 2025-07-28).
Source URL(s): https://arxiv.org/abs/2605.02821 ; https://arxiv.org/abs/2507.20534
Observed signal: One paper argues hosted open-weight APIs behave like time-varying services; Kimi K2 presents an open agentic model.
Existing KB snippet: 开源模型章节只按权重是否开放分类。
User/automation request: Update open model strategy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 九、图表、dashboard、visualizer 与可观测性
### CH-080 · Visualizer must show source funnel, not just new note count · ★★★★
- source_type: `benchmark`
- eval_type: `visualize`
- capability_tags: ["visualizer", "source-funnel", "observability"]
- source_urls: ["https://arxiv.org/abs/2606.15708", "https://news.smol.ai/"]
- source_title: AI Index and AINews
- source_date: annual report plus live daily feed
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AI Index and AINews (annual report plus live daily feed).
Source URL(s): https://arxiv.org/abs/2606.15708 ; https://news.smol.ai/
Observed signal: AI Index emphasizes tracking/visualizing AI data; AINews shows high-volume daily input.
Existing KB snippet: visualizer 草图只有新增条目数。
User/automation request: Design dashboard metrics.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-081 · Model comparison chart needs multi-axis and unit guardrails · ★★★★
- source_type: `benchmark`
- eval_type: `visualize`
- capability_tags: ["model-comparison", "chart", "unit"]
- source_urls: ["https://artificialanalysis.ai/leaderboards/models", "https://developers.openai.com/api/docs/pricing"]
- source_title: Artificial Analysis and OpenAI pricing
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Artificial Analysis and OpenAI pricing (live pages accessed 2026-07-11).
Source URL(s): https://artificialanalysis.ai/leaderboards/models ; https://developers.openai.com/api/docs/pricing
Observed signal: Leaderboard metrics and provider pricing have different units and update cadences.
Existing KB snippet: 想画一个总分榜单图。
User/automation request: Design model visualizer panel.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-082 · Visualizer should expose freshness debt and deprecation risk · ★★★★
- source_type: `official_doc`
- eval_type: `visualize`
- capability_tags: ["freshness", "deprecation", "risk"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations", "https://api-docs.deepseek.com/quick_start/pricing/"]
- source_title: OpenAI and DeepSeek deprecation docs
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: OpenAI and DeepSeek deprecation docs (live pages accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/deprecations ; https://api-docs.deepseek.com/quick_start/pricing/
Observed signal: Provider docs include dated deprecations and upcoming alias removals.
Existing KB snippet: 诊断报告只说近期更新了什么。
User/automation request: Add risk timeline.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-083 · Visualizer should show target-company coverage for AI PM prep · ★★★★★
- source_type: `chinese_ecosystem`
- eval_type: `visualize`
- capability_tags: ["target-company", "coverage", "ai-pm"]
- source_urls: ["https://api-docs.deepseek.com/", "https://help.aliyun.com/zh/model-studio/models", "https://docs.volcengine.com/docs/82379/1330310?lang=zh", "https://platform.stepfun.com/docs/llm/modeloverview"]
- source_title: DeepSeek, Alibaba, VolcEngine and StepFun docs
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: DeepSeek, Alibaba, VolcEngine and StepFun docs (live pages accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/ ; https://help.aliyun.com/zh/model-studio/models ; https://docs.volcengine.com/docs/82379/1330310?lang=zh ; https://platform.stepfun.com/docs/llm/modeloverview
Observed signal: Target-company source coverage differs across docs and platforms.
Existing KB snippet: 知识库看起来很技术，但不知道对秋招目标覆盖多少。
User/automation request: Create AI PM prep dashboard.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-084 · Rejected-source dashboard is required for source quality flywheel · ★★★★
- source_type: `newsletter`
- eval_type: `visualize`
- capability_tags: ["reject-dashboard", "flywheel", "quality"]
- source_urls: ["https://news.smol.ai/", "https://github.com/Hannibal046/Awesome-LLM/issues"]
- source_title: AINews and Awesome-LLM issue feed
- source_date: live sources accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews and Awesome-LLM issue feed (live sources accessed 2026-07-11).
Source URL(s): https://news.smol.ai/ ; https://github.com/Hannibal046/Awesome-LLM/issues
Observed signal: High-volume sources produce many candidates of uneven quality.
Existing KB snippet: 只记录采纳内容，不记录拒绝。
User/automation request: Design reject analytics.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-085 · Visualizer should support drill-down from chart to changelog diff · ★★★★
- source_type: `user_project`
- eval_type: `visualize`
- capability_tags: ["changelog", "diff", "drilldown"]
- source_urls: ["file://~/Documents/KB-Agent/evals/02-challenge-dataset-v0.3.md"]
- source_title: KB-Agent eval files
- source_date: local project 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: KB-Agent eval files (local project 2026-07-11).
Source URL(s): file://~/Documents/KB-Agent/evals/02-challenge-dataset-v0.3.md
Observed signal: v0.3 changed the dataset but needs traceable iteration history.
Existing KB snippet: dashboard 只显示今日做了更新。
User/automation request: Design drill-down interaction.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-086 · Visual QA is needed for technical diagrams · ★★★★
- source_type: `github_issue`
- eval_type: `visualize`
- capability_tags: ["diagram-qa", "visual-accuracy", "technical-illustration"]
- source_urls: ["https://github.com/huggingface/blog/issues/3119"]
- source_title: Hugging Face blog issue #3119
- source_date: created 2025-10-07
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Hugging Face blog issue #3119 (created 2025-10-07).
Source URL(s): https://github.com/huggingface/blog/issues/3119
Observed signal: A technical visual was challenged as misleading.
Existing KB snippet: 知识库可视化计划优先美观。
User/automation request: Add visual QA checklist.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-087 · Dashboard should distinguish source cadence and KB cadence · ★★★★
- source_type: `newsletter`
- eval_type: `visualize`
- capability_tags: ["cadence", "scheduler", "dashboard"]
- source_urls: ["https://news.smol.ai/", "https://arxiv.org/abs/2606.15708"]
- source_title: AINews and AI Index
- source_date: live daily source and annual report
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews and AI Index (live daily source and annual report).
Source URL(s): https://news.smol.ai/ ; https://arxiv.org/abs/2606.15708
Observed signal: One source updates every weekday; another is annual and report-like.
Existing KB snippet: 自动更新计划没有 source cadence 字段。
User/automation request: Add cadence visualization.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 十、自动化、人类把关、回滚与数据飞轮
### CH-088 · Automatic writes need risk tiers and human gates · ★★★★★
- source_type: `newsletter`
- eval_type: `workflow`
- capability_tags: ["human-in-loop", "risk-tier", "automation"]
- source_urls: ["https://news.smol.ai/", "https://github.com/openai/openai-cookbook/issues/2834"]
- source_title: AINews and OpenAI Cookbook issue #2834
- source_date: live/issue sources accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `smoke`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: AINews and OpenAI Cookbook issue #2834 (live/issue sources accessed 2026-07-11).
Source URL(s): https://news.smol.ai/ ; https://github.com/openai/openai-cookbook/issues/2834
Observed signal: Feeds and issues can produce candidates with different risk levels.
Existing KB snippet: agent 目标是自动运行直到叫停。
User/automation request: Define autonomy policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-089 · Every update run should produce changelog, diff and rollback anchor · ★★★★★
- source_type: `user_project`
- eval_type: `workflow`
- capability_tags: ["changelog", "rollback", "git"]
- source_urls: ["file://~/Documents/KB-Agent/DECISIONS.md"]
- source_title: KB-Agent decision log and git workflow
- source_date: local project 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `full`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: KB-Agent decision log and git workflow (local project 2026-07-11).
Source URL(s): file://~/Documents/KB-Agent/DECISIONS.md
Observed signal: The project already uses commits and decision logs for major dataset changes.
Existing KB snippet: 维护状态靠对话记忆。
User/automation request: Define run artifact output.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-090 · User override is highest-value flywheel data · ★★★★★
- source_type: `user_project`
- eval_type: `flywheel`
- capability_tags: ["user-override", "preference-learning", "judge-calibration"]
- source_urls: ["file://~/Documents/KB-Agent/evals/03-rubric-v0.1.md"]
- source_title: KB-Agent rubric v0.1 Judge protocol
- source_date: local project 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `full`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: KB-Agent rubric v0.1 Judge protocol (local project 2026-07-11).
Source URL(s): file://~/Documents/KB-Agent/evals/03-rubric-v0.1.md
Observed signal: Rubric says human score overrides should drive rubric or judge revision.
Existing KB snippet: 用户指出 v0.3 不够真实来源，但数据集没有把这个当回归样本。
User/automation request: Record user feedback as regression.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-091 · Prompt/SOP/tool/data-source root cause must be classified · ★★★★
- source_type: `user_project`
- eval_type: `flywheel`
- capability_tags: ["root-cause", "sop", "prompt-design"]
- source_urls: ["file://~/Documents/KB-Agent/evals/03-rubric-v0.1.md"]
- source_title: KB-Agent eval loop
- source_date: local project 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: KB-Agent eval loop (local project 2026-07-11).
Source URL(s): file://~/Documents/KB-Agent/evals/03-rubric-v0.1.md
Observed signal: The eval loop asks to classify failures as prompt, SOP, tool, data source or rubric root cause.
Existing KB snippet: 失败复盘只写这次做错了。
User/automation request: Design failure schema.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-092 · Scheduled source scan should not auto-promote stale daily items · ★★★★
- source_type: `newsletter`
- eval_type: `workflow`
- capability_tags: ["scheduler", "promotion", "source-log"]
- source_urls: ["https://news.smol.ai/"]
- source_title: AINews daily source
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: AINews daily source (live page accessed 2026-07-11).
Source URL(s): https://news.smol.ai/
Observed signal: AINews has weekday cadence and dense issue summaries.
Existing KB snippet: 计划每天自动更新长期知识库。
User/automation request: Design scheduled workflow.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-093 · Regression set must preserve historical failures after v0.4 · ★★★★
- source_type: `user_project`
- eval_type: `workflow`
- capability_tags: ["regression", "dataset-governance", "eval"]
- source_urls: ["file://~/Documents/KB-Agent/evals/02-challenge-dataset-v0.3.md"]
- source_title: Challenge dataset v0.3
- source_date: local project 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Challenge dataset v0.3 (local project 2026-07-11).
Source URL(s): file://~/Documents/KB-Agent/evals/02-challenge-dataset-v0.3.md
Observed signal: v0.3 itself failed source-realness and harness-separation expectations.
Existing KB snippet: 新版数据集可能覆盖掉旧失败。
User/automation request: Create regression governance.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-094 · Holdout split prevents prompt overfitting · ★★★★
- source_type: `paper`
- eval_type: `workflow`
- capability_tags: ["holdout", "eval-design", "anti-overfit"]
- source_urls: ["https://arxiv.org/abs/2406.04244"]
- source_title: Benchmark contamination survey
- source_date: published 2024-06-06
- accessed_at: 2026-07-11
- snapshot_policy: `frozen`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Benchmark contamination survey (published 2024-06-06).
Source URL(s): https://arxiv.org/abs/2406.04244
Observed signal: The survey motivates contamination-aware evaluation design.
Existing KB snippet: 所有挑战都拿来调 prompt。
User/automation request: Design dataset split policy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-095 · Automation should patch SOP after incidents, not only docs · ★★★★★
- source_type: `github_issue`
- eval_type: `workflow`
- capability_tags: ["incident", "sop-patch", "security"]
- source_urls: ["https://github.com/huggingface/blog/issues/3364", "https://github.com/langchain-ai/langchain/issues/38723"]
- source_title: Security and dependency drift issues
- source_date: 2026 issues accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: Security and dependency drift issues (2026 issues accessed 2026-07-11).
Source URL(s): https://github.com/huggingface/blog/issues/3364 ; https://github.com/langchain-ai/langchain/issues/38723
Observed signal: One issue highlights secret exposure; another highlights dependency drift.
Existing KB snippet: 事故修复后只改正文。
User/automation request: Define post-incident loop.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 十一、抗幻觉、假新闻、低可信与不可验证来源
### CH-096 · Fake urgent deprecation headline must be checked against official date · ★★★★★
- source_type: `synthetic_wrapper`
- eval_type: `reject`
- capability_tags: ["fake-news", "official-check", "deprecation"]
- source_urls: ["https://developers.openai.com/api/docs/deprecations"]
- source_title: OpenAI deprecations official page
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `regression`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: OpenAI deprecations official page (live page accessed 2026-07-11).
Source URL(s): https://developers.openai.com/api/docs/deprecations
Observed signal: A pasted social post claims Assistants API is removed tomorrow, while official docs say shutdown is 2026-08-26.
Existing KB snippet: agent receives user-pasted headline without source.
User/automation request: Decide whether to update KB immediately.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-097 · Paywalled PM article title is not enough to write a summary · ★★★★
- source_type: `blog`
- eval_type: `reject`
- capability_tags: ["paywall", "summary", "copyright"]
- source_urls: ["https://www.lennysnewsletter.com/"]
- source_title: Lenny's Newsletter
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `regression`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Lenny's Newsletter (live page accessed 2026-07-11).
Source URL(s): https://www.lennysnewsletter.com/
Observed signal: Only a title and teaser of a PM interview are visible; full content is not available to the agent.
Existing KB snippet: 用户希望生成完整访谈纪要。
User/automation request: Handle unavailable source.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-098 · Wikipedia model pages are not sufficient for current provider docs · ★★★★
- source_type: `blog`
- eval_type: `fact_check`
- capability_tags: ["wikipedia", "source-authority", "model-info"]
- source_urls: ["https://en.wikipedia.org/wiki/Qwen", "https://help.aliyun.com/zh/model-studio/models"]
- source_title: Qwen Wikipedia page and Alibaba official model docs
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `direct_real`
- split: `full`
- difficulty_vector: fact_verification=4, source_conflict=3, structural_impact=3, risk_level=4, autonomy_required=4

#### Actor Input
Input source snapshot: Qwen Wikipedia page and Alibaba official model docs (live pages accessed 2026-07-11).
Source URL(s): https://en.wikipedia.org/wiki/Qwen ; https://help.aliyun.com/zh/model-studio/models
Observed signal: A Wikipedia page may summarize model history while Alibaba official docs show current platform models.
Existing KB snippet: 模型表准备直接用维基百科最新版本字段。
User/automation request: Choose source hierarchy.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-099 · Newsletter model launch summary needs official-source verification · ★★★★★
- source_type: `newsletter`
- eval_type: `fact_check`
- capability_tags: ["rumor", "newsletter", "model-launch"]
- source_urls: ["https://news.smol.ai/", "https://developers.openai.com/api/docs/models"]
- source_title: AINews and OpenAI model docs
- source_date: live pages accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `live`
- realness: `direct_real`
- split: `holdout`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: AINews and OpenAI model docs (live pages accessed 2026-07-11).
Source URL(s): https://news.smol.ai/ ; https://developers.openai.com/api/docs/models
Observed signal: A newsletter summarizes a model launch and pricing; official docs are the source of record for API behavior.
Existing KB snippet: 模型更新文档准备只引用 newsletter 摘要。
User/automation request: Verify launch facts.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.

### CH-100 · 404 or inaccessible source should create a verification task, not hallucinated content · ★★★★★
- source_type: `synthetic_wrapper`
- eval_type: `reject`
- capability_tags: ["404", "unavailable-source", "verification"]
- source_urls: ["https://api-docs.deepseek.com/quick_start/pricing/"]
- source_title: DeepSeek pricing official page as fallback source
- source_date: live page accessed 2026-07-11
- accessed_at: 2026-07-11
- snapshot_policy: `hybrid`
- realness: `real_wrapped`
- split: `holdout`
- difficulty_vector: fact_verification=5, source_conflict=4, structural_impact=5, risk_level=5, autonomy_required=5

#### Actor Input
Input source snapshot: DeepSeek pricing official page as fallback source (live page accessed 2026-07-11).
Source URL(s): https://api-docs.deepseek.com/quick_start/pricing/
Observed signal: A candidate source URL pasted by a feed is inaccessible, but the same topic has an official pricing page.
Existing KB snippet: 自动抓取器拿到一个失效链接，标题声称 DeepSeek 调价。
User/automation request: Handle broken source.

#### Task
Decide the correct KB-Agent action: collect, reject, route, update, refactor, visualize, rollback, or ask for confirmation. Return the target KB location, source metadata, changelog note, and any flywheel/SOP update needed.


## 覆盖矩阵

- 一、真实信源噪音：issue、PR、社区投稿不是都该进库: CH-001~CH-010
- 二、官方文档演化：deprecation、migration、pricing、release notes: CH-011~CH-020
- 三、榜单、benchmark 与数据口径: CH-021~CH-030
- 四、知识库结构与公开形态的真实标杆: CH-031~CH-040
- 五、高频动态管线如何不污染长期库: CH-041~CH-048
- 六、版权、隐私、安全与公开发布风险: CH-049~CH-056
- 七、面向中国头部 AI 公司 AI PM 求职: CH-057~CH-071
- 八、理论演化：历史链条与最新版策略: CH-072~CH-079
- 九、图表、dashboard、visualizer 与可观测性: CH-080~CH-087
- 十、自动化、人类把关、回滚与数据飞轮: CH-088~CH-095
- 十一、抗幻觉、假新闻、低可信与不可验证来源: CH-096~CH-100

## 使用建议

- smoke set：15 条，用于每次 prompt/SOP 改动后的快速回归。
- regression set：15 条，保留历史失败、用户指出的问题和真实事故复盘。
- holdout set：10 条，不用于日常 prompt 调参，只用于阶段性验收。
- full set：100 条，用于周度全量行为评测。
