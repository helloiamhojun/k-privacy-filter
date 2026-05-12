# OPF Train Decision

## Result

- opf train command: runnable
- data format issue: fixed by converting spans list to OPF span mapping
- smoke train loop: completed 1 epoch and produced validation loss
- checkpoint saving: unstable in current Colab session
- LoRA option in CLI help: not confirmed

## Decision

Proceed to peft LoRA fallback for final training.

Reason:
The project requirement is LoRA adaptation, but the current opf train CLI does not expose a confirmed LoRA/adapter option. Also, checkpoint saving was unstable during smoke testing. We will use OPF for baseline/inference and peft for LoRA training.
