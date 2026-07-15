# Architecture rule — the vague version (weak feedforward)

> Keep the architecture clean and separate concerns.

**Why this steers badly.** "Clean" and "separate concerns" have no definition the agent can act
on. A single class that prices, taxes, settles, and prints can be described as "separated concerns"
(each is a different line!) and reads as compliant. The words feel like architecture guidance while
leaving every actual boundary — what is a port, what is an adapter, what may import what — to the
agent's default, which is to copy whatever the surrounding code already does.

**Tradeoff.** Cheap to write, applies to any codebase, ages well — and does almost nothing. A rule
you cannot fail is a rule that cannot steer. Compare `architecture-concrete.md`: it names the
boundary precisely enough that a violation is unambiguous, to a human *and* to a hook.
