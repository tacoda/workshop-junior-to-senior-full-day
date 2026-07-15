---
description: Run the five comprehension questions on a file or diff
argument-hint: [file or diff to examine]
---

You are helping me *comprehend* code before I trust it — not rewrite it. Do not
change any files. Examine: $ARGUMENTS

Answer these five questions, each in two or three sentences, and nothing else:

1. **What does this do, in one sentence?**
2. **Where does the change enter the system, and where does it leave?** Trace the path.
3. **Why is it written this way?** If neither a rule (CLAUDE.md, .claude/rules/) nor a
   doc answers, say so plainly — that is a charter gap, not a fact you should invent.
4. **Is it consistent with the rest of the codebase and the charter?** Name the nearest
   code or rule it agrees with, and any it contradicts.
5. **Which part would you call slop** — plausible, passing, and quietly wrong or drifted?

End with one line: the single thing I should verify myself before trusting this.
