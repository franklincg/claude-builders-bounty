# Tool map

This companion skill uses the real Mermail MCP catalog. Hosts may qualify names (for example `Mermail:list_mailboxes`); always call the exact identifier exposed by the connected host.

## Read path

| Intent | Mermail operation | Notes |
| --- | --- | --- |
| Resolve mailbox | `list_mailboxes` | Prefer `public_id` as `mailboxId`. |
| Find candidate mail | `list_emails`, `search_emails` | Keep searches bounded to known sponsors, subjects, or opportunity IDs. |
| Read one message | `get_email` | Interpret body only when `scan_status: clean`. |
| Read conversation | `get_thread` | Use for context after selecting an unambiguous thread. |
| Extra context | `get_email_context` | Use only when the base message is insufficient. |

## Write path

| Intent | Mermail operation | Safety condition |
| --- | --- | --- |
| Prepare response | `save_draft` | Preferred default; a draft is not authorization to send. |
| Reply | `reply_to_email` | Exact recipient/body preview + fresh human approval. |
| New email | `send_email` | Exact recipient/body preview + fresh human approval. |
| Escalate | `forward_email` | Exact destination preview + fresh human approval. |

## Optional mailbox provisioning

`create_mailbox` is not a discovery operation. Provision only after explicit user authorization or after previewing the address and current credit cost when no suitable mailbox exists.

## Data handling

- Pass MCP query arguments as native JSON objects, never stringified JSON blobs.
- Preserve stable message/thread IDs in evidence records.
- Do not copy full private message bodies into monitoring summaries when sender, subject, timestamp, and a short paraphrase are enough.
- Never log or summarize API keys, OAuth tokens, claim codes, magic links, wallet credentials, or authentication cookies.

## State classification evidence

Strong evidence examples:

- `paid`: receipt, transaction/settlement identifier, or explicit platform payout confirmation tied to the opportunity.
- `approved`: explicit award/acceptance/hire/merge-for-reward decision.
- `payment_pending`: acceptance plus an explicit future payout/invoice step.
- `action_required`: a concrete bounded request for revision, evidence, or clarification.
- `rejected`: explicit decline, duplicate, invalid report, lost award, or closed-without-payment decision.
- `blocked`: explicit requirement for login, KYC, signature, wallet approval, deposit, private access, or credential unavailable to the agent.

Weak evidence such as praise, emoji reactions, generic acknowledgements, or silence must not be upgraded to approval/payment.