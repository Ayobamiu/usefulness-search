# Demo query candidates

All 18 training tasks were checked. Held-out tasks are never used for the demo.
Rule: both agents answer correctly, and our top 3 shares at most 1 page with Keenable's top 3.
Among those: fewest shared pages, then lowest task id. The usage history excludes the task itself.

**Chosen: t16**

| task | top-3 pages shared with Keenable | naive correct | ours correct | qualifies | question |
|---|---|---|---|---|---|
| t01 | 2 | yes | no | no | How do I paginate results in the Stripe API? Which parameter fetches the next page of a list? |
| t02 | 2 | yes | yes | no | For how long does Stripe keep an idempotency key before it can be pruned and reused as a new request? |
| t04 | 3 | yes | yes | no | Which date value should be sent in the X-GitHub-Api-Version header to pin the current GitHub REST API version? |
| t05 | 3 | yes | yes | no | How many requests per hour does the GitHub REST API allow for unauthenticated requests under the primary rate limit? |
| t06 | 3 | yes | yes | no | In which Python version was the tomllib module added to the standard library? |
| t08 | 3 | yes | yes | no | In which Python version was itertools.batched added? |
| t09 | 3 | yes | yes | no | Which major PostgreSQL version first added the SQL MERGE command? |
| t10 | 3 | yes | yes | no | Which SQLite release first supported the RETURNING clause on INSERT, UPDATE and DELETE? |
| t12 | 3 | yes | yes | no | Which RUN flag in a Dockerfile keeps a package manager's download directory between builds without adding it to the image layer? |
| t13 | 3 | yes | yes | no | Which Git version introduced the git switch and git restore commands? |
| t14 | 2 | yes | yes | no | What is the default value of terminationGracePeriodSeconds for a Kubernetes Pod? |
| t16 | 1 | yes | yes | yes | In Next.js 15, GET Route Handlers are no longer cached by default. Which value of the dynamic route segment config option opts a GET handler back into caching? |
| t17 | 3 | yes | yes | no | Which Node.js command-line flag, added in v20.6.0, loads environment variables from a file without the dotenv package? |
| t18 | 3 | yes | yes | no | Which FastAPI app parameter replaces the deprecated on_event startup and shutdown handlers? |
| t20 | 3 | yes | yes | no | Which response_format type makes the OpenAI Chat Completions API guarantee output that matches a JSON Schema you supply (Structured Outputs)? |
| t21 | 2 | yes | yes | no | Which Redis command, added in 6.2.0, returns the value of a key and deletes the key in one atomic step? |
| t22 | 2 | yes | yes | no | Which operator, added in TypeScript 4.9, checks that an expression matches a type without changing the expression's inferred type? |
| t24 | 3 | yes | yes | no | Which flag of aws s3 sync removes files from the destination that no longer exist in the source? |

This is the best-looking example, not the average. The demo's end card shows the held-out average.
