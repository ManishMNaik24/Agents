User
 ↓
LLM -> Response
 ↓
If Tool Selection
 ↓
Tool Call
 ↓
┌──────────────────────────┐
│ Runtime                  │
│                          │
│ Tool exists?             │
│ Authorization            │
│ JSON parsing             │
│ Argument validation      │
│ Duplicate detection      │
│ Execution                │
│ Timeout                  │
│ Retry + backoff          │
│ Error handling           │
└──────────────────────────┘
 ↓
Tool Result
 ↓
tool_call_id
 ↓
LLM
 ↓
Final answer OR another iteration



Components :-

Tool Schema — Defines the tool's name, purpose, arguments, types, and required fields.

Tool Registry — Maps each tool name to its schema and actual Python function.

Tool Selection — The LLM decides which registered tool to call.

Tool Call Parsing — Runtime extracts the tool name and parses the LLM's JSON arguments.

Argument Validation — Checks required and unexpected arguments before execution.

Tool Execution — Runtime invokes the actual Python tool with validated arguments.

Dependency Injection — Runtime provides internal dependencies like the SQLAlchemy db session.

DB Session Lifecycle — Creates a fresh session for an execution attempt and closes it afterward.

Structured Errors — Tools/runtime return {ok, data/error} instead of uncontrolled failures.

Error Classification — Errors are categorized so the runtime knows whether they should be retried or returned.

Retry — Re-executes a tool when a recoverable error occurs.

Exponential Backoff — Increases the delay between retries: 1s → 2s → 4s.

Maximum Retries — Prevents unlimited retry attempts.

Timeout — Stops waiting when a tool exceeds its execution limit.

Duplicate Tool-Call Detection — Prevents identical tool calls from executing twice within the same LLM response.

Parallel Tool Execution — Independent tool calls from one LLM response can execute concurrently.

Tool Result Handling — Sends each tool's structured result back to the LLM.

Tool Call ID Mapping — Associates each result with the correct tool_call_id.

Authorization — Checks whether the current user is allowed to execute a tool; we'll eventually derive this from the user's stored permissions.

Agent Loop — Repeatedly performs LLM → tools → results → LLM.

Agent Iteration — One LLM decision plus the tool executions resulting from that decision.

Termination — Stops when the LLM produces no tool calls.

Maximum Iterations — Stops the agent if it keeps requesting tools indefinitely.