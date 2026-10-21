## Build Steps

1. **Environment setup**
   - Load `.env` with `python-dotenv`.
   - Read `GROQ_API_KEY` and `DATABASE_URL`.
   - Create the Groq client and keep the model name in config.

2. **Database layer**
   - Create the SQLAlchemy engine and `SessionLocal`.
   - Define `Base` for models.
   - Define the `Event` model with `id`, `title`, `event_date`, `event_time`, and `created_at`.

3. **Calendar tools**
   - `create_calender_event`: parse date/time, insert an `Event`, commit, refresh, and return the created event.
   - `list_calender_event`: parse a date and return all events for that date.
   - Return structured results: `{"ok": True, ...}` or `{"ok": False, "error": {...}}`.

4. **Tool schemas**
   - Define JSON function schemas for each tool.
   - Include name, description, parameter types, required fields, and `additionalProperties: False`.
   - These schemas are sent to the LLM so it knows which tools it can call.

5. **Tool registry**
   - Map each tool name to its function and schema.
   - This lets the loop look up a tool by the name returned by the LLM.

6. **Argument validation**
   - Compare required arguments with provided arguments.
   - Reject missing arguments with `MISSING ARGUMENTS`.
   - Reject unexpected arguments with `INVALID ARGUMENTS`.
   - Return `{"ok": True}` when valid.

7. **Tool execution**
   - Create a DB session for each tool call.
   - Pass `db` to the tool function.
   - Always close the session in `finally`.
   - Return the tool result unchanged.

8. **Retry policy**
   - Retry only on `DATABASE_ERROR`.
   - Use a maximum of 3 retries.
   - Start with a 1-second delay and double it after each attempt.
   - Open a fresh DB session for every retry.

9. **Duplicate-call detection**
   - Track tool name + arguments for each assistant turn.
   - Reject repeated calls with `DUPLICATE_TOOL_CALL`.
   - This prevents the same tool from running twice in one turn.

10. **Agent loop**
    - Add a system prompt.
    - Collect available tool schemas from the registry.
    - Read user input.
    - Send messages plus tools to the LLM.
    - If the LLM returns tool calls:
      - Append the assistant tool-call message.
      - Parse arguments as JSON.
      - Validate arguments.
      - Check for duplicates.
      - Execute the tool.
      - Append the tool result as a `tool` message.
    - If the LLM returns normal content, print it and append it.
    - Repeat until the user types `exit`.

11. **Entry point**
    - `app/main.py` starts the loop with `asyncio.run(agent_loop())`.

## Current Limitations

- After a tool call, the loop waits for another user message before the model summarizes the tool result.
- Tool calls are executed sequentially; there is no parallel execution.
- No timeout or cancellation handling.
- No idempotency keys for side-effecting tools.
- No tool permissions or per-user access control.
- No structured observability (latency, success rate, tool traces).
- Tests are placeholders.
- `datetime.utcnow()` is deprecated; prefer timezone-aware UTC timestamps.

## Next Steps

1. - Tool execution: sequential and parallel
   - Detect dependencies between tool calls.
   - Execute dependent calls sequentially in order.
   - Execute independent calls in parallel.
   - Use separate DB sessions per parallel call.
   - Preserve result ordering when appending tool messages.
   - Handle partial failures and cancellation safely.
   - Add tests for sequential, parallel, and mixed execution.

2. **Continue the turn after tool results**
   - Send tool results back to the LLM automatically so it can produce a final answer without waiting for another user message.

3. **Timeouts and cancellation**
   - Add per-tool and per-turn timeouts.
   - Cancel pending parallel calls when one call fails or the turn is aborted.

4. **Idempotency and side effects**
   - Add idempotency keys for write operations to prevent duplicate events on retries.

5. **Tool permissions**
   - Control which tools a user or agent is allowed to invoke.

6. **Observability**
   - Log tool name, arguments, latency, success/failure, and error code for every call.

7. **Evaluation**
   - Measure tool selection accuracy, argument correctness, and end-to-end task success.

8. **Production hardening**
   - Replace placeholders with real tests.
   - Replace `datetime.utcnow()` with timezone-aware UTC timestamps.
   - Add dependency declarations for SQLAlchemy, Alembic, psycopg, and python-dotenv.
